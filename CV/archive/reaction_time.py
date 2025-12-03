"""
BoxBunny Reaction Time Tester - Integrated Video UI
--------------------------------------------------
Requirements:
- models/yolo11n-pose.pt must exist
- Press 'q' to exit or click Quit button
"""

import cv2
import numpy as np
import time
import random
import threading
from ultralytics import YOLO
import sys
import os

# Disable OpenCV threading for stability
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# ---------------- CONFIG ----------------
MODEL_PATH = "models/yolo11s-pose.pt"
GET_READY_TIME = 3
CUE_DELAY_RANGE = (2, 5)
MOVEMENT_THRESHOLD = 0.80  # Much higher - need significant movement
FRAME_MOVEMENT_THRESHOLD = 0.60  # Much higher - need fast movement
CONSECUTIVE_FRAMES_REQUIRED = 8  # Must detect movement for 5 frames
MOVEMENT_RESET_THRESHOLD = 1  # Allow 2 frames gap before resetting
WINDOW_NAME = "BoxBunny Reaction Tester"
MAX_REACTION_TIME = 5.0
CAMERA_WIDTH = 1280  
CAMERA_HEIGHT = 720

# ---------------- GLOBALS ----------------
session_active = False
cue_active = False
cue_start_time = None
reaction_time = None
prev_wrist_pos = None
exit_program = False
session_lock = threading.Lock()
baseline_wrist_pos = None
calibration_frames = []
is_calibrated = False
test_result_time = None
countdown_timer = 0
current_phase = "idle"
button_hover = None
movement_frames = 0  # Track consecutive frames with movement
frames_without_movement = 0  # Track frames without movement

model = None
cap = None
font = cv2.FONT_HERSHEY_SIMPLEX

# Button definitions (x, y, width, height)
start_button = None
quit_button = None


# ---------------- INITIALIZATION ----------------
def initialize():
    """Initialize model and camera with error handling."""
    global model, cap
    
    try:
        print(f"Loading YOLO model from: {MODEL_PATH}")
        model = YOLO(MODEL_PATH)
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return False
    
    try:
        print("Opening camera...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Could not open camera")
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, 30)
        print("✓ Camera opened successfully")
        return True
    except Exception as e:
        print(f"Error opening camera: {e}")
        return False


# ---------------- HELPERS ----------------
def get_wrist_position(results):
    """Return mean of left/right wrist coords with validation."""
    try:
        if not results or len(results) == 0:
            return None
        
        if results[0].keypoints is None or results[0].keypoints.data is None:
            return None
        
        arr = results[0].keypoints.data.cpu().numpy()
        if arr.shape[0] == 0 or len(arr.shape) < 3:
            return None
        
        kp = arr[0]
        if kp.shape[0] < 11:
            return None
        
        left_wrist = kp[9, :2]
        right_wrist = kp[10, :2]
        
        if np.all(left_wrist == 0) and np.all(right_wrist == 0):
            return None
        
        if np.all(left_wrist == 0):
            return right_wrist
        elif np.all(right_wrist == 0):
            return left_wrist
        else:
            return np.mean([left_wrist, right_wrist], axis=0)
    
    except Exception as e:
        return None


def calibrate_baseline(wrist_pos):
    """Collect baseline wrist positions for better motion detection."""
    global calibration_frames, is_calibrated, baseline_wrist_pos
    
    if wrist_pos is None:
        return
    
    calibration_frames.append(wrist_pos.copy())
    
    if len(calibration_frames) > 30:
        calibration_frames.pop(0)
    
    if len(calibration_frames) >= 10:
        baseline_wrist_pos = np.mean(calibration_frames, axis=0)
        is_calibrated = True


def detect_punch(wrist_pos):
    """Detect significant wrist movement - requires sustained continuous movement."""
    global prev_wrist_pos, baseline_wrist_pos, movement_frames, frames_without_movement
    
    if wrist_pos is None or not is_calibrated:
        movement_frames = 0
        frames_without_movement = 0
        return False
    
    # Calculate movement from baseline position
    baseline_movement = np.linalg.norm(wrist_pos - baseline_wrist_pos)
    
    # Calculate movement from previous frame
    frame_movement = 0
    if prev_wrist_pos is not None:
        frame_movement = np.linalg.norm(wrist_pos - prev_wrist_pos)
    
    # Check if significant movement detected (BOTH conditions must be met)
    has_movement = (baseline_movement > MOVEMENT_THRESHOLD and 
                   frame_movement > FRAME_MOVEMENT_THRESHOLD)
    
    if has_movement:
        movement_frames += 1
        frames_without_movement = 0
    else:
        frames_without_movement += 1
        # Allow small gap due to jitter, but reset if gap too large
        if frames_without_movement > MOVEMENT_RESET_THRESHOLD:
            movement_frames = 0
    
    # Only register punch after consecutive frames of sustained movement
    return movement_frames >= CONSECUTIVE_FRAMES_REQUIRED


def start_session():
    """Triggered by button click."""
    global session_active
    
    with session_lock:
        if session_active:
            return
        
        if not is_calibrated:
            print("Please wait, calibrating...")
            return
        
        threading.Thread(target=run_session, daemon=True).start()


def run_session():
    """Handles timing logic with countdown display."""
    global session_active, cue_active, cue_start_time, reaction_time, calibration_frames
    global test_result_time, countdown_timer, current_phase, movement_frames, frames_without_movement
    
    try:
        with session_lock:
            session_active = True
            cue_active = False
            reaction_time = None
            test_result_time = None
            calibration_frames = []
            movement_frames = 0  # Reset movement counter
            frames_without_movement = 0  # Reset gap counter
        
        print("\n=== NEW SESSION ===")
        
        # Countdown phase
        current_phase = "countdown"
        for i in range(GET_READY_TIME, 0, -1):
            if exit_program:
                return
            countdown_timer = i
            time.sleep(1)
        
        if exit_program:
            return
        
        # Waiting phase
        current_phase = "waiting"
        cue_delay = random.uniform(*CUE_DELAY_RANGE)
        print(f"Waiting {cue_delay:.1f}s before cue...")
        time.sleep(cue_delay)
        
        if exit_program:
            return
        
        # Cue phase
        current_phase = "cue"
        with session_lock:
            cue_active = True
            cue_start_time = time.time()
        
        print("🟢 CUE: PUNCH NOW!")
        
        # Wait for punch or timeout
        timeout_start = time.time()
        while cue_active and not exit_program:
            if time.time() - timeout_start > MAX_REACTION_TIME:
                with session_lock:
                    cue_active = False
                    session_active = False
                    current_phase = "idle"
                print("⏱️ Timeout - no punch detected")
                time.sleep(2)
                return
            time.sleep(0.05)
        
    except Exception as e:
        print(f"Error in session: {e}")
        with session_lock:
            session_active = False
            cue_active = False
            current_phase = "idle"


def draw_rounded_rect(frame, x, y, w, h, radius, color, thickness=-1):
    """Draw a rounded rectangle."""
    if thickness == -1:  # Filled
        cv2.rectangle(frame, (x + radius, y), (x + w - radius, y + h), color, -1)
        cv2.rectangle(frame, (x, y + radius), (x + w, y + h - radius), color, -1)
        cv2.circle(frame, (x + radius, y + radius), radius, color, -1)
        cv2.circle(frame, (x + w - radius, y + radius), radius, color, -1)
        cv2.circle(frame, (x + radius, y + h - radius), radius, color, -1)
        cv2.circle(frame, (x + w - radius, y + h - radius), radius, color, -1)
    else:  # Outline
        cv2.line(frame, (x + radius, y), (x + w - radius, y), color, thickness)
        cv2.line(frame, (x + radius, y + h), (x + w - radius, y + h), color, thickness)
        cv2.line(frame, (x, y + radius), (x, y + h - radius), color, thickness)
        cv2.line(frame, (x + w, y + radius), (x + w, y + h - radius), color, thickness)
        cv2.ellipse(frame, (x + radius, y + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(frame, (x + w - radius, y + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(frame, (x + radius, y + h - radius), (radius, radius), 90, 0, 90, color, thickness)
        cv2.ellipse(frame, (x + w - radius, y + h - radius), (radius, radius), 0, 0, 90, color, thickness)


def draw_button(frame, x, y, w, h, text, bg_color, text_color, is_hover=False):
    """Draw a styled button with hover effect."""
    if is_hover:
        # Lighter color on hover
        bg_color = tuple(min(c + 30, 255) for c in bg_color)
    
    draw_rounded_rect(frame, x, y, w, h, 10, bg_color, -1)
    
    # Add shadow effect
    shadow_offset = 2
    if not is_hover:
        shadow_color = (0, 0, 0)
        draw_rounded_rect(frame, x + shadow_offset, y + shadow_offset, w, h, 10, shadow_color, 2)
    
    # Draw text
    text_size = cv2.getTextSize(text, font, 0.7, 2)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2
    
    cv2.putText(frame, text, (text_x, text_y), font, 0.7, text_color, 2, cv2.LINE_AA)
    
    return (x, y, w, h)


def draw_ui_overlay(frame, w, h):
    """Draw UI elements on the frame with buttons."""
    global start_button, quit_button
    
    bar_height = 120
    
    # Status bar at top
    if current_phase == "countdown":
        color = (50, 159, 255)
        cv2.rectangle(frame, (0, 0), (w, bar_height), color, -1)
        text = f"GET READY: {countdown_timer}"
        text_color = (255, 255, 255)
        text_size = 1.8
        
    elif current_phase == "waiting":
        color = (79, 90, 238)
        cv2.rectangle(frame, (0, 0), (w, bar_height), color, -1)
        text = "WAIT FOR GREEN..."
        text_color = (255, 255, 255)
        text_size = 1.2
        
    elif current_phase == "cue":
        if int(time.time() * 4) % 2 == 0:
            cv2.rectangle(frame, (0, 0), (w, bar_height), (0, 255, 100), -1)
        else:
            cv2.rectangle(frame, (0, 0), (w, bar_height), (0, 255, 0), -1)
        text = "PUNCH NOW!!!"
        text_color = (255, 255, 255)
        text_size = 1.8
        
    else:
        # Header with title
        color = (30, 30, 46)
        cv2.rectangle(frame, (0, 0), (w, bar_height), color, -1)
        
        # Title
        title = "BoxBunny"
        emoji = "🥊"
        title_size = cv2.getTextSize(title, font, 1.5, 3)[0]
        title_x = (w - title_size[0]) // 2
        cv2.putText(frame, title, (title_x, 50), font, 1.5, (78, 205, 196), 3, cv2.LINE_AA)
        
        # Subtitle
        subtitle = "Reaction Time Tester"
        subtitle_size = cv2.getTextSize(subtitle, font, 0.6, 1)[0]
        subtitle_x = (w - subtitle_size[0]) // 2
        cv2.putText(frame, subtitle, (subtitle_x, 85), font, 0.6, (149, 225, 211), 1, cv2.LINE_AA)
        
        text = ""
        text_color = (255, 255, 255)
        text_size = 1.0
    
    # Draw status text if exists
    if text:
        text_x = 20
        text_y = 75
        cv2.putText(frame, text, (text_x + 3, text_y + 3), font, text_size, (0, 0, 0), 5)
        cv2.putText(frame, text, (text_x, text_y), font, text_size, text_color, 4)
    
    # Calibration status
    if not is_calibrated:
        cv2.putText(frame, "Calibrating... Stand still!", (20, h - 140), 
                    font, 0.8, (0, 200, 255), 2)
    
    # Show last reaction time in top right corner
    if reaction_time is not None and current_phase == "idle" and test_result_time is None:
        rt_text = f"Last: {reaction_time:.0f} ms"
        text_size = cv2.getTextSize(rt_text, font, 0.6, 1)[0]   # smaller font + thinner text
        text_x = w - text_size[0] - 15
        text_y = 40
        padding = 6                                              # smaller background box
        cv2.rectangle(frame, (text_x - padding, text_y - text_size[1] - padding),
                    (text_x + text_size[0] + padding, text_y + padding),
                    (30, 30, 46), -1)
        cv2.putText(frame, rt_text, (text_x, text_y),
                    font, 0.6, (0, 255, 150), 1)
    
    # Show result overlay (center of screen)
    if test_result_time is not None:
        result_text = f"{test_result_time:.0f} ms"
        text_width = cv2.getTextSize(result_text, font, 2.5, 4)[0][0]
        result_x = (w - text_width) // 2
        result_y = h // 2
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, result_y - 80), (w, result_y + 40), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(frame, result_text, (result_x, result_y), 
                    font, 2.5, (0, 255, 150), 4)
        
        label = "REACTION TIME"
        label_width = cv2.getTextSize(label, font, 0.8, 2)[0][0]
        label_x = (w - label_width) // 2
        cv2.putText(frame, label, (label_x, result_y - 40), 
                    font, 0.8, (200, 200, 200), 2)
    
    
    # Draw buttons at bottom
    button_y = h - 100
    button_width = 180
    button_height = 50
    button_spacing = 20
    
    # Start button (center-left)
    start_x = (w // 2) - button_width - (button_spacing // 2)
    start_button = draw_button(frame, start_x, button_y, button_width, button_height,
                               "START TEST", (78, 205, 196), (20, 20, 20),
                               button_hover == "start")
    
    # Quit button (center-right)
    quit_x = (w // 2) + (button_spacing // 2)
    quit_button = draw_button(frame, quit_x, button_y, button_width, button_height,
                              "QUIT", (231, 76, 60), (255, 255, 255),
                              button_hover == "quit")
    
    return frame


def mouse_callback(event, x, y, flags, param):
    """Handle mouse events for button clicks."""
    global button_hover, exit_program
    
    if event == cv2.EVENT_MOUSEMOVE:
        # Check if hovering over buttons
        if start_button and is_point_in_rect(x, y, start_button):
            button_hover = "start"
        elif quit_button and is_point_in_rect(x, y, quit_button):
            button_hover = "quit"
        else:
            button_hover = None
    
    elif event == cv2.EVENT_LBUTTONDOWN:
        # Check if clicked on buttons
        if start_button and is_point_in_rect(x, y, start_button):
            print("Start button clicked!")
            start_session()
        elif quit_button and is_point_in_rect(x, y, quit_button):
            print("Quit button clicked!")
            exit_program = True


def is_point_in_rect(x, y, rect):
    """Check if point (x, y) is inside rectangle (rx, ry, rw, rh)."""
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


def cleanup():
    """Clean up resources."""
    global cap, exit_program
    print("Cleaning up resources...")
    exit_program = True
    
    if cap is not None:
        cap.release()
    
    cv2.destroyAllWindows()


# ---------------- MAIN LOOP ----------------
def main():
    """Main application loop."""
    global prev_wrist_pos, cue_active, session_active, reaction_time, exit_program
    global test_result_time, current_phase, movement_frames, frames_without_movement
    
    print("=" * 50)
    print("BoxBunny Reaction Time Tester")
    print("=" * 50)
    
    if not initialize():
        sys.exit(1)
    
    # Create fullscreen window
    # cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(WINDOW_NAME, 1280, 720)
    # cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
    
    print("\n=== Camera feed started ===")
    print("Click START TEST button or press 'q' to quit\n")
    
    try:
        while not exit_program:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # Run pose detection
            results = model.predict(frame, imgsz=640, verbose=False)
            annotated = results[0].plot()
            
            # Get wrist position
            wrist_pos = get_wrist_position(results)
            
            # Calibration when idle
            if current_phase == "idle" and wrist_pos is not None:
                calibrate_baseline(wrist_pos)
            
            # Reset movement counter when not in cue phase
            if not cue_active:
                movement_frames = 0
                frames_without_movement = 0
            
            # Detect punch during active cue
            punch_detected = False
            if cue_active and wrist_pos is not None:
                punch_detected = detect_punch(wrist_pos)
            
            # Handle successful punch detection
            if cue_active and punch_detected:
                with session_lock:
                    reaction_time = (time.time() - cue_start_time) * 1000
                    test_result_time = reaction_time
                    current_phase = "result"
                    print(f"✓ Reaction time: {reaction_time:.0f} ms")
                    cue_active = False
                    session_active = False
                
                # Schedule result clear
                result_start = time.time()
            
            # Clear result after 2.5 seconds
            if test_result_time is not None and current_phase == "result":
                if time.time() - result_start > 2.5:
                    test_result_time = None
                    current_phase = "idle"
            
            # Update previous position
            prev_wrist_pos = wrist_pos.copy() if wrist_pos is not None else None
            
            # Draw UI overlay with buttons
            annotated = draw_ui_overlay(annotated, w, h)
            
            # Display frame
            cv2.imshow(WINDOW_NAME, annotated)
            
            # Check for 'q' key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        cleanup()


if __name__ == "__main__":
    main()