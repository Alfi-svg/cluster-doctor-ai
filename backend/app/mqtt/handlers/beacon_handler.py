"""
Beacon MQTT Handler

Processes beacon requests coming from ESP32 devices.
"""

from __future__ import annotations

from app.core.logging import logger
from app.mqtt.publisher import mqtt_publisher
from app.mqtt.topics import BEACON_RESPONSE_TOPIC


class BeaconHandler:
    """
    Handle Smart Beacon requests.
    """

    async def handle(
        self,
        payload: dict,
    ) -> None:

        try:

            logger.info(
                f"Beacon Request Received -> {payload}"
            )

            response = {
                "device_id": payload.get("device_id"),
                "status": "received",
                "message": "Beacon command accepted",
            }

            mqtt_publisher.publish(
                BEACON_RESPONSE_TOPIC,
                response,
            )

        except Exception as e:

            logger.exception(
                f"Beacon Handler Error: {e}"
            )


beacon_handler = BeaconHandler()