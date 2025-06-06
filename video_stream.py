# backend/video_stream.py
import cv2
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from stats_manager import stats  # to overlay vehicle count

router = APIRouter()

CAM_SOURCES = {
    "CAM1": "cameras/v.mp4",
    "CAM2": "cameras/v.mp4",
    "CAM3": "cameras/v.mp4",
    "CAM4": "cameras/v.mp4"
}
def gen_frames(source):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video source: {source}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # ✅ Draw vehicle count on frame
        count = stats.get_stats()["vehicles"]
        cv2.putText(frame, f"Vehicles: {count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
        )

    cap.release()

@router.get("/video_feed/{cam_id}")
def video_feed(cam_id: str):
    if cam_id not in CAM_SOURCES:
        raise HTTPException(status_code=404, detail="Camera not found")

    return StreamingResponse(
        gen_frames(CAM_SOURCES[cam_id]),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
