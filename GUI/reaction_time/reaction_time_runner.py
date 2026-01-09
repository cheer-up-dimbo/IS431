"""
BoxBunny Reaction Trainer v2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Controls: SPACE start | R replay | S stats | Q quit
"""

import cv2
import numpy as np
import time
import random
import threading
from ultralytics import YOLO
import os
import json
from collections import deque
import math

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1" 
os.environ["MKL_NUM_THREADS"] = "1"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MODEL_PATH = "models/yolo11s-pose.pt"
COUNTDOWN_SECS = 3
CUE_DELAY = (1.5, 4)
MAX_REACTION = 5.0
CAM_W, CAM_H = 1280, 720
STATS_FILE = "boxbunny_stats.json"

# Punch detection - default thresholds (adjustable via GUI)
# These are base values that get modified by sensitivity setting
DEFAULT_PUNCH_DISTANCE = 60   # Distance from baseline to trigger
DEFAULT_PUNCH_VELOCITY = 30   # Velocity threshold
DEFAULT_FRAMES_REQUIRED = 3   # Consecutive frames needed

# Sensitivity presets: (distance, velocity, frames) - lower = more sensitive
SENSITIVITY_PRESETS = {
    1: (30, 15, 2),   # Very High - triggers easily (good for low movement/lighting)
    2: (45, 22, 2),   # High
    3: (60, 30, 3),   # Medium (default)
    4: (80, 40, 3),   # Low
    5: (100, 50, 4),  # Very Low - requires strong movement
}

# Replay
REPLAY_PRE = 10
REPLAY_POST = 35
REPLAY_SPEED = 0.07

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COLORS (BGR) - Clean Orange & Black Theme
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class C:
    # Dark base
    BLACK = (0, 0, 0)
    DARK = (15, 15, 15)
    OVERLAY = (20, 20, 20)
    
    # Orange accent palette
    ORANGE = (40, 140, 255)           # Primary orange
    ORANGE_BRIGHT = (50, 165, 255)    # Bright orange
    ORANGE_DIM = (30, 100, 180)       # Muted orange
    AMBER = (60, 180, 255)            # Light amber
    
    # Supporting colors
    GREEN = (100, 210, 130)           # Success green
    RED = (80, 80, 230)               # Alert red
    
    # Text
    WHITE = (255, 255, 255)
    LIGHT = (210, 210, 210)
    GRAY = (140, 140, 140)
    DIM = (80, 80, 80)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class State:
    phase = "idle"
    countdown = 0
    active = False
    cue_on = False
    cue_time = None
    result_ms = None
    
    # Calibration (during last second of countdown)
    baseline_left = None
    baseline_right = None
    baseline_scale_left = None  # Depth proxy: shoulder-to-wrist distance
    baseline_scale_right = None
    calibrated = False
    
    # Detection
    move_frames = 0
    
    # Sensitivity settings (1-5, 3 is default/medium)
    sensitivity = 3
    punch_distance = DEFAULT_PUNCH_DISTANCE
    punch_velocity = DEFAULT_PUNCH_VELOCITY
    frames_required = DEFAULT_FRAMES_REQUIRED
    show_settings = False
    
    # Replay
    buffer = deque(maxlen=150)
    cue_idx = -1
    replay_data = []
    show_replay = False
    replay_idx = 0
    
    # UI
    show_stats = True
    hover = None
    
    # Stats
    stats = {
        "attempts": 0,
        "success": 0,
        "best": float('inf'),
        "times": [],
        "session": []
    }
    
    exit = False

def update_sensitivity(level):
    """Update detection thresholds based on sensitivity level."""
    level = max(1, min(5, level))  # Clamp to 1-5
    s.sensitivity = level
    s.punch_distance, s.punch_velocity, s.frames_required = SENSITIVITY_PRESETS[level]

s = State()
lock = threading.Lock()
model = None
cap = None
btn_start = btn_replay = btn_settings = btn_quit = None
btn_sens_up = btn_sens_down = None
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_BOLD = cv2.FONT_HERSHEY_DUPLEX

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# KALMAN FILTER - Smooth out pose jitter
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class KalmanFilter2D:
    """2D Kalman filter for position + velocity tracking."""
    
    def __init__(self, process_noise=0.05, measurement_noise=2.0):
        # State: [x, y, vx, vy]
        self.x = np.zeros(4)
        
        # State transition (constant velocity model)
        self.F = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float64)
        
        # Measurement matrix (we observe position only)
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=np.float64)
        
        # Process noise
        self.Q = np.eye(4) * process_noise
        self.Q[2:, 2:] *= 2  # More noise on velocity
        
        # Measurement noise
        self.R = np.eye(2) * measurement_noise
        
        # State covariance
        self.P = np.eye(4) * 100
        
        self.initialized = False
    
    def update(self, measurement):
        """Update with new measurement, return smoothed position."""
        if measurement is None:
            return self.get_position()
        
        z = np.array(measurement, dtype=np.float64)
        
        if not self.initialized:
            self.x[:2] = z
            self.x[2:] = 0
            self.initialized = True
            return z
        
        # Predict
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        # Update
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P
        
        return self.x[:2]
    
    def get_position(self):
        return self.x[:2] if self.initialized else None
    
    def get_velocity(self):
        return np.linalg.norm(self.x[2:4]) if self.initialized else 0
    
    def reset(self):
        self.x = np.zeros(4)
        self.P = np.eye(4) * 100
        self.initialized = False

# Kalman filters for each wrist
kf_left = KalmanFilter2D()
kf_right = KalmanFilter2D()

# Scale trackers for depth (shoulder-to-wrist distance)
# Using exponential moving average for smoothing
class ScaleTracker:
    def __init__(self, alpha=0.3):
        self.alpha = alpha  # Smoothing factor
        self.scale = None
        self.initialized = False
    
    def update(self, scale):
        """Update with new scale measurement."""
        if scale is None:
            return self.scale
        
        if not self.initialized:
            self.scale = scale
            self.initialized = True
        else:
            # Exponential moving average
            self.scale = self.alpha * scale + (1 - self.alpha) * self.scale
        
        return self.scale
    
    def get_scale(self):
        return self.scale
    
    def reset(self):
        self.scale = None
        self.initialized = False

scale_tracker_left = ScaleTracker()
scale_tracker_right = ScaleTracker()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_stats():
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE) as f:
                s.stats.update(json.load(f))
    except: pass

def save_stats():
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(s.stats, f)
    except: pass

def rating(ms):
    """Get rating text and color based on reaction time."""
    if ms < 180: return "LEGENDARY", C.AMBER
    if ms < 220: return "ELITE", C.GREEN
    if ms < 280: return "FAST", C.ORANGE_BRIGHT
    if ms < 350: return "GOOD", C.ORANGE
    return "KEEP GOING", C.RED

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INIT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def init():
    global model, cap
    print("  ⏳ Loading pose estimation model...")
    try:
        model = YOLO(MODEL_PATH)
        print("  ✅ Model loaded successfully")
    except Exception as e:
        print(f"  ❌ Model error: {e}")
        return False
    
    print("  ⏳ Initializing camera...")
    try:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        print("  ✅ Camera initialized")
        load_stats()
        print("  ✅ Stats loaded\n")
        return True
    except Exception as e:
        print(f"  ❌ Camera error: {e}")
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# POSE DETECTION - Track both wrists with Kalman filtering
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_wrists(results):
    """
    Get both wrist positions and depth scale from pose results.
    Returns: (left_pos, right_pos, left_scale, right_scale)
    Scale is shoulder-to-wrist distance as a proxy for depth.
    """
    try:
        if not results or len(results) == 0:
            return None, None, None, None
        if results[0].keypoints is None or results[0].keypoints.data is None:
            return None, None, None, None
        
        kp = results[0].keypoints.data.cpu().numpy()
        if kp.shape[0] == 0 or kp.shape[1] < 11:
            return None, None, None, None
        kp = kp[0]
        
        # Keypoint indices (YOLO pose model)
        # 5 = left shoulder, 6 = right shoulder
        # 9 = left wrist, 10 = right wrist
        
        left_wrist = kp[9, :2]   # Left wrist
        right_wrist = kp[10, :2]  # Right wrist
        left_shoulder = kp[5, :2]  # Left shoulder
        right_shoulder = kp[6, :2]  # Right shoulder
        
        # Check validity
        left_valid = not np.all(left_wrist == 0) and not np.all(left_shoulder == 0)
        right_valid = not np.all(right_wrist == 0) and not np.all(right_shoulder == 0)
        
        # Calculate scale (shoulder-to-wrist distance) as depth proxy
        left_scale = None
        right_scale = None
        
        if left_valid:
            left_scale = np.linalg.norm(left_wrist - left_shoulder)
        if right_valid:
            right_scale = np.linalg.norm(right_wrist - right_shoulder)
        
        return (
            left_wrist if left_valid else None,
            right_wrist if right_valid else None,
            left_scale,
            right_scale
        )
    except:
        return None, None, None, None

def update_kalman(left_raw, right_raw, left_scale=None, right_scale=None):
    """Update Kalman filters with raw wrist positions and scale, return smoothed."""
    left_smooth = kf_left.update(left_raw)
    right_smooth = kf_right.update(right_raw)
    
    # Update scale trackers for depth detection
    if left_scale is not None:
        scale_tracker_left.update(left_scale)
    if right_scale is not None:
        scale_tracker_right.update(right_scale)
    
    return left_smooth, right_smooth

def calibrate_baseline():
    """Set current Kalman-filtered positions and scales as baseline."""
    left_pos = kf_left.get_position()
    right_pos = kf_right.get_position()
    left_scale = scale_tracker_left.get_scale()
    right_scale = scale_tracker_right.get_scale()
    
    if left_pos is not None:
        s.baseline_left = left_pos.copy()
    if right_pos is not None:
        s.baseline_right = right_pos.copy()
    if left_scale is not None:
        s.baseline_scale_left = left_scale
    if right_scale is not None:
        s.baseline_scale_right = right_scale
    
    s.calibrated = (s.baseline_left is not None or s.baseline_right is not None)

def detect_punch():
    """
    Detect punch by checking both wrists for movement.
    Detects both lateral (side-to-side) and forward (toward camera) punches.
    - Lateral: 2D position change
    - Forward: Scale increase (shoulder-to-wrist distance increases as hand moves closer)
    """
    if not s.calibrated:
        s.move_frames = 0
        return False
    
    max_dist = 0
    max_vel = 0
    max_scale_change = 0
    
    # Check left wrist
    if s.baseline_left is not None and kf_left.initialized:
        pos = kf_left.get_position()
        vel = kf_left.get_velocity()
        dist = np.linalg.norm(pos - s.baseline_left)
        max_dist = max(max_dist, dist)
        max_vel = max(max_vel, vel)
        
        # Check forward movement (scale increase)
        if s.baseline_scale_left is not None:
            current_scale = scale_tracker_left.get_scale()
            if current_scale is not None and s.baseline_scale_left > 0:
                # Scale increase indicates forward movement
                scale_change = (current_scale - s.baseline_scale_left) / s.baseline_scale_left
                max_scale_change = max(max_scale_change, scale_change)
    
    # Check right wrist
    if s.baseline_right is not None and kf_right.initialized:
        pos = kf_right.get_position()
        vel = kf_right.get_velocity()
        dist = np.linalg.norm(pos - s.baseline_right)
        max_dist = max(max_dist, dist)
        max_vel = max(max_vel, vel)
        
        # Check forward movement (scale increase)
        if s.baseline_scale_right is not None:
            current_scale = scale_tracker_right.get_scale()
            if current_scale is not None and s.baseline_scale_right > 0:
                # Scale increase indicates forward movement
                scale_change = (current_scale - s.baseline_scale_right) / s.baseline_scale_right
                max_scale_change = max(max_scale_change, scale_change)
    
    # Forward punch threshold: 15-25% scale increase (hand moved significantly closer)
    # Adjust based on sensitivity
    forward_threshold = 0.15 + (s.sensitivity - 3) * 0.02  # 0.11 to 0.19 range
    
    # Trigger if:
    # 1. Lateral movement (2D distance or velocity)
    # 2. Forward movement (scale increase > threshold)
    has_punch = (
        (max_dist > s.punch_distance) or 
        (max_vel > s.punch_velocity) or
        (max_scale_change > forward_threshold)
    )
    
    if has_punch:
        s.move_frames += 1
    else:
        s.move_frames = max(0, s.move_frames - 1)  # Decay slowly
    
    return s.move_frames >= s.frames_required

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SESSION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def start_session():
    if s.show_replay or s.active:
        return
    threading.Thread(target=run_session, daemon=True).start()

def run_session():
    try:
        with lock:
            s.active = True
            s.cue_on = False
            s.result_ms = None
            s.move_frames = 0
            s.buffer.clear()
            s.cue_idx = -1
            s.calibrated = False
            s.baseline_left = None
            s.baseline_right = None
            s.baseline_scale_left = None
            s.baseline_scale_right = None
            # Reset Kalman filters and scale trackers for fresh tracking
            kf_left.reset()
            kf_right.reset()
            scale_tracker_left.reset()
            scale_tracker_right.reset()
        
        s.stats["attempts"] += 1
        
        # Countdown - calibrate during LAST second
        s.phase = "countdown"
        for i in range(COUNTDOWN_SECS, 0, -1):
            if s.exit: return
            s.countdown = i
            
            if i == 1:
                # Last second: wait then calibrate at the very end
                time.sleep(0.8)
                calibrate_baseline()  # Capture baseline right before action
                time.sleep(0.2)
            else:
                time.sleep(1)
        
        if not s.calibrated:
            print("  ⚠️  Calibration failed - no pose detected. Please stay visible.")
            with lock:
                s.active = False
                s.phase = "idle"
            return
        
        # Random wait
        s.phase = "waiting"
        time.sleep(random.uniform(*CUE_DELAY))
        if s.exit: return
        
        # GO!
        s.phase = "cue"
        with lock:
            s.cue_on = True
            s.cue_time = time.time()
            s.cue_idx = len(s.buffer)
        
        # Wait for punch
        t0 = time.time()
        while s.cue_on and not s.exit:
            if time.time() - t0 > MAX_REACTION:
                with lock:
                    s.cue_on = False
                    s.active = False
                    s.phase = "idle"
                    build_replay()
                save_stats()
                return
            time.sleep(0.008)
        
        with lock:
            build_replay()
        
    except Exception as e:
        print(f"Session error: {e}")
        with lock:
            s.active = False
            s.cue_on = False
            s.phase = "idle"

def build_replay():
    """Extract frames around the cue moment."""
    s.replay_data = []
    buf = list(s.buffer)
    if not buf or s.cue_idx < 0:
        return
    
    start = max(0, s.cue_idx - REPLAY_PRE)
    end = min(len(buf), s.cue_idx + REPLAY_POST)
    
    for i in range(start, end):
        is_go = (i >= s.cue_idx)
        s.replay_data.append((buf[i].copy(), is_go))

def finish_punch(ms):
    with lock:
        s.cue_on = False
        s.result_ms = ms
        s.phase = "result"
    
    r, _ = rating(ms)
    print(f"  🥊 Punch! {ms:.0f}ms → {r}")
    
    s.stats["success"] += 1
    s.stats["times"].append(ms)
    s.stats["session"].append(ms)
    if ms < s.stats["best"]:
        s.stats["best"] = ms
    if len(s.stats["times"]) > 100:
        s.stats["times"] = s.stats["times"][-100:]
    save_stats()
    
    threading.Thread(target=reset_session, daemon=True).start()

def reset_session():
    time.sleep(2.5)
    with lock:
        s.active = False
        s.phase = "idle"
        s.calibrated = False
        s.move_frames = 0
        s.baseline_left = None
        s.baseline_right = None
        s.baseline_scale_left = None
        s.baseline_scale_right = None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UI DRAWING - Clean Minimal Overlay Design
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def draw_rounded_rect(img, x, y, w, h, radius, color, thickness=-1):
    """Draw a rectangle with rounded corners."""
    radius = min(radius, h // 2, w // 2)
    
    if thickness == -1:
        cv2.rectangle(img, (x + radius, y), (x + w - radius, y + h), color, -1)
        cv2.rectangle(img, (x, y + radius), (x + w, y + h - radius), color, -1)
        cv2.circle(img, (x + radius, y + radius), radius, color, -1)
        cv2.circle(img, (x + w - radius, y + radius), radius, color, -1)
        cv2.circle(img, (x + radius, y + h - radius), radius, color, -1)
        cv2.circle(img, (x + w - radius, y + h - radius), radius, color, -1)
    else:
        cv2.line(img, (x + radius, y), (x + w - radius, y), color, thickness)
        cv2.line(img, (x + radius, y + h), (x + w - radius, y + h), color, thickness)
        cv2.line(img, (x, y + radius), (x, y + h - radius), color, thickness)
        cv2.line(img, (x + w, y + radius), (x + w, y + h - radius), color, thickness)
        cv2.ellipse(img, (x + radius, y + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(img, (x + w - radius, y + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(img, (x + radius, y + h - radius), (radius, radius), 90, 0, 90, color, thickness)
        cv2.ellipse(img, (x + w - radius, y + h - radius), (radius, radius), 0, 0, 90, color, thickness)

def glass_panel(img, x, y, w, h, alpha=0.7):
    """Draw a translucent dark glass panel."""
    ov = img.copy()
    draw_rounded_rect(ov, x, y, w, h, 10, C.BLACK, -1)
    cv2.addWeighted(ov, alpha, img, 1 - alpha, 0, img)
    # Orange accent line at top
    cv2.line(img, (x + 10, y + 2), (x + w - 10, y + 2), C.ORANGE, 2)
    # Subtle border
    draw_rounded_rect(img, x, y, w, h, 10, C.DIM, 1)

def btn(img, x, y, w, h, text, active_color, hover=False, enabled=True):
    """Draw a clean minimal button."""
    ov = img.copy()
    font_scale = 0.6
    
    if not enabled:
        # Disabled state
        draw_rounded_rect(ov, x, y, w, h, 8, C.DIM, -1)
        cv2.addWeighted(ov, 0.5, img, 0.5, 0, img)
        sz = cv2.getTextSize(text, FONT_BOLD, font_scale, 1)[0]
        cv2.putText(img, text, (x + (w-sz[0])//2, y + (h+sz[1])//2 - 1), FONT_BOLD, font_scale, C.GRAY, 1, cv2.LINE_AA)
    else:
        if hover:
            # Hover - filled with color
            draw_rounded_rect(ov, x, y, w, h, 8, active_color, -1)
            cv2.addWeighted(ov, 0.9, img, 0.1, 0, img)
            sz = cv2.getTextSize(text, FONT_BOLD, font_scale, 1)[0]
            cv2.putText(img, text, (x + (w-sz[0])//2, y + (h+sz[1])//2 - 1), FONT_BOLD, font_scale, C.BLACK, 2, cv2.LINE_AA)
        else:
            # Normal - outline only
            draw_rounded_rect(ov, x, y, w, h, 8, C.DARK, -1)
            cv2.addWeighted(ov, 0.6, img, 0.4, 0, img)
            draw_rounded_rect(img, x, y, w, h, 8, active_color, 2)
            sz = cv2.getTextSize(text, FONT_BOLD, font_scale, 1)[0]
            cv2.putText(img, text, (x + (w-sz[0])//2, y + (h+sz[1])//2 - 1), FONT_BOLD, font_scale, active_color, 1, cv2.LINE_AA)
    
    return (x, y, w, h)

def text_center(img, text, y, font_scale, color, thickness=1):
    """Draw centered text."""
    sz = cv2.getTextSize(text, FONT, font_scale, thickness)[0]
    x = (img.shape[1] - sz[0]) // 2
    # Shadow
    cv2.putText(img, text, (x + 2, y + 2), FONT, font_scale, C.BLACK, thickness + 1, cv2.LINE_AA)
    cv2.putText(img, text, (x, y), FONT, font_scale, color, thickness, cv2.LINE_AA)

def draw_progress_bar(img, x, y, w, h, progress, fill_color):
    """Draw a simple progress bar."""
    # Background
    ov = img.copy()
    draw_rounded_rect(ov, x, y, w, h, h // 2, C.BLACK, -1)
    cv2.addWeighted(ov, 0.5, img, 0.5, 0, img)
    
    # Fill
    fill_w = max(h, int(w * progress))
    if progress > 0:
        draw_rounded_rect(img, x, y, fill_w, h, h // 2, fill_color, -1)

def in_rect(mx, my, r):
    if not r: return False
    x, y, w, h = r
    return x <= mx <= x+w and y <= my <= y+h

def add_vignette(img, strength=0.4):
    """Add subtle vignette effect to frame edges."""
    h, w = img.shape[:2]
    
    # Create vignette mask
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)
    mask = 1 - np.sqrt(X**2 + Y**2) * strength
    mask = np.clip(mask, 0.3, 1)
    
    # Apply to each channel
    for i in range(3):
        img[:, :, i] = (img[:, :, i] * mask).astype(np.uint8)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UI SECTIONS - Clean Minimal Overlay Design
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def draw_top_bar(f, w, h):
    """Draw minimal top overlay bar."""
    # Gradient fade from top
    for i in range(80):
        alpha = 0.8 * (1 - i / 80)
        ov = f.copy()
        cv2.line(ov, (0, i), (w, i), C.BLACK, 1)
        cv2.addWeighted(ov, alpha, f, 1 - alpha, 0, f)
    
    if s.phase == "countdown":
        # Logo left
        cv2.putText(f, "BOXBUNNY", (30, 50), FONT_BOLD, 0.9, C.ORANGE, 2, cv2.LINE_AA)
        
        # Big countdown circle - centered in upper area
        circle_x, circle_y = w // 2, h // 3
        circle_r = 80
        
        # Draw circle with glow effect
        for i in range(3):
            glow_r = circle_r + (3 - i) * 8
            glow_alpha = 0.15 - i * 0.04
            ov = f.copy()
            cv2.circle(ov, (circle_x, circle_y), glow_r, C.ORANGE, -1)
            cv2.addWeighted(ov, glow_alpha, f, 1 - glow_alpha, 0, f)
        
        # Circle background and border
        cv2.circle(f, (circle_x, circle_y), circle_r, C.BLACK, -1)
        cv2.circle(f, (circle_x, circle_y), circle_r, C.ORANGE, 4)
        
        # Center the number in the circle - much bigger
        num = str(s.countdown)
        sz = cv2.getTextSize(num, FONT_BOLD, 4.0, 5)[0]
        num_x = circle_x - sz[0] // 2
        num_y = circle_y + sz[1] // 2
        cv2.putText(f, num, (num_x, num_y), FONT_BOLD, 4.0, C.WHITE, 5, cv2.LINE_AA)
        
        # Status text below circle
        status = "HOLD STILL" if s.countdown == 1 else "GET READY"
        text_center(f, status, circle_y + circle_r + 50, 1.0, C.ORANGE, 2)
        
    elif s.phase == "waiting":
        # Pulsing warning - bigger and more visible
        pulse = 0.5 + 0.5 * math.sin(time.time() * 5)
        col = tuple(int(c * (0.5 + pulse * 0.5)) for c in C.RED)
        
        dots = "." * (int(time.time() * 3) % 4)
        text_center(f, f"WAIT{dots}", 55, 1.6, col, 3)
        
    elif s.phase == "cue":
        # Flash green border
        pulse = int(time.time() * 10) % 2
        thickness = 10 + pulse * 5
        cv2.rectangle(f, (0, 0), (w, h), C.GREEN, thickness)
        
        # Big GO - larger
        text_center(f, "GO!", h // 2 + 20, 4.0, C.GREEN, 5)
        
    else:
        # Idle - clean branding
        cv2.putText(f, "BOXBUNNY", (30, 45), FONT_BOLD, 0.9, C.ORANGE, 2, cv2.LINE_AA)
        
        # Hints - larger and more readable
        cv2.putText(f, "[SPACE] Start", (w - 450, 35), FONT, 0.5, C.LIGHT, 1, cv2.LINE_AA)
        cv2.putText(f, "[R] Replay", (w - 320, 35), FONT, 0.5, C.LIGHT, 1, cv2.LINE_AA)
        cv2.putText(f, "[G] Settings", (w - 200, 35), FONT, 0.5, C.LIGHT, 1, cv2.LINE_AA)
        cv2.putText(f, "[Q] Quit", (w - 80, 35), FONT, 0.5, C.GRAY, 1, cv2.LINE_AA)

def draw_stats(f, w, h):
    """Draw floating stats overlay in corner."""
    if not s.show_stats or s.phase != "idle":
        return
    
    px, py = w - 220, 85
    pw, ph = 200, 130
    
    glass_panel(f, px, py, pw, ph, 0.8)
    
    # Values
    best = f"{s.stats['best']:.0f}" if s.stats['best'] != float('inf') else "---"
    avg = f"{sum(s.stats['times'])/len(s.stats['times']):.0f}" if s.stats['times'] else "---"
    cnt = str(len(s.stats['session']))
    
    # Title - larger
    cv2.putText(f, "STATISTICS", (px + 15, py + 28), FONT_BOLD, 0.6, C.ORANGE, 1, cv2.LINE_AA)
    cv2.line(f, (px + 15, py + 38), (px + pw - 15, py + 38), C.DIM, 1)
    
    # Stats rows - larger text
    cv2.putText(f, "Best", (px + 15, py + 65), FONT, 0.55, C.GRAY, 1, cv2.LINE_AA)
    cv2.putText(f, f"{best} ms", (px + pw - 85, py + 65), FONT_BOLD, 0.6, C.GREEN, 1, cv2.LINE_AA)
    
    cv2.putText(f, "Average", (px + 15, py + 92), FONT, 0.55, C.GRAY, 1, cv2.LINE_AA)
    cv2.putText(f, f"{avg} ms", (px + pw - 85, py + 92), FONT_BOLD, 0.6, C.ORANGE, 1, cv2.LINE_AA)
    
    cv2.putText(f, "Session", (px + 15, py + 119), FONT, 0.55, C.GRAY, 1, cv2.LINE_AA)
    cv2.putText(f, cnt, (px + pw - 50, py + 119), FONT_BOLD, 0.6, C.LIGHT, 1, cv2.LINE_AA)

def draw_settings(f, w, h):
    """Draw sensitivity settings panel."""
    global btn_sens_up, btn_sens_down
    
    if not s.show_settings or s.phase != "idle":
        btn_sens_up = btn_sens_down = None
        return
    
    # Panel on left side
    px, py = 20, 85
    pw, ph = 220, 180
    
    glass_panel(f, px, py, pw, ph, 0.85)
    
    # Title
    cv2.putText(f, "SENSITIVITY", (px + 15, py + 28), FONT_BOLD, 0.6, C.ORANGE, 1, cv2.LINE_AA)
    cv2.line(f, (px + 15, py + 38), (px + pw - 15, py + 38), C.DIM, 1)
    
    # Sensitivity level display
    level_names = {1: "VERY HIGH", 2: "HIGH", 3: "MEDIUM", 4: "LOW", 5: "VERY LOW"}
    level_name = level_names[s.sensitivity]
    
    # Level indicator bar
    bar_x, bar_y = px + 20, py + 55
    bar_w, bar_h = pw - 40, 12
    
    # Background bar
    cv2.rectangle(f, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), C.DIM, -1)
    
    # Filled portion (inverted: 1 = full, 5 = minimal)
    fill_ratio = (6 - s.sensitivity) / 5
    fill_w = int(bar_w * fill_ratio)
    if fill_w > 0:
        # Color gradient from green (sensitive) to orange (less sensitive)
        if s.sensitivity <= 2:
            col = C.GREEN
        elif s.sensitivity == 3:
            col = C.ORANGE
        else:
            col = C.ORANGE_DIM
        cv2.rectangle(f, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), col, -1)
    
    # Level name
    sz = cv2.getTextSize(level_name, FONT_BOLD, 0.7, 2)[0]
    cv2.putText(f, level_name, (px + (pw - sz[0]) // 2, py + 92), FONT_BOLD, 0.7, C.WHITE, 2, cv2.LINE_AA)
    
    # +/- Buttons
    btn_w, btn_h = 50, 35
    btn_y = py + 105
    
    btn_sens_down = btn(f, px + 30, btn_y, btn_w, btn_h, "-", C.ORANGE, s.hover == "sens_down", s.sensitivity < 5)
    btn_sens_up = btn(f, px + pw - 80, btn_y, btn_w, btn_h, "+", C.ORANGE, s.hover == "sens_up", s.sensitivity > 1)
    
    # Current values (smaller, informational)
    cv2.putText(f, f"Distance: {s.punch_distance}", (px + 15, py + 158), FONT, 0.4, C.GRAY, 1, cv2.LINE_AA)
    cv2.putText(f, f"Velocity: {s.punch_velocity}", (px + 115, py + 158), FONT, 0.4, C.GRAY, 1, cv2.LINE_AA)
    
    # Help text
    cv2.putText(f, "Higher = triggers easier", (px + 15, py + 175), FONT, 0.35, C.DIM, 1, cv2.LINE_AA)

def draw_replay(f, w, h):
    """Draw compact replay overlay."""
    if not s.show_replay or not s.replay_data:
        return
    
    if s.replay_idx >= len(s.replay_data):
        s.replay_idx = 0
    
    frame_data, is_go = s.replay_data[s.replay_idx]
    s.replay_idx += 1
    
    # Replay in bottom-left - larger
    pw, ph = 240, 140
    px, py = 25, h - ph - 90
    
    col = C.GREEN if is_go else C.RED
    
    glass_panel(f, px - 8, py - 35, pw + 16, ph + 65, 0.8)
    
    # Title - larger
    cv2.putText(f, "REPLAY", (px, py - 12), FONT_BOLD, 0.6, C.ORANGE, 1, cv2.LINE_AA)
    
    # Status - larger
    status = "GO!" if is_go else "WAIT"
    sz = cv2.getTextSize(status, FONT_BOLD, 0.6, 1)[0]
    cv2.putText(f, status, (px + pw - sz[0], py - 12), FONT_BOLD, 0.6, col, 1, cv2.LINE_AA)
    
    # Video
    small = cv2.resize(frame_data, (pw, ph))
    f[py:py + ph, px:px + pw] = small
    cv2.rectangle(f, (px, py), (px + pw, py + ph), col, 2)
    
    # Progress
    prog = s.replay_idx / len(s.replay_data)
    bar_y = py + ph + 10
    draw_progress_bar(f, px, bar_y, pw, 8, prog, col)

def draw_result(f, w, h):
    """Draw clean centered result overlay."""
    if s.result_ms is None or s.phase != "result":
        return
    
    ms = s.result_ms
    r, col = rating(ms)
    
    # Darken entire frame
    ov = f.copy()
    cv2.rectangle(ov, (0, 0), (w, h), C.BLACK, -1)
    cv2.addWeighted(ov, 0.7, f, 0.3, 0, f)
    
    # Result card - even larger
    cw, ch = 500, 300
    cx, cy = (w - cw) // 2, (h - ch) // 2
    
    glass_panel(f, cx, cy, cw, ch, 0.9)
    
    # Accent line at top
    cv2.line(f, (cx + 30, cy + 12), (cx + cw - 30, cy + 12), col, 5)
    
    # Rating - bigger
    rsz = cv2.getTextSize(r, FONT_BOLD, 1.2, 2)[0]
    cv2.putText(f, r, (cx + (cw - rsz[0]) // 2, cy + 60), FONT_BOLD, 1.2, col, 2, cv2.LINE_AA)
    
    # Big time - much larger and centered
    time_str = f"{ms:.0f}"
    sz = cv2.getTextSize(time_str, FONT_BOLD, 5.5, 6)[0]
    tx = cx + (cw - sz[0]) // 2 - 25
    cv2.putText(f, time_str, (tx, cy + 180), FONT_BOLD, 5.5, C.WHITE, 6, cv2.LINE_AA)
    cv2.putText(f, "ms", (tx + sz[0] + 15, cy + 180), FONT, 1.5, C.GRAY, 2, cv2.LINE_AA)
    
    # Label
    text_center(f, "REACTION TIME", cy + 230, 0.7, C.GRAY)
    
    # Best comparison
    if s.stats['best'] != float('inf'):
        if ms <= s.stats['best']:
            text_center(f, "NEW BEST!", cy + 270, 0.8, C.GREEN)
        else:
            diff = ms - s.stats['best']
            text_center(f, f"+{diff:.0f}ms from best", cy + 270, 0.6, C.DIM)

def draw_punch_meter(f, w, h):
    """Show punch detection indicator."""
    if not s.cue_on:
        return
    
    prog = min(s.move_frames / s.frames_required, 1.0)
    col = C.GREEN if prog >= 1 else C.ORANGE
    
    # Bottom left indicator - larger
    px, py = 25, h - 85
    pw = 180
    
    glass_panel(f, px, py, pw, 45, 0.75)
    
    cv2.putText(f, "PUNCH DETECTION", (px + 12, py + 20), FONT, 0.5, col, 1, cv2.LINE_AA)
    draw_progress_bar(f, px + 12, py + 30, pw - 24, 8, prog, col)

def draw_controls(f, w, h):
    """Draw bottom control bar."""
    global btn_start, btn_replay, btn_settings, btn_quit
    
    # Gradient fade from bottom - taller
    for i in range(70):
        alpha = 0.75 * (i / 70)
        ov = f.copy()
        cv2.line(ov, (0, h - 70 + i), (w, h - 70 + i), C.BLACK, 1)
        cv2.addWeighted(ov, alpha, f, 1 - alpha, 0, f)
    
    # 4 centered buttons
    bw, bh = 115, 45
    gap = 20
    total_w = 4 * bw + 3 * gap
    start_x = (w - total_w) // 2
    y = h - 55
    
    can_start = not s.active and not s.show_replay
    btn_start = btn(f, start_x, y, bw, bh, "START", C.GREEN, s.hover == "start", can_start)
    
    has_replay = len(s.replay_data) > 0
    txt = "HIDE" if s.show_replay else "REPLAY"
    btn_replay = btn(f, start_x + bw + gap, y, bw, bh, txt, C.ORANGE, s.hover == "replay", has_replay and not s.active)
    
    # Settings button - shows current sensitivity level
    sens_txt = f"SENS {s.sensitivity}" if not s.show_settings else "CLOSE"
    btn_settings = btn(f, start_x + 2 * (bw + gap), y, bw, bh, sens_txt, C.AMBER, s.hover == "settings", not s.active)
    
    btn_quit = btn(f, start_x + 3 * (bw + gap), y, bw, bh, "QUIT", C.RED, s.hover == "quit", True)

def draw_ui(f, w, h, fps):
    """Compose all UI overlays on video."""
    draw_top_bar(f, w, h)
    draw_controls(f, w, h)
    
    # Floating overlays
    if s.show_replay and s.replay_data:
        draw_replay(f, w, h)
    
    if s.phase == "idle":
        draw_stats(f, w, h)
        draw_settings(f, w, h)
    
    draw_punch_meter(f, w, h)
    draw_result(f, w, h)
    
    # FPS in corner
    cv2.putText(f, f"{fps} fps", (w - 70, h - 75), FONT, 0.45, C.DIM, 1, cv2.LINE_AA)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def mouse(ev, x, y, fl, p):
    if ev == cv2.EVENT_MOUSEMOVE:
        s.hover = None
        if in_rect(x, y, btn_start): s.hover = "start"
        elif in_rect(x, y, btn_replay): s.hover = "replay"
        elif in_rect(x, y, btn_settings): s.hover = "settings"
        elif in_rect(x, y, btn_quit): s.hover = "quit"
        elif in_rect(x, y, btn_sens_up): s.hover = "sens_up"
        elif in_rect(x, y, btn_sens_down): s.hover = "sens_down"
    elif ev == cv2.EVENT_LBUTTONDOWN:
        if in_rect(x, y, btn_start) and not s.active:
            start_session()
        elif in_rect(x, y, btn_replay) and s.replay_data and not s.active:
            s.show_replay = not s.show_replay
            s.replay_idx = 0
        elif in_rect(x, y, btn_settings) and not s.active:
            s.show_settings = not s.show_settings
        elif in_rect(x, y, btn_quit):
            s.exit = True
        elif in_rect(x, y, btn_sens_up) and s.sensitivity > 1:
            update_sensitivity(s.sensitivity - 1)
        elif in_rect(x, y, btn_sens_down) and s.sensitivity < 5:
            update_sensitivity(s.sensitivity + 1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    if not init():
        return
    
    cv2.namedWindow("BoxBunny", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("BoxBunny", CAM_W, CAM_H)
    cv2.setMouseCallback("BoxBunny", mouse)
    
    print("\n" + "─" * 38)
    print("  🥊 BOXBUNNY - Reaction Trainer")
    print("─" * 38)
    print("  SPACE   Start")
    print("  R       Replay")
    print("  G       Settings (sensitivity)")
    print("  +/-     Adjust sensitivity")
    print("  Q       Quit")
    print("─" * 38 + "\n")
    
    fps_t, fps_c, fps = time.time(), 0, 0
    replay_t = time.time()
    
    try:
        while not s.exit:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            
            frame = cv2.flip(frame, 1)
            
            # Run pose detection
            try:
                results = model(frame, verbose=False)
                frame = results[0].plot()
                
                left_raw, right_raw, left_scale, right_scale = get_wrists(results)
                update_kalman(left_raw, right_raw, left_scale, right_scale)
                
                if s.active:
                    s.buffer.append(frame.copy())
                    if s.cue_on and detect_punch():
                        finish_punch((time.time() - s.cue_time) * 1000)
            except:
                pass
            
            # FPS counter
            fps_c += 1
            if time.time() - fps_t >= 1:
                fps = fps_c
                fps_c = 0
                fps_t = time.time()
            
            # Replay timing
            if s.show_replay and s.replay_data:
                if time.time() - replay_t >= REPLAY_SPEED:
                    replay_t = time.time()
                else:
                    s.replay_idx = max(0, s.replay_idx - 1)
            
            # Full-screen video - resize to fill canvas
            canvas = cv2.resize(frame, (CAM_W, CAM_H))
            
            # Add subtle vignette for depth
            add_vignette(canvas, 0.3)
            
            # Draw all UI overlays on top
            draw_ui(canvas, CAM_W, CAM_H, fps)
            
            cv2.imshow("BoxBunny", canvas)
            
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q'), 27]: 
                s.exit = True
            elif key == ord(' ') and not s.active: 
                start_session()
            elif key == ord('r') and s.replay_data and not s.active:
                s.show_replay = not s.show_replay
                s.replay_idx = 0
            elif key == ord('s'): 
                s.show_stats = not s.show_stats
            elif key == ord('g') and not s.active:
                s.show_settings = not s.show_settings
            elif key in [ord('+'), ord('='), 82] and not s.active:  # + key or up arrow
                if s.sensitivity > 1:
                    update_sensitivity(s.sensitivity - 1)
            elif key in [ord('-'), ord('_'), 84] and not s.active:  # - key or down arrow
                if s.sensitivity < 5:
                    update_sensitivity(s.sensitivity + 1)
    
    except KeyboardInterrupt:
        pass
    finally:
        save_stats()
        cap.release()
        cv2.destroyAllWindows()
        
        print("\n" + "─" * 38)
        if s.stats['session']:
            t = s.stats['session']
            print(f"  Session: {len(t)} attempts")
            print(f"  Best: {min(t):.0f}ms | Avg: {sum(t)/len(t):.0f}ms")
        print("  Goodbye!")
        print("─" * 38 + "\n")

if __name__ == "__main__":
    main()
