"""Reaction time measurement module using YOLO pose estimation.

This module provides backend functionality for measuring reaction time
by tracking user movements through pose estimation. Designed for GUI integration
without any UI components (no OpenCV displays or print statements).
"""

import os
import time
import random
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple

try:
    import cv2
    import numpy as np
except ImportError as e:
    raise ImportError(f"Failed to import OpenCV/NumPy: {e}")

try:
    from ultralytics import YOLO
except ImportError as e:
    raise ImportError(f"Failed to import ultralytics (YOLO): {e}")


ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT_DIR / "models" / "yolo11s-pose.pt"


@dataclass
class ReactionResult:
    """Structured result from reaction time measurement."""
    success: bool
    reaction_ms: Optional[float] = None
    status: Optional[str] = None  # "too_soon", "timeout", "error", or None if success
    error_message: Optional[str] = None


class ReactionTimeRunner:
    """Backend for reaction time measurement using YOLO pose estimation."""
    
    def __init__(self, camera_index: int = 0, confidence_threshold: float = 0.3, 
                 motion_threshold: float = 20.0):
        """Initialize the reaction time runner.
        
        Args:
            camera_index: Camera device index (default 0)
            confidence_threshold: Minimum keypoint confidence (0.0-1.0)
            motion_threshold: Pixel distance to detect motion (default 20.0)
        """
        self.camera_index = camera_index
        self.confidence_threshold = confidence_threshold
        self.motion_threshold = motion_threshold
        self.cap: Optional[cv2.VideoCapture] = None
        self.model: Optional[YOLO] = None
    
    def initialize_camera_and_model(self) -> Tuple[bool, Optional[str]]:
        """Initialize camera and load YOLO model with warmup.
        
        Performs:
        - Model loading
        - Camera initialization
        - 10 warmup frames for stability
        
        Returns:
            (success: bool, error_message: str | None)
            - (True, None) if successful
            - (False, error_str) if failed
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
    
    def measure_reaction_time(self) -> ReactionResult:
        """Measure reaction time after green signal.
        
        Called when the GUI shows "Punch Now!" (green screen).
        Assumes camera and model are already initialized.
        
        Returns:
            ReactionResult with reaction_ms, status, or error details
        """
        if self.cap is None or self.model is None:
            return ReactionResult(success=False, status="error", 
                                error_message="Camera/model not initialized")
        
        try:
            prev_keypoints = None
            
            # Stabilize pose detection with initial frames
            for _ in range(5):
                ok, frame = self.cap.read()
                if not ok:
                    return ReactionResult(success=False, status="error",
                                        error_message="Failed to read frame")
                
                frame = cv2.flip(frame, 1)
                try:
                    results = self.model(frame, verbose=False)
                    prev_keypoints = self._extract_keypoints(results)
                except Exception as e:
                    return ReactionResult(success=False, status="error",
                                        error_message=f"Inference failed: {e}")
            
            # Wait for punch with timeout of 2.5 seconds
            # (user should respond within this window after seeing "Punch Now!")
            punch_start_time = time.time()
            punch_detected = False
            timeout_seconds = 2.5
            
            while time.time() - punch_start_time < timeout_seconds:
                ok, frame = self.cap.read()
                if not ok:
                    return ReactionResult(success=False, status="error",
                                        error_message="Failed to read frame")
                
                frame = cv2.flip(frame, 1)
                
                try:
                    results = self.model(frame, verbose=False)
                    curr_keypoints = self._extract_keypoints(results)
                    
                    if curr_keypoints is not None and prev_keypoints is not None:
                        motion = self._calculate_motion_magnitude(prev_keypoints, 
                                                                 curr_keypoints)
                        if motion > self.motion_threshold:
                            punch_detected = True
                            reaction_time_ms = (time.time() - punch_start_time) * 1000
                            return ReactionResult(success=True, reaction_ms=reaction_time_ms)
                    
                    prev_keypoints = curr_keypoints
                except Exception as e:
                    return ReactionResult(success=False, status="error",
                                        error_message=f"Inference failed: {e}")
            
            if not punch_detected:
                return ReactionResult(success=False, status="timeout")
        
        except Exception as e:
            return ReactionResult(success=False, status="error",
                                error_message=f"Measurement failed: {str(e)}")
        
        finally:
            pass  # Keep camera open for potential reuse
    
    def cleanup(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    @staticmethod
    def _calculate_motion_magnitude(prev_keypoints, curr_keypoints, 
                                   confidence_threshold: float = 0.3) -> float:
        """Calculate max distance moved by any keypoint.
        
        Args:
            prev_keypoints: Previous frame keypoints
            curr_keypoints: Current frame keypoints
            confidence_threshold: Minimum confidence to consider
        
        Returns:
            Maximum Euclidean distance moved by any keypoint
        """
        if prev_keypoints is None or curr_keypoints is None:
            return 0.0
        
        max_distance = 0.0
        for i in range(min(len(prev_keypoints), len(curr_keypoints))):
            prev_pt = prev_keypoints[i]
            curr_pt = curr_keypoints[i]
            
            # Check confidence (3rd value if available)
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


# Global instance for GUI integration
_runner: Optional[ReactionTimeRunner] = None


def initialize_camera_and_model() -> Tuple[bool, Optional[str]]:
    """Initialize camera and model (global instance).
    
    Returns:
        (success: bool, error_message: str | None)
    """
    global _runner
    _runner = ReactionTimeRunner()
    return _runner.initialize_camera_and_model()


def measure_reaction_time() -> ReactionResult:
    """Measure reaction time using global instance.
    
    Returns:
        ReactionResult with reaction_ms or status
    """
    global _runner
    if _runner is None:
        return ReactionResult(success=False, status="error",
                            error_message="Not initialized")
    return _runner.measure_reaction_time()


def cleanup():
    """Cleanup resources."""
    global _runner
    if _runner is not None:
        _runner.cleanup()
