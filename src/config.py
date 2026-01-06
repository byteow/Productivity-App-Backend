from dotenv import load_dotenv
import os
load_dotenv()

# Database
PG_URI = os.environ.get("PG_URI")

# Authorization
JWT_ACCESS_SECRET = os.environ.get("JWT_ACCESS_SECRET")
JWT_REFRESH_SECRET = os.environ.get("JWT_REFRESH_SECRET")

# Background tasks
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

# Redis
REDIS_URL = os.environ.get("REDIS_URI")

# Emails
EMAIL_LOGIN = os.environ.get("EMAIL_LOGIN")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_SERVER = os.environ.get("EMAIL_SERVER")
EMAIL_SERVER_PORT = int(os.environ.get("EMAIL_SERVER_PORT"))

# CORS
CORS_ORIGINS = os.environ.get("CORS_ORIGINS").split(",")