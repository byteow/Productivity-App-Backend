from celery import Celery
from config import (
    CELERY_BROKER_URL, 
    CELERY_RESULT_BACKEND,
    EMAIL_PASSWORD,
    EMAIL_LOGIN,
    EMAIL_SERVER,
    EMAIL_SERVER_PORT,
    REDIS_URL
)
from db import (
    SurveyStatus,
    update_survey,
    get_engine
)
from email.message import EmailMessage
import ssl
import smtplib
import asyncio
import redis.asyncio as redis
import json

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND

questions = [
    {"question": "Сколько часов вы спали прошлой ночью?", "answer_type": "numeric"},
    {"question": "Как вы оцениваете свою продуктивность за неделю?", "answer_type": "scale-1-5"},
    {"question": "Какая личная активность дала наибольшую пользу вашему самочувствию?", "answer_type": "text"},
    {"question": "Сколько задач вы закрыли на прошлой неделе?", "answer_type": "numeric"},
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

async def async_generate_survey(user_id: int, survey_id: int):
    await asyncio.sleep(10)

    # TODO: generate survey via ChatGPT

    _, AsyncSessionLocal = get_engine()

    async with AsyncSessionLocal() as session:
        await update_survey(
            session,
            survey_id=survey_id,
            status=SurveyStatus.PENDING,
            schema=questions
        )

    r = redis.from_url(REDIS_URL)

    notification = {"type": "survey_generated"}
    await r.publish(f"user_event_{user_id}", json.dumps(notification))
    await r.aclose()

@worker.task(name="generate_survey")
def generate_survey(user_id: int, survey_id: int):
    return asyncio.run(async_generate_survey(user_id, survey_id))