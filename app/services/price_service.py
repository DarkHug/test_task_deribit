from sqlalchemy.orm import Session

from app.repositories import price_repo


def save_price(db: Session, ticker: str, price: float, timestamp: int):
    new_price = price_repo.create_price(
        session=db,
        ticker=ticker,
        price=price,
        timestamp=timestamp,
    )
    db.commit()
    return new_price


def get_all_prices(db: Session, ticker: str):
    return price_repo.get_all_by_ticker(
        session=db,
        ticker=ticker,
    )


def get_last_price(db: Session, ticker: str):
    return price_repo.get_last_price_by_ticker(
        session=db,
        ticker=ticker,
    )


def get_prices_by_date(db: Session, ticker: str, timestamp: int):
    return price_repo.get_price_by_date(
        session=db,
        ticker=ticker,
        timestamp=timestamp,
    )
