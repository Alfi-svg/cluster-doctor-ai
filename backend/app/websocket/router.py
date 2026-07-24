"""
WebSocket Router

Endpoint:

ws://localhost:8000/ws
"""

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.core.logging import logger
from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    """
    Main WebSocket endpoint.
    """

    await manager.connect(websocket)

    try:

        while True:

            data = await websocket.receive_text()

            logger.info(
                f"WebSocket Message: {data}"
            )

            await manager.send_personal_message(
                {
                    "type": "heartbeat",
                    "message": "connected",
                    "echo": data,
                },
                websocket,
            )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

    except Exception as e:

        logger.exception(e)

        manager.disconnect(websocket)