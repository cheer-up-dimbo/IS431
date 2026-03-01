import cv2
from ultralytics import YOLO
import numpy as np

MODEL_PATH = "models/yolo11n-pose.pt"

class PunchDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        
    def calculate_angle(self, point1, point2, point3):
        """Calculate angle at point2 formed by point1-point2-point3."""
        vector1 = point1[:2] - point2[:2]
        vector2 = point3[:2] - point2[:2]
        
        dot_product = np.dot(vector1, vector2)
        magnitude1 = np.linalg.norm(vector1)
        magnitude2 = np.linalg.norm(vector2)
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        cos_angle = dot_product / (magnitude1 * magnitude2)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.degrees(np.arccos(cos_angle))
        
        return angle
    
    def get_punch_type(self, keypoints):
        """
        Detect punch type based on arm straightness and extension.
        
        YOLO pose keypoints (17 points):
        0: nose, 1-2: eyes, 3-4: ears, 5: left shoulder, 6: right shoulder,
        7: left elbow, 8: right elbow, 9: left wrist, 10: right wrist,
        11: left hip, 12: right hip, 13-16: knees and ankles
        
        Boxing logic:
        - JAB = LEFT arm extended (right side of face exposed to counter)
        - CROSS = RIGHT arm extended (left side of face exposed to counter)
        """
        if keypoints is None or len(keypoints) < 11:
            return None, None
            
        # Extract key points
        nose = keypoints[0]
        left_shoulder = keypoints[5]
        right_shoulder = keypoints[6]
        left_elbow = keypoints[7]
        right_elbow = keypoints[8]
        left_wrist = keypoints[9]
        right_wrist = keypoints[10]
        
        # Check confidence of keypoints (3rd value)
        if (left_shoulder[2] < 0.5 or right_shoulder[2] < 0.5 or
            left_elbow[2] < 0.5 or right_elbow[2] < 0.5 or
            left_wrist[2] < 0.5 or right_wrist[2] < 0.5):
            return None, None
        
        # Calculate angles at elbows (straight arm = ~180 degrees)
        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        # Calculate arm extensions
        left_extension = np.linalg.norm(left_wrist[:2] - left_shoulder[:2])
        right_extension = np.linalg.norm(right_wrist[:2] - right_shoulder[:2])
        
        # Calculate shoulder width for normalization
        shoulder_width = np.linalg.norm(left_shoulder[:2] - right_shoulder[:2])
        if shoulder_width == 0:
            return None, None
        
        # Normalize extensions
        left_ext_ratio = left_extension / shoulder_width
        right_ext_ratio = right_extension / shoulder_width
        
        # Check if arm is extended forward (wrist ahead of shoulder in x)
        # In most camera views, x increases to the right, y increases downward
        left_forward = abs(left_wrist[1] - left_shoulder[1]) > shoulder_width * 0.2
        right_forward = abs(right_wrist[1] - right_shoulder[1]) > shoulder_width * 0.2
        
        # Detection thresholds
        angle_threshold = 150  # degrees (straighter arm = punch)
        extension_threshold = 0.9  # Lower threshold for more sensitivity
        
        left_punch_score = 0
        right_punch_score = 0
        
        # Score left arm
        if left_elbow_angle > angle_threshold:
            left_punch_score += 2
        if left_ext_ratio > extension_threshold:
            left_punch_score += 2
        if left_forward:
            left_punch_score += 1
            
        # Score right arm
        if right_elbow_angle > angle_threshold:
            right_punch_score += 2
        if right_ext_ratio > extension_threshold:
            right_punch_score += 2
        if right_forward:
            right_punch_score += 1
        
        # Determine punch type (need score >= 3)
        if left_punch_score >= 3 and left_punch_score > right_punch_score:
            return 'jab', left_elbow_angle
        elif right_punch_score >= 3 and right_punch_score > left_punch_score:
            return 'cross', right_elbow_angle
            
        return None, None
    
    def get_head_center_and_size(self, keypoints):
        """Calculate head center position and approximate size."""
        nose = keypoints[0]
        left_eye = keypoints[1]
        right_eye = keypoints[2]
        left_ear = keypoints[3]
        right_ear = keypoints[4]
        
        # Head center (average of facial keypoints)
        valid_points = []
        for point in [nose, left_eye, right_eye, left_ear, right_ear]:
            if point[2] > 0.5:  # Check confidence
                valid_points.append(point[:2])
        
        if len(valid_points) < 2:
            # Fallback to nose
            return nose[:2], 50, 65
        
        head_center = np.mean(valid_points, axis=0)
        
        # Head size (distance between ears or eyes)
        if left_ear[2] > 0.5 and right_ear[2] > 0.5:
            head_width = np.linalg.norm(left_ear[:2] - right_ear[:2])
        else:
            head_width = np.linalg.norm(left_eye[:2] - right_eye[:2]) * 1.5
            
        head_height = head_width * 1.3
        
        return head_center, head_width, head_height
    
    def draw_head_exposure(self, frame, keypoints, punch_type):
        """
        Draw the exposed/vulnerable side of the head.
        
        When you throw a JAB (left punch):
        - Your LEFT arm extends forward
        - Your RIGHT side of face is EXPOSED to counters
        
        When you throw a CROSS (right punch):
        - Your RIGHT arm extends forward  
        - Your LEFT side of face is EXPOSED to counters
        """
        if punch_type is None or keypoints is None:
            return frame
        
        head_center, head_width, head_height = self.get_head_center_and_size(keypoints)
        
        # Create overlay for semi-transparent effect
        overlay = frame.copy()
        
        center_x, center_y = int(head_center[0]), int(head_center[1])
        radius = int(head_width * 1.8)  # Larger radius for more obvious visualization
        
        if punch_type == 'jab':
            # JAB = left arm extended, so RIGHT side of face is exposed
            color = (0, 0, 255)  # Red for danger/exposure
            label = "RIGHT SIDE EXPOSED!"
            
            # Create points for filled polygon (RIGHT half circle)
            points = []
            for angle in range(-90, 91, 2):  # Right half
                x = int(center_x + radius * np.cos(np.radians(angle)))
                y = int(center_y + radius * np.sin(np.radians(angle)))
                points.append([x, y])
            points.append([center_x, center_y])
            
            points = np.array(points, dtype=np.int32)
            cv2.fillPoly(overlay, [points], color)
                
        elif punch_type == 'cross':
            # CROSS = right arm extended, so LEFT side of face is exposed
            color = (0, 0, 255)  # Red for danger/exposure
            label = "LEFT SIDE EXPOSED!"
            
            # Create points for filled polygon (LEFT half circle)
            points = []
            for angle in range(90, 271, 2):  # Left half
                x = int(center_x + radius * np.cos(np.radians(angle)))
                y = int(center_y + radius * np.sin(np.radians(angle)))
                points.append([x, y])
            points.append([center_x, center_y])
            
            points = np.array(points, dtype=np.int32)
            cv2.fillPoly(overlay, [points], color)
        
        # Blend overlay with original frame (more visible)
        alpha = 0.65
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        # Draw label with background for better visibility
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        label_x = center_x - label_size[0] // 2
        label_y = center_y - radius - 30
        
        # Draw background rectangle
        cv2.rectangle(frame, 
                     (label_x - 10, label_y - label_size[1] - 10),
                     (label_x + label_size[0] + 10, label_y + 10),
                     (0, 0, 0), -1)
        
        # Draw text
        cv2.putText(frame, label, (label_x, label_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        # Draw head outline circle
        cv2.circle(frame, (center_x, center_y), radius, (255, 255, 0), 3)
        
        return frame
    
    def process_frame(self, frame):
        """Process a single frame and return annotated frame."""
        # Run pose detection
        results = self.model(frame, verbose=False)
        
        annotated_frame = frame.copy()
        
        if len(results) > 0 and results[0].keypoints is not None:
            # Get first person's keypoints
            keypoints_data = results[0].keypoints.data
            
            if len(keypoints_data) > 0:
                keypoints = keypoints_data[0].cpu().numpy()
                
                # Detect punch type
                punch_type, confidence = self.get_punch_type(keypoints)
                
                # Draw skeleton
                annotated_frame = results[0].plot()
                
                # Draw head exposure
                if punch_type:
                    annotated_frame = self.draw_head_exposure(
                        annotated_frame, keypoints, punch_type
                    )
                    
                    # Display punch type
                    punch_text = f"{punch_type.upper()} DETECTED!"
                    cv2.putText(annotated_frame, punch_text, (20, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    
                    # Display angle for debugging
                    debug_text = f"Angle: {confidence:.1f}deg"
                    cv2.putText(annotated_frame, debug_text, (20, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        return annotated_frame


def main():
    # Initialize detector
    detector = PunchDetector(MODEL_PATH)
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Boxing Punch Detection Started!")
    print("=" * 50)
    print("JAB (left punch) -> RIGHT side of face EXPOSED")
    print("CROSS (right punch) -> LEFT side of face EXPOSED")
    print("=" * 50)
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame
        annotated_frame = detector.process_frame(frame)
        
        # Display
        cv2.imshow('Boxing Punch Detection - Head Exposure', annotated_frame)
        
        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()