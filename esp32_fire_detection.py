from roboflow import Roboflow
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# -------- CONFIGURATION --------

ROBOFLOW_API_KEY = "TA_NOUVELLE_API_KEY"
WORKSPACE = "ton_workspace"
PROJECT = "fire-smoke-detection-kg5hm"
VERSION = 5

EMAIL_SENDER = "monprojet.alert@gmail.com"
EMAIL_PASSWORD = "MOT_DE_PASSE_APPLICATION"
EMAIL_RECEIVER = "destinataire@gmail.com"

CONFIDENCE_THRESHOLD = 0.6  # 60%
ALERT_INTERVAL = 60  # secondes (anti-spam)

# -------- INITIALISATION --------

rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)
model = project.version(VERSION).model

last_alert_time = 0

# -------- FONCTION EMAIL --------

def send_email_alert(classe, confidence):
    subject = "🚨 ALERTE INCENDIE"
    body = f"""
    ⚠️ DÉTECTION DANGEREUSE ⚠️

    Type détecté : {classe}
    Confiance : {confidence*100:.1f} %

    Veuillez vérifier immédiatement.
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

# -------- TEST SUR UNE IMAGE --------

result = model.predict("image_test.jpg", confidence=40, overlap=30).json()

current_time = time.time()

for pred in result["predictions"]:
    classe = pred["class"]
    confidence = pred["confidence"]

    if classe in ["fire", "smoke"] and confidence >= CONFIDENCE_THRESHOLD:
        if current_time - last_alert_time > ALERT_INTERVAL:
            print("🚨 ALERTE :", classe, confidence)
            send_email_alert(classe, confidence)
            last_alert_time = current_time