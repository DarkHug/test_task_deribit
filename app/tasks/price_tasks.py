import logging
import time

from app.clients.deribit_client import get_index_price
from app.db.session import SessionLocal
from app.services import price_service
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def fetch_prices():
    db = SessionLocal()

    try:
        btc_price = get_index_price("btc_usd")
        eth_price = get_index_price("eth_usd")

        timestamp = int(time.time())

        price_service.save_price(db, "BTC_USD", btc_price, timestamp)
        price_service.save_price(db, "ETH_USD", eth_price, timestamp)
        logger.info("Fetched BTC: %s, ETH: %s", btc_price, eth_price)

    finally:
        db.close()
