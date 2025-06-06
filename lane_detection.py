import cv2
import numpy as np

def detect_lanes_and_assign_vehicles(frame, vehicles):
    lane_lines = []
    lane_regions = []

    # Step 1: Preprocess for white detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    edges = cv2.Canny(white_mask, 50, 150)

    # Step 2: Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100,
                            minLineLength=50, maxLineGap=50)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            lane_lines.append((x1 + x2) // 2)  # Approximate vertical x positions

    lane_lines = sorted(list(set(lane_lines)))

    # Step 3: Define lane regions between lines
    if len(lane_lines) >= 2:
        for i in range(len(lane_lines) - 1):
            lane_regions.append((lane_lines[i], lane_lines[i + 1]))

    # Step 4: Assign each vehicle to a lane
    vehicle_lane_map = {}
    for vehicle in vehicles:
        x1, y1, x2, y2 = vehicle["bbox"]
        vehicle_center = (x1 + x2) // 2

        assigned = False
        for idx, (left, right) in enumerate(lane_regions):
            if left <= vehicle_center < right:
                vehicle_lane_map[vehicle["id"]] = idx + 1
                assigned = True
                break
        if not assigned:
            vehicle_lane_map[vehicle["id"]] = -1  # Unassigned

    # Optional: annotate frame
    for vehicle in vehicles:
        lane = vehicle_lane_map.get(vehicle["id"], -1)
        x1, y1, _, _ = vehicle["bbox"]
        cv2.putText(frame, f"Lane {lane}", (x1, y1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    return frame, vehicle_lane_map
