from fastapi import APIRouter, Depends, WebSocket
from loguru import logger

from src.security import required_login
from src.model import Service

private_ws_router = APIRouter(prefix="/ws", dependencies=[Depends(required_login)])


def get_service():
    return Service()

@private_ws_router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, service: Service = Depends(get_service)):
    await websocket.accept()
    try:
        async for change in service.watch_collection():
            logger.debug(change)
            await websocket.send_json(change)
    except Exception as e:
        logger.error(e)
    finally:
        await websocket.close()