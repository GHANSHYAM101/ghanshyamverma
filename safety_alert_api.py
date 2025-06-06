from fastapi import APIRouter
from women_safety_audio import alert_log

router = APIRouter()

@router.get("/api/safety-alerts")
def get_safety_alerts():
    return alert_log
