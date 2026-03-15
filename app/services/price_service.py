from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import price_repo


async def save_price(db: AsyncSession, ticker: str, price: float, timestamp: int):
    new_price = await price_repo.create_price(session=db, ticker=ticker, price=price, timestamp=timestamp)
    await db.commit()
    return new_price


async def get_all_prices(db: AsyncSession, ticker: str):
    return await price_repo.get_all_by_ticker(session=db, ticker=ticker)


async def get_last_price(db: AsyncSession, ticker: str):
    return await price_repo.get_last_price_by_ticker(session=db, ticker=ticker)


async def get_prices_by_date(db: AsyncSession, ticker: str, timestamp: int):
    return await price_repo.get_price_by_date(session=db, ticker=ticker, timestamp=timestamp)
