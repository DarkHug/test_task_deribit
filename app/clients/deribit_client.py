import aiohttp

from app.config import settings


async def get_index_price(currency: str) -> float:
    url = f"{settings.DERIBIT_API_URL}/public/get_index_price"

    params = {"index_name": currency}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json(content_type=None)

    if "result" not in data:
        raise ValueError(f"Invalid response from Deribit: {data}")

    return data["result"]["index_price"]
