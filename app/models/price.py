from sqlalchemy import String, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    price: Mapped[float] = mapped_column(Numeric)
    timestamp: Mapped[int] = mapped_column(BigInteger, index=True)
