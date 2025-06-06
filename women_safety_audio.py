import json
from vosk import Model, KaldiRecognizer
import pyaudio
from datetime import datetime

# Initialize model & recognizer on import
model     = Model("models/vosk-model-small-en-us-0.15")
rec       = KaldiRecognizer(model, 16000)
alert_log = []

def check_for_alerts(text):
    alert_keywords = ["help", "save me", "leave me", "don't touch", "bachao"]
    return any(phrase in text.lower() for phrase in alert_keywords)

def monitor_audio():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000
    )
    stream.start_stream()
    print("[🔊 Listening for distress signals...]")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text   = result.get("text", "")
            if text and check_for_alerts(text):
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[⚠️ ALERT @ {ts}] \"{text}\"")
                alert_log.append({"timestamp": ts, "message": text})

def get_alerts():
    return alert_log
