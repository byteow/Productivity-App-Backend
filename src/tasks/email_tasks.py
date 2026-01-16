from email.message import EmailMessage
from config import (
    EMAIL_LOGIN,
    EMAIL_PASSWORD,
    EMAIL_SERVER,
    EMAIL_SERVER_PORT
)
import ssl
import smtplib

def send_code(email: str, code: int):
    try:
        message = EmailMessage()
        message.set_content(f"Ваш код подтверждения: {code}")
        message["Subject"] = "Код подтверждения"
        message["From"] = EMAIL_LOGIN
        message["To"] = email

        with smtplib.SMTP(EMAIL_SERVER, EMAIL_SERVER_PORT, timeout=10) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
            server.send_message(message)

    except smtplib.SMTPException as e:
        print("SMTPException:", e)