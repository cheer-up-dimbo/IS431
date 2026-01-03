#!/usr/bin/env python3
import cv2
import numpy as np
import torch
import json
import time
from collections import deque
from ultralytics import YOLO
from combo_assembler import ComboAssembler
from decision_tree import DecisionTreeEngine

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
SELECTED_STYLE  = "balanced"  # Options: "aggressive", "defensive", "balanced"
POSE_MODEL_PATH = "models/pretrained_pose_estimator/yolo11n-pose.pt"
CLS_MODEL_PATH  = "models/trained_action_model/best_boxing_lstm.pth"
SEQ_LEN         = 50
DEVICE          = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Your classes in the same order as training
CLASSES = [
    "block",
    "cross",
    "idle",
    "jab",
    "left_hook",
    "left_uppercut",
    "right_hook",
    "right_uppercut",
]

# Map predicted labels to punch IDs (1-6) or None
def map_label_to_punch_id(label):
    mapping = {
        "jab": "1",
        "cross": "2",
        "left_hook": "3",
        "right_hook": "4",
        "left_uppercut": "5",
        "right_uppercut": "6",
    }
    return mapping.get(label.lower(), None)

# COCO skeleton connections (0-indexed keypoints)
SKELETON = [
    (0,1),(0,2),(1,3),(2,4),
    (0,5),(0,6),(5,7),(7,9),(6,8),(8,10),
    (5,6),(5,11),(6,12),(11,12),(11,13),(13,15),(12,14),(14,16)
]

# Hard-code number of keypoints to 17 (COCO)
num_kpts  = 17
input_dim = num_kpts * 2

# ──────────────────────────────────────────────────────────────────────────────
# LOAD & PREPARE MODELS
# ──────────────────────────────────────────────────────────────────────────────
# 1) Pose model
pose_model = YOLO(POSE_MODEL_PATH)
pose_model.fuse()  # optimize for inference

# 2) LSTM classifier (must match your training code)
class LSTMClassifier(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_layers=2, num_classes=len(CLASSES), dp=0.3):
        super().__init__()
        self.lstm = torch.nn.LSTM(input_dim,
                                  hidden_dim,
                                  num_layers,
                                  batch_first=True,
                                  dropout=dp)
        self.head = torch.nn.Sequential(
            torch.nn.Linear(hidden_dim, hidden_dim//2),
            torch.nn.ReLU(),
            torch.nn.Dropout(dp),
            torch.nn.Linear(hidden_dim//2, num_classes)
        )

    def forward(self, x):
        out, (h_n, _) = self.lstm(x)
        last = h_n[-1]            # (batch, hidden_dim)
        return self.head(last)    # (batch, num_classes)

# Instantiate & load weights
cls_model = LSTMClassifier(input_dim).to(DEVICE)
cls_model.load_state_dict(torch.load(CLS_MODEL_PATH, map_location=DEVICE))
cls_model.eval()

# ──────────────────────────────────────────────────────────────────────────────
# COMBO HANDLING
# ──────────────────────────────────────────────────────────────────────────────
def on_combo_finalized(combo_dict):
    """Called when ComboAssembler finalizes a combo."""
    print(f"\n[USER COMBO] {' → '.join(combo_dict['sequence'])} "
          f"({combo_dict['num_punches']} punches, {combo_dict['duration']:.2f}s)")
    
    # Get robot response
    decision = DecisionTreeEngine.decide(SELECTED_STYLE, combo_dict)
    robot_sequence = decision['response_sequence']
    robot_names = [DecisionTreeEngine.punch_id_to_name(pid) for pid in robot_sequence]
    
    print(f"[ROBOT] {' → '.join(robot_names)} "
          f"(strategy: {decision['strategy']}, timing: {decision['timing']})")

assembler = ComboAssembler(on_combo_callback=on_combo_finalized, debounce_sec=1.5)

# ──────────────────────────────────────────────────────────────────────────────
# REAL-TIME INFERENCE LOOP
# ──────────────────────────────────────────────────────────────────────────────
buffer = deque(maxlen=SEQ_LEN)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam.")

# Hysteresis tracking
current_label = None
consecutive_count = 0
last_prediction = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1) Pose detection (BGR→RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose_model(rgb)[0]  # single Results object

    # 2) Extract keypoints
    if result.keypoints is not None and result.keypoints.xy.shape[0] > 0:
        kps = result.keypoints.xy.cpu().numpy()[0]  # (17,2)
    else:
        kps = np.zeros((num_kpts, 2), dtype=float)

    # 3) Append to buffer
    buffer.append(kps.flatten())

    # 4) Classify when buffer full
    if len(buffer) == SEQ_LEN:
        seq = np.stack(buffer, axis=0)                 # (SEQ_LEN, input_dim)
        seq = (seq - seq.mean(axis=0)) / (seq.std(axis=0) + 1e-6)
        x = torch.from_numpy(seq).unsqueeze(0).to(DEVICE).float()
        with torch.no_grad():
            logits = cls_model(x)
            pred  = logits.argmax(dim=1).item()
            conf  = torch.softmax(logits, dim=1)[0, pred].item()
        label = CLASSES[pred]
        
        # Hysteresis logic
        if label == last_prediction:
            consecutive_count += 1
        else:
            consecutive_count = 1
            last_prediction = label
        
        # Accept label change if: 3 consecutive frames OR confidence > 0.80
        accept_change = (consecutive_count >= 3) or (conf > 0.80)
        
        if accept_change and label != current_label:
            # Label has changed - create event and feed to assembler
            current_label = label
            punch_id = map_label_to_punch_id(label)
            
            event = {
                "t": time.time(),
                "move": label,
                "punch": punch_id,
                "stance": "unknown",
                "distance": "unknown",
                "conf": conf
            }
            
            # Feed to combo assembler
            assembler.ingest_event(event)
            
            # Print JSON event
            print(json.dumps({
                "t": event["t"],
                "move": label,
                "conf": round(conf, 4),
                "stance": "unknown",
                "distance": "unknown"
            }), flush=True)
        
        cv2.putText(frame,
                    f"{label} ({conf*100:.1f}%)",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA)

    # 5) Draw skeleton
    for a, b in SKELETON:
        x1, y1 = kps[a]
        x2, y2 = kps[b]
        if x1>0 and y1>0 and x2>0 and y2>0:
            cv2.line(frame, (int(x1),int(y1)), (int(x2),int(y2)), (0,255,0), 2)
    for x, y in kps:
        if x>0 and y>0:
            cv2.circle(frame, (int(x),int(y)), 3, (0,0,255), -1)

    # 6) Display & exit
    cv2.imshow("Boxing Move Predictor", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
