"""
ESP32 Heartbeat Monitor
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.core.logging import logger


class HeartbeatMonitor:
    """
    Tracks the last heartbeat received from the ESP32.
    """

    def __init__(self):

        self.last_seen: datetime | None = None

    def update(self) -> None:

        self.last_seen = datetime.utcnow()

        logger.info("ESP32 heartbeat updated.")

    def is_online(self) -> bool:

        if self.last_seen is None:
            return False

        return datetime.utcnow() - self.last_seen < timedelta(seconds=15)

    def status(self) -> dict:

        return {
            "online": self.is_online(),
            "last_seen": self.last_seen,
        }


heartbeat_monitor = HeartbeatMonitor()