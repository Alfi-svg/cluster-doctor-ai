"""
MQTT Dispatcher

Routes incoming MQTT messages
to the appropriate handler.
"""

from app.core.logging import logger

from app.mqtt.topics import (
    TELEMETRY_TOPIC,
    BEACON_REQUEST_TOPIC,
)

from app.mqtt.handlers.telemetry_handler import telemetry_handler
from app.mqtt.handlers.beacon_handler import beacon_handler


class MQTTDispatcher:
    """
    Dispatch incoming MQTT messages
    based on topic.
    """

    async def dispatch(
        self,
        topic: str,
        payload: dict,
    ) -> None:

        logger.info(f"MQTT Dispatch -> {topic}")

        if topic == TELEMETRY_TOPIC:

            await telemetry_handler.handle(payload)
            return

        if topic == BEACON_REQUEST_TOPIC:

            await beacon_handler.handle(payload)
            return

        logger.warning(
            f"No handler registered for topic: {topic}"
        )


mqtt_dispatcher = MQTTDispatcher()