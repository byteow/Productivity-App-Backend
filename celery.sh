cd src
celery -A worker.worker worker --loglevel=info