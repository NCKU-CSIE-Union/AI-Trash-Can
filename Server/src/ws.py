from fastapi import WebSocket, status, WebSocketDisconnect
from loguru import logger
import asyncio

from src.security import is_valid_token
from src.schema import SystemEvent, NewRecordEvent, Filters
from src.model import Service


async def handle_websocket_notification(
    websocket: WebSocket,
    service: Service,
):
    await websocket.accept()
    token = websocket.cookies.get("auth")
    if not token or not is_valid_token(token):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await websocket.send_json(SystemEvent(message="Connected").model_dump())
    try:
        while True:
            new_records = service.read_records(Filters(seen=False))
            new_ids = []
            for record in new_records:
                new_ids.append(record["_id"])
                logger.debug(f"sending new record: {record}")
                await websocket.send_json(
                    NewRecordEvent(**record).model_dump(mode="json")
                )
                await asyncio.sleep(0.1)
            service.mark_as_seen(new_ids)
            logger.debug(f"marked {new_ids} as seen")
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(e)
    finally:
        await websocket.close()
