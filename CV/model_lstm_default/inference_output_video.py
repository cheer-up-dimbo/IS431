#!/usr/bin/env python3
import os
import cv2
import numpy as np
import torch
import subprocess
from collections import deque
from ultralytics import YOLO

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
VIDEO_PATH   = "/home/yogee/Desktop/boxing_ai_ws/zakir_bottom.mp4"

# Final H.264 output for preview in VSCode
OUTPUT_PATH  = "/home/yogee/Desktop/boxing_ai_ws/zakir_bottom_pred.mp4"

# Temporary file written by OpenCV using mp4v codec
RAW_OUTPUT_PATH = "/home/yogee/Desktop/boxing_ai_ws/zakir_bottom_pred_raw.mp4"

POSE_MODEL_PATH = "models/pretrained_pose_estimator/yolo11n-pose.pt"
CLS_MODEL_PATH  = "models/trained_action_model/best_boxing_lstm.pth"
SEQ_LEN         = 50
DEVICE          = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

SKELETON = [
    (0,1),(0,2),(1,3),(2,4),
    (0,5),(0,6),(5,7),(7,9),(6,8),(8,10),
    (5,6),(5,11),(6,12),(11,12),(11,13),(13,15),(12,14),(14,16)
]

num_kpts  = 17
input_dim = num_kpts * 2

# ---------------------------------------------------------------------------
# Load Models
# ---------------------------------------------------------------------------
pose_model = YOLO(POSE_MODEL_PATH)
pose_model.fuse()

class LSTMClassifier(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_layers=2, num_classes=len(CLASSES), dp=0.3):
        super().__init__()
        self.lstm = torch.nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dp)
        self.head = torch.nn.Sequential(
            torch.nn.Linear(hidden_dim, hidden_dim // 2),
            torch.nn.ReLU(),
            torch.nn.Dropout(dp),
            torch.nn.Linear(hidden_dim // 2, num_classes)
        )

    def forward(self, x):
        out, (h_n, _) = self.lstm(x)
        return self.head(h_n[-1])

cls_model = LSTMClassifier(input_dim).to(DEVICE)
cls_model.load_state_dict(torch.load(CLS_MODEL_PATH, map_location=DEVICE))
cls_model.eval()

# ---------------------------------------------------------------------------
# Video Inference
# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Cannot open video: {VIDEO_PATH}")

fps = cap.get(cv2.CAP_PROP_FPS) or 30
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# OpenCV mp4v codec (supported by default builds)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(RAW_OUTPUT_PATH, fourcc, fps, (w, h))

if not writer.isOpened():
    raise RuntimeError("VideoWriter failed to open using mp4v codec")

buffer = deque(maxlen=SEQ_LEN)
pred_label, conf = None, 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose_model(rgb)[0]

    if result.keypoints is not None and result.keypoints.xy.shape[0] > 0:
        kps = result.keypoints.xy.cpu().numpy()[0]
    else:
        kps = np.zeros((num_kpts, 2), dtype=float)

    buffer.append(kps.flatten())

    if len(buffer) == SEQ_LEN:
        seq = np.stack(buffer, axis=0)
        seq = (seq - seq.mean(axis=0)) / (seq.std(axis=0) + 1e-6)

        x = torch.from_numpy(seq).unsqueeze(0).to(DEVICE).float()
        with torch.no_grad():
            logits = cls_model(x)
            pred = logits.argmax(dim=1).item()
            conf = torch.softmax(logits, dim=1)[0, pred].item()

        pred_label = CLASSES[pred]

    # Draw skeleton
    for a, b in SKELETON:
        x1, y1 = kps[a]
        x2, y2 = kps[b]
        if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    for x, y in kps:
        if x > 0 and y > 0:
            cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)

    # Draw label
    if pred_label is not None:
        label_text = f"{pred_label.upper()} ({conf*100:.1f}%)"
        (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 1.6, 3)
        x_pos = (w - tw) // 2
        y_pos = 60

        cv2.rectangle(frame, (x_pos - 10, y_pos - th - 10),
                      (x_pos + tw + 10, y_pos + 10), (0, 0, 0), -1)
        cv2.putText(frame, label_text, (x_pos, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 255), 3, cv2.LINE_AA)

    writer.write(frame)

cap.release()
writer.release()
print(f"Raw video saved to: {RAW_OUTPUT_PATH}")

# ---------------------------------------------------------------------------
# Convert to H.264 using ffmpeg (required for VSCode preview)
# ---------------------------------------------------------------------------
try:
    cmd = [
        "ffmpeg", "-y",
        "-i", RAW_OUTPUT_PATH,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-movflags", "+faststart",
        OUTPUT_PATH
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print(f"H.264 video saved to: {OUTPUT_PATH}")

    # Remove temporary file
    try:
        os.remove(RAW_OUTPUT_PATH)
    except OSError:
        pass

except FileNotFoundError:
    print("ffmpeg is not installed. Install it using: sudo apt install ffmpeg")
    print(f"Raw video is still available at: {RAW_OUTPUT_PATH}")

except subprocess.CalledProcessError:
    print("ffmpeg failed during conversion.")
    print(f"Raw video is available at: {RAW_OUTPUT_PATH}")
