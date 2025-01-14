from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.model import test_connection
from src.api import private_api_router, public_api_router
from src.view import view_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    test_connection()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(public_api_router)
app.include_router(private_api_router)
app.include_router(view_router)