from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, Depends

from src.model import test_connection, get_service
from src.api import private_api_router, public_api_router
from src.view import view_router
from src.ws import handle_websocket_notification


@asynccontextmanager
async def lifespan(app: FastAPI):
    test_connection()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(public_api_router)
app.include_router(private_api_router)
app.include_router(view_router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, service=Depends(get_service)):
    await handle_websocket_notification(websocket=websocket, service=service)
