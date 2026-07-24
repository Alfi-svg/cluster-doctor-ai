"""
MQTT Bridge

Provides a simple interface between
the IoT layer and MQTT.
"""

from __future__ import annotations

from app.core.logging import logger

from app.mqtt.publisher import mqtt_publisher
from app.mqtt.topics import (
    COMMAND_TOPIC,
    AI_ALERT_TOPIC,
)


class MQTTBridge:

    def send_command(
        self,
        command: dict,
    ) -> None:

        mqtt_publisher.publish(
            COMMAND_TOPIC,
            command,
        )

        logger.info(
            f"ESP32 Command Sent -> {command}"
        )

    def send_alert(
        self,
        alert: dict,
    ) -> None:

        mqtt_publisher.publish(
            AI_ALERT_TOPIC,
            alert,
        )

        logger.info(
            f"AI Alert Sent -> {alert}"
        )


mqtt_bridge = MQTTBridge()