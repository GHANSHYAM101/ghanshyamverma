from fastapi import APIRouter
from multi_camera_processor import vehicle_counts, traffic_lights

router = APIRouter()

@router.get("/traffic/vehicle-counts")
def get_vehicle_counts():
    return vehicle_counts

@router.get("/traffic/lights")
def get_traffic_lights():
    return traffic_lights
