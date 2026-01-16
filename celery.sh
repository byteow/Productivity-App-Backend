cd src
celery -A celery_worker.worker worker --loglevel=info -B