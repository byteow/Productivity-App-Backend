from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND

@worker.task(name="send_code")
def send_code(email: str, code: int):
    print("Hello world")