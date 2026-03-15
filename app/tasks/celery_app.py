from celery import Celery
from app.config import settings

from app.tasks import price_tasks

celery_app = Celery(
    "crypto_price_service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.timezone = "UTC"

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.price_tasks.fetch_prices",
        "schedule": 60.0,
    },
}
