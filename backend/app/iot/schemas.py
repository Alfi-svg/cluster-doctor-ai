"""
IoT Payload Schema
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class IoTPayload(BaseModel):

    status: Literal[
        "SAFE",
        "ALERT",
    ]

    risk: str = "LOW"

    score: float = 0

    cluster: str = ""

    node: str = ""

    message: str = ""

    timestamp: str = datetime.utcnow().isoformat()