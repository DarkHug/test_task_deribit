import asyncio
import aiohttp

from app.config import settings


async def _get_index_price(currency: str) -> float:
    url = f"{settings.DERIBIT_API_URL}/public/get_index_price"

    params = {"index_name": currency}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()

    return data["result"]["index_price"]


def get_index_price(currency: str) -> float:
    return asyncio.run(_get_index_price(currency))