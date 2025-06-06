from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf(vehicle_number, violation_type, speed, image_path=None, output_path=None, camera_id="CAM01"):
    # Create default path if output_path not given
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not output_path:
        challan_dir = "e_challans"
        os.makedirs(challan_dir, exist_ok=True)
        output_path = os.path.join(challan_dir, f"challan_{vehicle_number}_{timestamp}.pdf")
    else:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, "Smart Traffic E-Challan")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Vehicle Number: {vehicle_number}")
    c.drawString(50, 740, f"Violation: {violation_type}")
    c.drawString(50, 720, f"Speed: {speed:.2f} km/h")
    c.drawString(50, 700, f"Camera ID: {camera_id}")
    c.drawString(50, 680, f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if image_path and os.path.exists(image_path):
        c.drawImage(image_path, 50, 500, width=200, height=150)

    c.showPage()
    c.save()
    return output_path
