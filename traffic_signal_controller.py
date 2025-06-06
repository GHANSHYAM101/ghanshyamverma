# traffic_signal_controller.py
from threading import Lock

override_map = {}
lock = Lock()

def override_signal(cam_name):
    with lock:
        override_map[cam_name] = True

def is_override(cam_name):
    with lock:
        return override_map.get(cam_name, False)

def clear_override(cam_name):
    with lock:
        override_map.pop(cam_name, None)
