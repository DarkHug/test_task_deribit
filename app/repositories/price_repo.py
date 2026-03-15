from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.price import Price


def create_price(session: Session, ticker: str, price: float, timestamp: int):
    new_price = Price(ticker=ticker, price=price, timestamp=timestamp)
    session.add(new_price)
    return new_price


def get_all_by_ticker(session: Session, ticker: str):
    stmt = select(Price).where(Price.ticker == ticker)
    return session.execute(stmt).scalars().all()


def get_last_price_by_ticker(session: Session, ticker: str):
    stmt = (
        select(Price)
        .where(Price.ticker == ticker)
        .order_by(Price.timestamp.desc())
        .limit(1)
    )
    return session.execute(stmt).scalar_one_or_none()


def get_price_by_date(session: Session, ticker: str, timestamp: int):
    stmt = select(Price).where(
        Price.ticker == ticker,
        Price.timestamp == timestamp,
    )
    return session.execute(stmt).scalar_one_or_none()
