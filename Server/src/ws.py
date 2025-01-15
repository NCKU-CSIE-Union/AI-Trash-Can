from fastapi import WebSocket, HTTPException, status, WebSocketDisconnect
from loguru import logger
from pymongo import AsyncMongoClient

from src.security import is_valid_token
from src.config import server_config
from src.schema import SystemEvent, NewRecordEvent


async def handle_websocket_notification(
    websocket: WebSocket,
    service,
):
    await websocket.accept()
    # token = websocket.cookies.get("auth")
    # if not token or not is_valid_token(token):
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    #     return
    await websocket.send_json(SystemEvent(message="Connected").model_dump())
    try:
        async with AsyncMongoClient(server_config.mongo.MONGO_URI) as client:
            db = client[server_config.mongo.MONGO_DB]
            collection = db[server_config.mongo.MONGO_COLLECTION]
            await websocket.send_json(
                SystemEvent(message="Watching for changes").model_dump()
            )
            async with await collection.watch() as change_stream:
                async for change in change_stream:
                    logger.debug(change)
                    await websocket.send_json(
                        NewRecordEvent(**change["fullDocument"]).model_dump(mode="json")
                    )
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(e)
    finally:
        await websocket.close()
