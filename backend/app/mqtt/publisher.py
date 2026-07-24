"""
MQTT Publisher

Publishes AI events to IoT devices.

Used by:

- ESP32 Smart Rack Beacon
- Future IoT Devices
"""

import json

import paho.mqtt.client as mqtt

from app.core.config import settings
from app.core.logging import logger


class MQTTPublisher:
    """
    MQTT Publisher
    """

    def __init__(self):

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.connected = False

    # =====================================================
    # Connect
    # =====================================================

    def connect(self):

        if self.connected:
            return

        logger.info("Connecting MQTT Publisher...")

        self.client.connect(
            host=settings.MQTT_HOST,
            port=settings.MQTT_PORT,
            keepalive=60,
        )

        self.client.loop_start()

        self.connected = True

        logger.info("MQTT Publisher Connected")

    # =====================================================
    # Disconnect
    # =====================================================

    def disconnect(self):

        if not self.connected:
            return

        logger.info("Stopping MQTT Publisher...")

        self.client.loop_stop()

        self.client.disconnect()

        self.connected = False

    # =====================================================
    # Publish
    # =====================================================

    def publish(
        self,
        topic: str,
        payload: dict,
    ):

        if not self.connected:

            self.connect()

        self.client.publish(
            topic,
            json.dumps(payload),
            qos=1,
        )

        logger.info(
            f"Published MQTT Topic: {topic}"
        )


mqtt_publisher = MQTTPublisher()