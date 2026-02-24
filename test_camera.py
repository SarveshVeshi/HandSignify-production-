import cv2
import sys

try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera failed to open")
    else:
        print("Camera opened successfully")
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
        else:
            print(f"Read frame with shape: {frame.shape}")
        cap.release()
except Exception as e:
    print(f"Exception during camera init: {e}")
