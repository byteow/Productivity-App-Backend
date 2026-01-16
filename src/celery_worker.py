import asyncio
from celery import Celery
from config import (
    CELERY_BROKER_URL, 
    CELERY_RESULT_BACKEND
)
from tasks import (
    async_generate_survey, 
    send_code, 
    async_clean_old_tasks
)
from datetime import timedelta

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND

worker.conf.beat_schedule = {
    'old_tasks_clean_every_hour': {
        'task': 'clean_old_tasks',
        'schedule': timedelta(hours=1),
    },
}
worker.conf.timezone = 'UTC'

@worker.task(name="clean_old_tasks")
def clean_old_tasks_task():
    return asyncio.run(async_clean_old_tasks())

@worker.task(name="generate_survey", rate_limit="40/m")
def generate_survey_task(user_id: int, survey_id: int):
    return asyncio.run(async_generate_survey(user_id, survey_id))

@worker.task(name="send_code", rate_limit="20/m")
def send_code_task(email: str, code: int):
    return send_code(email, code)