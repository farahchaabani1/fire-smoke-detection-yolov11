import requests
import time
import smtplib
from roboflow import Roboflow
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =====================================================
# ================= CONFIGURATION =====================
# =====================================================

# ESP32
ESP32_CAM_URL = "http://192.168.1.25/capture"  
# Roboflow
ROBOFLOW_API_KEY = "TA_CLE_API_PRIVEE_ICI"
WORKSPACE = "farahchaaabani"
PROJECT = "fire-smoke-detection-kg5hm"
VERSION = 5

# Détection
CONFIDENCE_THRESHOLD = 0.6
CAPTURE_INTERVAL = 5  # secondes
ALERT_INTERVAL = 60   # anti-spam email (secondes)

# Email
EMAIL_SENDER = "tonemail@gmail.com"
EMAIL_PASSWORD = "abcdefghijklmnoq"
EMAIL_RECEIVER = "destinataire@gmail.com"

# =====================================================
# ================= INITIALISATION ====================
# =====================================================

rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)
model = project.version(VERSION).model

last_alert_time = 0

print("📷 ESP32 + Roboflow + Email démarré")

# =====================================================
# ================= FONCTION EMAIL ====================
# =====================================================

def send_email_alert(classe, confidence):
    subject = "🚨 ALERTE INCENDIE - ESP32 AI CAM"
    body = f"""
⚠️ ALERTE AUTOMATIQUE ⚠️

Type détecté : {classe}
Confiance : {confidence*100:.1f} %

Source : ESP32-S3 AI CAM
Action requise immédiatement.
"""

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    print("📧 Email envoyé avec succès")

# =====================================================
# ================= BOUCLE PRINCIPALE =================
# =====================================================

while True:
    try:
        # 1️⃣ Capture image depuis ESP32
        response = requests.get(ESP32_CAM_URL, timeout=5)
        with open("esp32.jpg", "wb") as f:
            f.write(response.content)

        # 2️⃣ Prédiction Roboflow
        result = model.predict("esp32.jpg", confidence=40, overlap=30).json()

        # 3️⃣ Analyse des résultats
        current_time = time.time()

        for pred in result["predictions"]:
            classe = pred["class"]
            confidence = pred["confidence"]

            if classe in ["fire", "smoke"] and confidence >= CONFIDENCE_THRESHOLD:
                print(f"🚨 DÉTECTION : {classe} ({confidence:.2f})")

                if current_time - last_alert_time > ALERT_INTERVAL:
                    send_email_alert(classe, confidence)
                    last_alert_time = current_time

        time.sleep(CAPTURE_INTERVAL)

    except Exception as e:
        print("❌ Erreur :", e)
        time.sleep(5)
