"""
WebSocket Connection Manager

Handles:

- Active Connections
- Connect
- Disconnect
- Broadcast
- Send Personal Message
"""

from fastapi import WebSocket
from app.core.logging import logger


class ConnectionManager:
    """
    WebSocket Connection Manager.
    """

    def __init__(self):

        self.active_connections: list[WebSocket] = []

    # -------------------------------------------------

    async def connect(
        self,
        websocket: WebSocket,
    ):

        await websocket.accept()

        self.active_connections.append(websocket)

        logger.info(
            f"WebSocket Connected | Total={len(self.active_connections)}"
        )

    # -------------------------------------------------

    def disconnect(
        self,
        websocket: WebSocket,
    ):

        if websocket in self.active_connections:

            self.active_connections.remove(websocket)

        logger.info(
            f"WebSocket Disconnected | Total={len(self.active_connections)}"
        )

    # -------------------------------------------------

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket,
    ):

        await websocket.send_json(message)

    # -------------------------------------------------

    async def broadcast(
        self,
        message: dict,
    ):

        disconnected = []

        for connection in self.active_connections:

            try:

                await connection.send_json(message)

            except Exception:

                disconnected.append(connection)

        for connection in disconnected:

            self.disconnect(connection)

    # -------------------------------------------------

    @property
    def total_connections(self):

        return len(self.active_connections)


manager = ConnectionManager()