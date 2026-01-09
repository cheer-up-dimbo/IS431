import os
import sys
import argparse
from pathlib import Path

try:
    import cv2
    import numpy as np
except Exception as e:
    print(f"ERROR: Failed to import OpenCV/NumPy: {e}")
    sys.exit(1)

try:
    from ultralytics import YOLO
except Exception as e:
    print(f"ERROR: Failed to import ultralytics (YOLO): {e}")
    print("Hint: pip install ultralytics")
    sys.exit(1)


ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT_DIR / "models" / "yolo11s-pose.pt"


def draw_pose_skeleton(img, results, point_color=(60, 180, 255), line_color=(40, 140, 255), thickness=3):
    """Draw COCO-17 skeleton for all detected persons on img."""
    try:
        if not results or len(results) == 0:
            return img
        kps = results[0].keypoints
        if kps is None or kps.data is None:
            return img
        arr = kps.data.cpu().numpy()
        if arr.shape[0] == 0:
            return img

        connections = [
            (5, 6),
            (5, 7), (7, 9),
            (6, 8), (8, 10),
            (11, 12),
            (5, 11), (6, 12),
            (11, 13), (13, 15),
            (12, 14), (14, 16),
        ]

        for person in arr:
            pts = person[:, :2]
            for i, j in connections:
                x1, y1 = pts[i]
                x2, y2 = pts[j]
                if (x1 > 0 or y1 > 0) and (x2 > 0 or y2 > 0):
                    cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), line_color, thickness)
            for x, y in pts:
                if x > 0 or y > 0:
                    cv2.circle(img, (int(x), int(y)), 4, point_color, -1, lineType=cv2.LINE_AA)
    except Exception:
        # Do not crash drawing
        pass
    return img


def main():
    parser = argparse.ArgumentParser(description="Simple YOLO pose viewer with skeleton overlay")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default 0)")
    parser.add_argument("--frames", type=int, default=-1, help="Max frames to process before exit (-1 = infinite)")
    parser.add_argument("--conf", type=float, default=0.30, help="Min keypoint confidence to consider valid")
    args = parser.parse_args()

    if not MODEL_PATH.exists():
        print(f"ERROR: Model file not found at: {MODEL_PATH}")
        sys.exit(1)

    try:
        model = YOLO(str(MODEL_PATH))
    except Exception as e:
        print(f"ERROR: Failed to load model: {e}")
        sys.exit(1)

    # Prefer DirectShow on Windows for better camera compatibility
    if os.name == "nt":
        cap = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(args.camera)

    if not cap.isOpened():
        print("ERROR: Cannot open camera. Check device index, permissions, or if another app is using it.")
        sys.exit(1)

    cv2.namedWindow("Pose Viewer", cv2.WINDOW_NORMAL)
    frame_limit = args.frames
    processed = 0
    any_detected = False

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("ERROR: Failed to read frame from camera.")
                break

            frame = cv2.flip(frame, 1)

            try:
                results = model(frame, verbose=False)
            except Exception as e:
                print(f"ERROR: Inference failed: {e}")
                break

            reason_printed = False
            if not results or len(results) == 0:
                print("INFO: No results returned by model for this frame.")
                reason_printed = True
            else:
                kps = results[0].keypoints
                if kps is None or kps.data is None:
                    print("INFO: No keypoints tensor in results (model did not produce pose data).")
                    reason_printed = True
                else:
                    arr = kps.data.cpu().numpy()
                    if arr.shape[0] == 0:
                        print("INFO: No persons detected (no pose instances).")
                        reason_printed = True
                    else:
                        # Check confidence if available (arr shape may be (N,17,3) with conf)
                        confs_ok = True
                        if arr.shape[-1] >= 3:
                            confs = arr[:, :, 2]
                            confs_ok = np.any(confs >= args.conf)
                        if not confs_ok:
                            print(f"INFO: Detected keypoints but all below confidence threshold {args.conf}.")
                            reason_printed = True
                        else:
                            any_detected = True
                            draw_pose_skeleton(frame, results)

            if not any_detected and not reason_printed:
                # Fallback reason when none could be determined
                print("INFO: Cannot detect.")

            cv2.imshow("Pose Viewer", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord('q'), 27):
                break

            processed += 1
            if frame_limit > 0 and processed >= frame_limit:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
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
from pathlib import Path

