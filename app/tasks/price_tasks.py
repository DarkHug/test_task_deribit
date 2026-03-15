import asyncio
import logging
import time

from app.clients.deribit_client import get_index_price
from app.db.session import SessionLocal
from app.services import price_service
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def fetch_prices():
    async def run():
        btc_price = await get_index_price("btc_usd")
        eth_price = await get_index_price("eth_usd")

        timestamp = int(time.time())

        async with SessionLocal() as db:
            await price_service.save_price(db, "BTC_USD", btc_price, timestamp)
            await price_service.save_price(db, "ETH_USD", eth_price, timestamp)
            logger.info("Fetched BTC: %s, ETH: %s", btc_price, eth_price)

    asyncio.run(run())
