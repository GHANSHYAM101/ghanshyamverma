# emergency_detector.py
import torch

# Load model once
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Change to your custom model if needed
model.conf = 0.4  # Confidence threshold

EMERGENCY_CLASSES = ["ambulance", "fire_truck", "police_car"]

def detect_emergency_vehicle(frame):
    results = model(frame)
    detected = False

    for *box, conf, cls in results.xyxy[0]:
        label = results.names[int(cls)]
        if label.lower() in EMERGENCY_CLASSES:
            detected = True
            break

    return detected
