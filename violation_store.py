from datetime import datetime
from e_challan_generator import generate_pdf
import os
from stats_manager import stats  # Import the stats manager


violation_log = []
os.makedirs("e_challans", exist_ok=True)

def log_violation(vehicle_number, violation_type, speed, pdf_path, snapshot_path, cam_id):  
    pdf_path = generate_pdf(vehicle_number, violation_type, speed, snapshot_path, pdf_path, cam_id)
    violation_log.append({
        "vehicle": vehicle_number,
        "camera": cam_id,
        "type": violation_type,
        "speed": speed,
        "pdf": pdf_path,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    stats.increment_violation()


def get_all_violations():
    return violation_log
