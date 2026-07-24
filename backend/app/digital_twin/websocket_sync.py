"""
Digital Twin WebSocket Manager

Responsible for managing all websocket connections
and broadcasting Digital Twin updates.
"""

from __future__ import annotations

import json
from fastapi import WebSocket


class WebSocketManager:

    def __init__(self):

        self.connections: list[WebSocket] = []

    # --------------------------------------------------

    async def connect(
        self,
        websocket: WebSocket,
    ):

        await websocket.accept()

        self.connections.append(websocket)

    # --------------------------------------------------

    def disconnect(
        self,
        websocket: WebSocket,
    ):

        if websocket in self.connections:

            self.connections.remove(websocket)

    # --------------------------------------------------

    async def send(
        self,
        websocket: WebSocket,
        data: dict,
    ):

        await websocket.send_text(
            json.dumps(data)
        )

    # --------------------------------------------------

    async def broadcast(
        self,
        data: dict,
    ):

        dead_connections = []

        for connection in self.connections:

            try:

                await connection.send_text(
                    json.dumps(data)
                )

            except Exception:

                dead_connections.append(connection)

        for connection in dead_connections:

            self.disconnect(connection)

    # --------------------------------------------------

    @property
    def total_connections(self):

        return len(self.connections)


websocket_manager = WebSocketManager()