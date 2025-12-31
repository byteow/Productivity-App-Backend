from celery import Celery
from config import (
    CELERY_BROKER_URL, 
    CELERY_RESULT_BACKEND,
    EMAIL_PASSWORD,
    EMAIL_LOGIN,
    EMAIL_SERVER
)
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND

@worker.task(name="send_code")
def send_code(email: str, code: int):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(EMAIL_SERVER, 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_LOGIN, EMAIL_PASSWORD)

            message = MIMEMultipart()
            message["From"] = EMAIL_LOGIN
            message["To"] = email
            message["Subject"] = "Confirmation code"
            message.attach(MIMEText(f"Confirmation code: {code}", "plain"))

            server.send_message(message)
    except smtplib.SMTPException as e:
        print("SMTPException:", e)