"""Combo detection module using YOLO pose estimation.

This module provides backend functionality for detecting and analyzing
punch combinations (specifically "1-1-2") through pose estimation.
Designed for GUI integration without any UI components.

Architecture matches reaction_time_runner.py pattern.
"""

import os
import time
import cv2
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, List

try:
    from ultralytics import YOLO
except ImportError as e:
    raise ImportError(f"Failed to import ultralytics (YOLO): {e}")


# Assume model is in ../models/ directory
ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "yolo11s-pose.pt"


@dataclass
class ComboResult:
    """Structured result from combo detection."""
    success: bool
    successful_punches: int = 0
    total_expected: int = 5
    video_path: Optional[str] = None
    punch_timings: List[float] = None  # Timestamps of detected punches
    status: Optional[str] = None  # "error", "timeout", or None if success
    error_message: Optional[str] = None


class ComboDetector:
    """Backend for combo detection using YOLO pose estimation."""
    
    def __init__(self, camera_index: int = 0, confidence_threshold: float = 0.3,
                 motion_threshold: float = 25.0, video_save_path: str = "/home/claude/combo_recording.mp4"):
        """Initialize the combo detector.
        
        Args:
            camera_index: Camera device index (default 0)
            confidence_threshold: Minimum keypoint confidence (0.0-1.0)
            motion_threshold: Pixel distance to detect punch motion (default 25.0)
            video_save_path: Path to save recorded video
        """
        self.camera_index = camera_index
        self.confidence_threshold = confidence_threshold
        self.motion_threshold = motion_threshold
        self.video_save_path = video_save_path
        self.cap: Optional[cv2.VideoCapture] = None
        self.model: Optional[YOLO] = None
        self.video_writer: Optional[cv2.VideoWriter] = None
        
        # Punch detection state
        self.punch_count = 0
        self.punch_timings = []
        self.last_punch_time = 0
        self.debounce_time = 0.5  # 500ms between punches
    
    def initialize_camera_and_model(self) -> Tuple[bool, Optional[str]]:
        """Initialize camera and load YOLO model with warmup.
        
        Performs:
        - Model loading
        - Camera initialization
        - 10 warmup frames for stability
        
        Returns:
            (success: bool, error_message: str | None)
        """
        try:
            # Check model exists
            if not MODEL_PATH.exists():
                return (False, f"Model file not found at: {MODEL_PATH}")
            
            # Load model
            self.model = YOLO(str(MODEL_PATH))
            
            # Open camera
            if os.name == "nt":
                self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            else:
                self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                return (False, "Cannot open camera. Check device index or permissions.")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Warmup frames
            for _ in range(10):
                ok, frame = self.cap.read()
                if not ok:
                    return (False, "Failed to read frames from camera.")
                
                frame = cv2.flip(frame, 1)
                try:
                    self.model(frame, verbose=False)
                except Exception as e:
                    return (False, f"Model inference failed during warmup: {e}")
            
            return (True, None)
        
        except Exception as e:
            return (False, f"Initialization failed: {str(e)}")
    
    def start_recording(self) -> Tuple[bool, Optional[str]]:
        """Start video recording.
        
        Returns:
            (success: bool, error_message: str | None)
        """
        try:
            if self.cap is None:
                return (False, "Camera not initialized")
            
            # Get video properties
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(
                self.video_save_path,
                fourcc,
                fps,
                (width, height)
            )
            
            if not self.video_writer.isOpened():
                return (False, "Failed to create video writer")
            
            # Reset punch detection state
            self.punch_count = 0
            self.punch_timings = []
            self.last_punch_time = 0
            
            return (True, None)
        
        except Exception as e:
            return (False, f"Failed to start recording: {str(e)}")
    
    def detect_combo(self, duration_seconds: float = 15.0, 
                    expected_punches: int = 5) -> ComboResult:
        """Detect combo punches during the specified duration.
        
        Args:
            duration_seconds: How long to detect punches (default 15 seconds)
            expected_punches: Expected number of punches (default 5 for "1-1-2" repeated)
        
        Returns:
            ComboResult with detection details
        """
        if self.cap is None or self.model is None:
            return ComboResult(
                success=False, 
                status="error",
                error_message="Camera/model not initialized"
            )
        
        if self.video_writer is None:
            return ComboResult(
                success=False,
                status="error", 
                error_message="Recording not started"
            )
        
        try:
            start_time = time.time()
            prev_keypoints = None
            
            # Stabilize pose detection
            for _ in range(5):
                ok, frame = self.cap.read()
                if not ok:
                    return ComboResult(
                        success=False,
                        status="error",
                        error_message="Failed to read frame"
                    )
                
                frame = cv2.flip(frame, 1)
                results = self.model(frame, verbose=False)
                prev_keypoints = self._extract_keypoints(results)
                
                # Write frame to video
                self.video_writer.write(frame)
            
            # Main detection loop
            while time.time() - start_time < duration_seconds:
                ok, frame = self.cap.read()
                if not ok:
                    return ComboResult(
                        success=False,
                        status="error",
                        error_message="Failed to read frame"
                    )
                
                frame = cv2.flip(frame, 1)
                
                # Run pose estimation
                results = self.model(frame, verbose=False)
                curr_keypoints = self._extract_keypoints(results)
                
                # Detect punch motion
                if curr_keypoints is not None and prev_keypoints is not None:
                    motion = self._calculate_motion_magnitude(prev_keypoints, curr_keypoints)
                    
                    current_time = time.time()
                    time_since_last = current_time - self.last_punch_time
                    
                    # Detect punch with debounce
                    if motion > self.motion_threshold and time_since_last > self.debounce_time:
                        self.punch_count += 1
                        self.punch_timings.append(current_time - start_time)
                        self.last_punch_time = current_time
                        
                        # Draw visual feedback on frame
                        cv2.putText(
                            frame, 
                            f"PUNCH {self.punch_count}!", 
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.5,
                            (0, 255, 0),
                            3
                        )
                
                # Draw punch count on frame
                cv2.putText(
                    frame,
                    f"Punches: {self.punch_count}/{expected_punches}",
                    (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )
                
                # Write frame to video
                self.video_writer.write(frame)
                prev_keypoints = curr_keypoints
            
            # Detection complete
            return ComboResult(
                success=True,
                successful_punches=min(self.punch_count, expected_punches),
                total_expected=expected_punches,
                video_path=self.video_save_path,
                punch_timings=self.punch_timings.copy()
            )
        
        except Exception as e:
            return ComboResult(
                success=False,
                status="error",
                error_message=f"Detection failed: {str(e)}"
            )
    
    def stop_recording(self) -> bool:
        """Stop video recording and release resources.
        
        Returns:
            success: bool
        """
        try:
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None
            return True
        except Exception:
            return False
    
    def cleanup(self):
        """Release all resources."""
        self.stop_recording()
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    @staticmethod
    def _calculate_motion_magnitude(prev_keypoints, curr_keypoints,
                                   confidence_threshold: float = 0.3) -> float:
        """Calculate max distance moved by any keypoint.
        
        Focuses on wrist keypoints (indices 9, 10) for punch detection.
        
        Args:
            prev_keypoints: Previous frame keypoints
            curr_keypoints: Current frame keypoints
            confidence_threshold: Minimum confidence to consider
        
        Returns:
            Maximum Euclidean distance moved by wrists
        """
        if prev_keypoints is None or curr_keypoints is None:
            return 0.0
        
        # Focus on wrist keypoints: 9 (L wrist), 10 (R wrist)
        wrist_indices = [9, 10]
        max_distance = 0.0
        
        for idx in wrist_indices:
            if idx >= len(prev_keypoints) or idx >= len(curr_keypoints):
                continue
            
            prev_pt = prev_keypoints[idx]
            curr_pt = curr_keypoints[idx]
            
            # Check confidence (3rd value)
            if len(prev_pt) >= 3 and len(curr_pt) >= 3:
                if prev_pt[2] < confidence_threshold or curr_pt[2] < confidence_threshold:
                    continue
            
            # Calculate Euclidean distance
            distance = np.sqrt((curr_pt[0] - prev_pt[0])**2 + (curr_pt[1] - prev_pt[1])**2)
            max_distance = max(max_distance, distance)
        
        return max_distance
    
    @staticmethod
    def _extract_keypoints(results):
        """Extract keypoints from YOLO results.
        
        Returns:
            Keypoints array for first person or None
        """
        if not results or len(results) == 0:
            return None
        kps = results[0].keypoints
        if kps is None or kps.data is None:
            return None
        arr = kps.data.cpu().numpy()
        if arr.shape[0] == 0:
            return None
        return arr[0]  # Return keypoints for first person


# ============================================================================
# GLOBAL INSTANCE FOR GUI INTEGRATION
# ============================================================================

_detector: Optional[ComboDetector] = None


def initialize_camera_and_model(camera_index: int = 0,
                                video_path: str = "/home/claude/combo_recording.mp4") -> Tuple[bool, Optional[str]]:
    """Initialize camera and model (global instance).
    
    Args:
        camera_index: Camera device index
        video_path: Path to save recorded video
    
    Returns:
        (success: bool, error_message: str | None)
    """
    global _detector
    _detector = ComboDetector(camera_index=camera_index, video_save_path=video_path)
    return _detector.initialize_camera_and_model()


def start_recording() -> Tuple[bool, Optional[str]]:
    """Start video recording using global instance.
    
    Returns:
        (success: bool, error_message: str | None)
    """
    global _detector
    if _detector is None:
        return (False, "Detector not initialized")
    return _detector.start_recording()


def detect_combo(duration_seconds: float = 15.0,
                expected_punches: int = 5) -> ComboResult:
    """Detect combo punches using global instance.
    
    Args:
        duration_seconds: How long to detect punches
        expected_punches: Expected number of punches
    
    Returns:
        ComboResult with detection details
    """
    global _detector
    if _detector is None:
        return ComboResult(
            success=False,
            status="error",
            error_message="Detector not initialized"
        )
    return _detector.detect_combo(duration_seconds, expected_punches)


def stop_recording() -> bool:
    """Stop recording using global instance.
    
    Returns:
        success: bool
    """
    global _detector
    if _detector is None:
        return False
    return _detector.stop_recording()


def cleanup():
    """Cleanup resources."""
    global _detector
    if _detector is not None:
        _detector.cleanup()
        _detector = None


# ============================================================================
# PLACEHOLDER COMBO DETECTION (for testing)
# ============================================================================

def detect_combo_continuous(callback, interval_seconds: float = 3.0) -> None:
    """Placeholder: Continuously detect combos and call callback on success.
    
    This is a placeholder function that simulates successful combo detection
    every `interval_seconds` by printing JSON and calling the callback.
    
    Args:
        callback: Function to call when combo is detected (receives 'successful' string)
        interval_seconds: Time between simulated detections (default 3.0)
    
    Note: This runs in the caller's thread - should be called from a worker thread.
    """
    import json
    start_time = time.time()
    combo_count = 0
    max_combos = 3  # We need 3 successful combos
    
    while combo_count < max_combos:
        time.sleep(interval_seconds)
        combo_count += 1
        # Print JSON output for successful combo detection
        print(json.dumps({"status": "successful", "combo": "1-1-2", "count": combo_count}))
        callback("successful")
    
    return
