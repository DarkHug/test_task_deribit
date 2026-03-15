#!/bin/sh

echo "[!]Starting celery worker"
celery -A app.tasks.celery_app worker --loglevel=info &

echo "[!]Starting celery beat"
celery -A app.tasks.celery_app beat --loglevel=info &

echo "[!]Starting FastAPI"
uvicorn app.main:app --host 0.0.0.0 --port 8000