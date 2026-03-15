from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.price_schema import PriceResponse
from app.services import price_service

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/", response_model=list[PriceResponse])
async def get_prices(ticker: str, db: Annotated[AsyncSession, Depends(get_db)]):
    return await price_service.get_all_prices(db=db, ticker=ticker)


@router.get("/latest", response_model=PriceResponse | None)
async def get_latest_price(ticker: str, db: Annotated[AsyncSession, Depends(get_db)]):
    return await price_service.get_last_price(db=db, ticker=ticker)


@router.get("/by-date", response_model=PriceResponse | None)
async def get_prices_by_date(ticker: str, timestamp: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await price_service.get_prices_by_date(db=db, ticker=ticker, timestamp=timestamp)
