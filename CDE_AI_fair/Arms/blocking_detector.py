"""Blocking detection module using YOLO pose estimation.

This module provides backend functionality for detecting blocking movements
and recording user actions through pose estimation.
Designed for GUI integration without any UI components.

Architecture matches reaction_time_runner.py pattern.
"""

import os
import time
import cv2
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

try:
    from ultralytics import YOLO
except ImportError as e:
    raise ImportError(f"Failed to import ultralytics (YOLO): {e}")


# Assume model is in ../models/ directory
ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "yolo11s-pose.pt"


@dataclass
class BlockingResult:
    """Structured result from blocking detection."""
    success: bool
    video_path: Optional[str] = None
    button_presses: List[Dict] = None  # List of {number: int, timestamp: float, pose_data: dict}
    total_presses: int = 0
    status: Optional[str] = None  # "error" or None if success
    error_message: Optional[str] = None


class BlockingDetector:
    """Backend for blocking detection using YOLO pose estimation."""
    
    def __init__(self, camera_index: int = 0, confidence_threshold: float = 0.3,
                 video_save_path: str = "/home/claude/blocking_recording.mp4"):
        """Initialize the blocking detector.
        
        Args:
            camera_index: Camera device index (default 0)
            confidence_threshold: Minimum keypoint confidence (0.0-1.0)
            video_save_path: Path to save recorded video
        """
        self.camera_index = camera_index
        self.confidence_threshold = confidence_threshold
        self.video_save_path = video_save_path
        self.cap: Optional[cv2.VideoCapture] = None
        self.model: Optional[YOLO] = None
        self.video_writer: Optional[cv2.VideoWriter] = None
        
        # Recording state
        self.is_recording = False
        self.button_presses = []
        self.recording_start_time = None
    
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
        """Start video recording and blocking detection.
        
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
            
            # Reset recording state
            self.is_recording = True
            self.button_presses = []
            self.recording_start_time = time.time()
            
            return (True, None)
        
        except Exception as e:
            return (False, f"Failed to start recording: {str(e)}")
    
    def process_frame(self) -> Tuple[bool, Optional[str]]:
        """Process a single frame during recording.
        
        Should be called continuously while blocking mode is active.
        
        Returns:
            (success: bool, error_message: str | None)
        """
        if not self.is_recording:
            return (False, "Recording not active")
        
        if self.cap is None or self.model is None:
            return (False, "Camera/model not initialized")
        
        try:
            ok, frame = self.cap.read()
            if not ok:
                return (False, "Failed to read frame")
            
            frame = cv2.flip(frame, 1)
            
            # Run pose estimation
            results = self.model(frame, verbose=False)
            keypoints = self._extract_keypoints(results)
            
            # Draw skeleton on frame
            if keypoints is not None:
                frame = self._draw_skeleton(frame, keypoints)
            
            # Draw recording indicator
            cv2.circle(frame, (20, 20), 10, (0, 0, 255), -1)
            cv2.putText(
                frame,
                "RECORDING",
                (40, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )
            
            # Draw button press count
            cv2.putText(
                frame,
                f"Button Presses: {len(self.button_presses)}",
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
            
            # Write frame to video
            if self.video_writer is not None:
                self.video_writer.write(frame)
            
            return (True, None)
        
        except Exception as e:
            return (False, f"Frame processing failed: {str(e)}")
    
    def register_button_press(self, button_number: int) -> bool:
        """Register a button press with current pose data.
        
        Args:
            button_number: The number button pressed (1-6)
        
        Returns:
            success: bool
        """
        if not self.is_recording:
            return False
        
        try:
            # Capture current frame and pose
            ok, frame = self.cap.read()
            if ok:
                frame = cv2.flip(frame, 1)
                results = self.model(frame, verbose=False)
                keypoints = self._extract_keypoints(results)
                
                # Store button press with timestamp and pose data
                press_data = {
                    'number': button_number,
                    'timestamp': time.time() - self.recording_start_time,
                    'pose_data': {
                        'keypoints': keypoints.tolist() if keypoints is not None else None,
                        'confidence': self._get_average_confidence(keypoints)
                    }
                }
                
                self.button_presses.append(press_data)
                
                # Draw visual feedback on video
                if self.video_writer is not None:
                    # Annotate frame with button press
                    cv2.putText(
                        frame,
                        f"BUTTON {button_number}",
                        (frame.shape[1] // 2 - 100, frame.shape[0] // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2.0,
                        (0, 255, 0),
                        4
                    )
                    
                    # Write annotated frame multiple times for visibility
                    for _ in range(15):  # Show for ~0.5 seconds at 30fps
                        self.video_writer.write(frame)
                
                return True
            
            return False
        
        except Exception as e:
            print(f"Failed to register button press: {e}")
            return False
    
    def stop_recording(self) -> BlockingResult:
        """Stop video recording and return results.
        
        Returns:
            BlockingResult with recording details
        """
        try:
            self.is_recording = False
            
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None
            
            return BlockingResult(
                success=True,
                video_path=self.video_save_path,
                button_presses=self.button_presses.copy(),
                total_presses=len(self.button_presses)
            )
        
        except Exception as e:
            return BlockingResult(
                success=False,
                status="error",
                error_message=f"Failed to stop recording: {str(e)}"
            )
    
    def cleanup(self):
        """Release all resources."""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
        
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
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
    
    @staticmethod
    def _get_average_confidence(keypoints) -> float:
        """Calculate average confidence of all keypoints.
        
        Args:
            keypoints: Keypoint array
        
        Returns:
            Average confidence (0.0-1.0)
        """
        if keypoints is None:
            return 0.0
        
        confidences = []
        for kp in keypoints:
            if len(kp) >= 3:
                confidences.append(kp[2])
        
        return np.mean(confidences) if confidences else 0.0
    
    @staticmethod
    def _draw_skeleton(frame, keypoints, confidence_threshold: float = 0.3):
        """Draw skeleton on frame.
        
        Args:
            frame: Video frame
            keypoints: YOLO keypoints
            confidence_threshold: Minimum confidence to draw
        
        Returns:
            Annotated frame
        """
        if keypoints is None:
            return frame
        
        # COCO-17 skeleton connections
        connections = [
            (0, 1), (0, 2), (1, 3), (2, 4),  # Head
            (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),  # Arms
            (5, 11), (6, 12), (11, 12),  # Torso
            (11, 13), (13, 15), (12, 14), (14, 16)  # Legs
        ]
        
        # Draw connections
        for start_idx, end_idx in connections:
            if start_idx >= len(keypoints) or end_idx >= len(keypoints):
                continue
            
            start_pt = keypoints[start_idx]
            end_pt = keypoints[end_idx]
            
            # Check confidence
            if len(start_pt) >= 3 and len(end_pt) >= 3:
                if start_pt[2] < confidence_threshold or end_pt[2] < confidence_threshold:
                    continue
            
            # Draw line
            start_pos = (int(start_pt[0]), int(start_pt[1]))
            end_pos = (int(end_pt[0]), int(end_pt[1]))
            cv2.line(frame, start_pos, end_pos, (0, 255, 0), 2)
        
        # Draw keypoints
        for kp in keypoints:
            if len(kp) >= 3 and kp[2] > confidence_threshold:
                pos = (int(kp[0]), int(kp[1]))
                cv2.circle(frame, pos, 4, (0, 0, 255), -1)
        
        return frame


# ============================================================================
# GLOBAL INSTANCE FOR GUI INTEGRATION
# ============================================================================

_detector: Optional[BlockingDetector] = None


def initialize_camera_and_model(camera_index: int = 0,
                                video_path: str = "/home/claude/blocking_recording.mp4") -> Tuple[bool, Optional[str]]:
    """Initialize camera and model (global instance).
    
    Args:
        camera_index: Camera device index
        video_path: Path to save recorded video
    
    Returns:
        (success: bool, error_message: str | None)
    """
    global _detector
    _detector = BlockingDetector(camera_index=camera_index, video_save_path=video_path)
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


def process_frame() -> Tuple[bool, Optional[str]]:
    """Process a single frame using global instance.
    
    Returns:
        (success: bool, error_message: str | None)
    """
    global _detector
    if _detector is None:
        return (False, "Detector not initialized")
    return _detector.process_frame()


def register_button_press(button_number: int) -> bool:
    """Register a button press using global instance.
    
    Args:
        button_number: The number button pressed (1-6)
    
    Returns:
        success: bool
    """
    global _detector
    if _detector is None:
        return False
    return _detector.register_button_press(button_number)


def stop_recording() -> BlockingResult:
    """Stop recording using global instance.
    
    Returns:
        BlockingResult with recording details
    """
    global _detector
    if _detector is None:
        return BlockingResult(
            success=False,
            status="error",
            error_message="Detector not initialized"
        )
    return _detector.stop_recording()


def cleanup():
    """Cleanup resources."""
    global _detector
    if _detector is not None:
        _detector.cleanup()
        _detector = None
