from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
