from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Test Task API",
)

app.include_router(api_router)
