from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.clients.deribit_client import get_index_price
from app.db.session import get_db
from app.services import price_service

router = APIRouter(prefix="/prices", tags=["prices"])
DBSession = Annotated[Session, Depends(get_db)]


@router.get("/")
def get_prices(ticker: str, db: DBSession):
    return price_service.get_all_prices(db=db, ticker=ticker)


@router.get("/latest")
def get_latest_price(ticker: str, db: DBSession):
    return price_service.get_last_price(db=db, ticker=ticker)


@router.get("/by-date")
def get_prices_by_date(
        ticker: str,
        timestamp: int,
        db: DBSession,
):
    return price_service.get_prices_by_date(
        db=db,
        ticker=ticker,
        timestamp=timestamp,
    )


@router.get("/test-deribit")
async def test_deribit():
    btc_price = await get_index_price("btc_usd")
    eth_price = await get_index_price("eth_usd")

    return {
        "BTC_USD": btc_price,
        "ETH_USD": eth_price,
    }
