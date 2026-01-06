from celery import Celery
from config import (
    CELERY_BROKER_URL, 
    CELERY_RESULT_BACKEND,
    EMAIL_PASSWORD,
    EMAIL_LOGIN,
    EMAIL_SERVER,
    EMAIL_SERVER_PORT
)
from db import (
    get_session,
    SurveyStatus,
    update_survey,
    AsyncSessionLocal
)
from email.message import EmailMessage
import ssl
import smtplib
import time
import asyncio

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND

questions = [
    {"question": "Сколько часов сна прошлой ночью?", "answer_type": "numeric"},
    {"question": "Как вы оцениваете свою продуктивность за неделю?", "answer_type": "scale-1-5"},
    {"question": "Какая личная активность дала наибольшую пользу вашему самочувствию?", "answer_type": "text"},
    {"question": "Сколько задач вы закрыли на прошлой неделе?", "answer_type": "numeric", "order": 4},
    {"question": "Насколько вы восстановились эмоционально и физически?", "answer_type": "scale-1-5"},
    {"question": "Вы планируете новые цели на следующую неделю?", "answer_type": "single_choice"}
]

@worker.task(name="send_code")
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

async def async_generate_survey(survey_id: int):
    time.sleep(10)

    # TODO: generate survey via ChatGPT

    async with AsyncSessionLocal() as session:
        await update_survey(
            session,
            survey_id=survey_id,
            status=SurveyStatus.PENDING,
            schema=questions
        )

@worker.task(name="generate_survey")
def generate_survey(survey_id: int):
    return asyncio.run(async_generate_survey(survey_id))