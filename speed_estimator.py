import cv2
import math

class SpeedEstimator:
    def __init__(self, fps, pixels_to_meters=0.05):
        self.speeds = {}  # object_id → latest speed in km/h
        self.fps = fps
        self.pixels_to_meters = pixels_to_meters
        self.object_positions = {}
        self.frame_count = 0

    def update(self, tracked_objects, frame):
        self.frame_count += 1
        for obj in tracked_objects:
            object_id = obj['id']
            x1, y1, x2, y2 = obj['bbox']
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            if object_id in self.object_positions:
                prev_cx, prev_cy = self.object_positions[object_id]['position']
                frame_diff = self.frame_count - self.object_positions[object_id]['last_frame']

                if frame_diff > 0:
                    pixel_distance = math.hypot(cx - prev_cx, cy - prev_cy)
                    speed_m_s = (pixel_distance * self.pixels_to_meters) * self.fps / frame_diff
                    speed_kmh = speed_m_s * 3.6

                    # Store the speed
                    self.speeds[object_id] = speed_kmh

                    # Draw speed
                    cv2.putText(frame, f"{int(speed_kmh)} km/h", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 0), 2)

            # Update tracking memory
            self.object_positions[object_id] = {
                'position': (cx, cy),
                'last_frame': self.frame_count
            }
        return frame

    
    def get_speed(self, object_id):
        return self.speeds.get(object_id, 0.0)

