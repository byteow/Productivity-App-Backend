from dotenv import load_dotenv
import os
load_dotenv()

PG_URI = os.environ.get("PG_URI")
JWT_ACCESS_SECRET = os.environ.get("JWT_ACCESS_SECRET")
JWT_REFRESH_SECRET = os.environ.get("JWT_REFRESH_SECRET")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")