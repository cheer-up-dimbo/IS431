# 🥊 Boxing AI Workspace

This workspace implements a full pose-based boxing-action recognition pipeline, including data preparation, pose extraction, temporal sequence modeling, and inference (offline and real-time).
It also contains experimental model variants and archived materials from earlier development phases.

The current system uses **2D keypoints** extracted from RGB video.
In future iterations, the model will be upgraded to use **3D skeletal data** from a depth camera, which is expected to significantly improve prediction stability and accuracy, especially for occluded or fast-motion actions.

---

## 🚀 1. Project Overview

The workflow consists of the following stages:

### 1. Data acquisition

Raw sparring, drill, padwork, and bagwork videos are collected and placed in `data_raw/`.

### 2. Timestamp labeling & segmentation

Start/end times of each action are labeled in a spreadsheet under `time_stamps/`.
`data_processing.ipynb` automatically segments the raw videos into labeled action clips.

### 3. Pose extraction

A YOLO-based pose estimator extracts **17 keypoints per frame**.
Outputs are stored as `.npy` arrays under `data_pose_estimated/`.

### 4. Visualization (optional)

Annotated videos with skeleton overlays are generated for sanity checking.

### 5. Temporal model training

Sliding windows of pose sequences (e.g., 50 frames) are fed into an LSTM classifier to learn eight actions:

- block
- jab
- cross
- left/right hook
- left/right uppercut
- idle

### 6. Inference

- **Offline inference** for recorded MP4s
- **Real-time inference** using a laptop webcam

### 7. Experimental modules

A GCN-based framework is included for research experiments on graph-structured pose data.

---

## 📂 2. Directory Structure

```
BOXING_AI_WS/
├── archive/                        # Legacy experiments and older scripts
│
├── data/
│   ├── data_labelled/              # Segmented and labeled video clips
│   ├── data_pose_estimated/        # 17-keypoint pose arrays (.npy)
│   ├── data_pose_visualization/    # Pose-annotated preview videos
│   ├── data_raw/                   # Original uncut videos
│   └── time_stamps/                # Timestamp spreadsheets (.xlsx)
│
├── inference_outputs/              # Generated inference videos
│
├── model_gcn/                      # GCN experimentation (not core pipeline)
│   ├── gcn_inference.py
│   └── gcn_training.py
│
├── model_lstm_default/             # Main LSTM pipeline
│   ├── inference_output_video.py   # Offline inference on MP4 files
│   ├── inference_real_time.py      # Real-time webcam inference
│   ├── training.py                 # LSTM training script
│   └── training.ipynb              # Notebook version of training workflow
│
├── models/                         # Model weights and pretrained pose estimator
│   ├── pretrained_pose_estimator/
│   └── trained_action_model/
│
├── data_processing.ipynb           # Segmentation + pose extraction notebook
└── README.md
```

---

## 🛠️ 3. Requirements

- Python 3.8+
- PyTorch
- Ultralytics / YOLO
- OpenCV
- FFmpeg (required for generating H.264 inference videos)

Install the main packages:

```bash
pip install torch ultralytics opencv-python numpy pandas scikit-learn
sudo apt install ffmpeg
```

---

## ▶️ 4. Step-by-Step Usage

### Step 1 — Segment raw videos

1. Open `time_stamps/Boxing_Videos_Timestamp.xlsx`.
2. Fill in Start/End timestamps for each action.
3. Run `data_processing.ipynb` to automatically slice videos into labeled clips.
4. Output clips appear under `data_labelled/`.

### Step 2 — Extract poses

Configure paths in `data_processing.ipynb` and run the pose extraction cells.
The notebook will populate:

- `data_pose_estimated/` with `.npy` pose arrays
- `data_pose_visualization/` with sample annotated videos

### Step 3 — Train the LSTM model

You can use either:

**Command-line:**

```bash
python model_lstm_default/training.py
```

**Or via Jupyter:**

1. Open `training.ipynb`.
2. Run the preprocessing and dataloader setup cells.
3. Train the LSTM using sliding windows + early stopping.
4. The best checkpoint is saved under `models/trained_action_model/`.

### Step 4 — Offline inference

```bash
python model_lstm_default/inference_output_video.py
```

This produces annotated MP4s under `inference_outputs/`.

### Step 5 — Real-time webcam inference

```bash
python model_lstm_default/inference_real_time.py
```

The webcam stream is processed frame-by-frame, with pose extraction and action prediction overlaid in real time.

---

## 🧬 5. Current Limitations and Future Work

### Current: 2D pose-based predictions

The system currently uses **2D keypoints only**, extracted from standard RGB video.
Limitations include:

- Sensitivity to occlusions
- Reduced accuracy during fast or diagonal movements
- Lack of depth information for hooks/uppercuts crossing the body

### Future: 3D depth-camera training

A planned upgrade is to use **3D skeletal keypoints** generated from a depth camera (e.g., Intel RealSense or Azure Kinect).
This will improve:

- Motion disambiguation (e.g., left vs. right hand crossing depth)
- Stability during fast strikes
- Robustness when joints are partially occluded

3D keypoints will be integrated into both LSTM and GCN variants to evaluate performance gains.

---

## 🎯 6. Next Steps

- Expand the labeled dataset
- Evaluate additional architectures (Temporal CNNs, Transformers, ST-GCN)
- Integrate 3D depth-based pose estimation
- Experiment with ONNX/TensorRT for real-time deployment
- Add temporal smoothing and confidence-based filtering
- Investigate sequence augmentation methods

---
