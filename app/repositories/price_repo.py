from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import Price


async def create_price(session: AsyncSession, ticker: str, price: float, timestamp: int):
    new_price = Price(ticker=ticker, price=price, timestamp=timestamp)
    session.add(new_price)
    return new_price


async def get_all_by_ticker(session: AsyncSession, ticker: str):
    stmt = select(Price).where(Price.ticker == ticker)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_last_price_by_ticker(session: AsyncSession, ticker: str):
    stmt = (
        select(Price)
        .where(Price.ticker == ticker)
        .order_by(Price.timestamp.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_price_by_date(session: AsyncSession, ticker: str, timestamp: int):
    stmt = select(Price).where(
        Price.ticker == ticker,
        Price.timestamp == timestamp,
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
