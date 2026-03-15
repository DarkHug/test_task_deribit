from fastapi import FastAPI
from app.api.routes import router as api_router
from app.db.base import Base
from app.db.session import engine
import app.models

app = FastAPI(
    title="Test Task API",
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(api_router)
