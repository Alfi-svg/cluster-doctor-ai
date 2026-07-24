"""
MQTT Subscriber

Receives MQTT messages from compute nodes
and ESP32 devices, then routes them to the
appropriate async queue.
"""

import asyncio
import json

import paho.mqtt.client as mqtt

from app.core.config import settings
from app.core.logging import logger

from app.mqtt.queue import telemetry_queue
from app.mqtt.beacon_queue import beacon_queue
from app.mqtt.topics import (
    TELEMETRY_TOPIC,
    BEACON_REQUEST_TOPIC,
)
from app.iot.heartbeat import heartbeat_monitor

class MQTTSubscriber:
    """
    MQTT Subscriber
    """

    def __init__(self):

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.loop: asyncio.AbstractEventLoop | None = None

    # =====================================================
    # Connect
    # =====================================================

    def connect(self):

        logger.info("Connecting to MQTT Broker...")

        self.client.connect(
            host=settings.MQTT_HOST,
            port=settings.MQTT_PORT,
            keepalive=60,
        )

    # =====================================================
    # Start
    # =====================================================

    def start(self):

        logger.info("Starting MQTT Subscriber...")

        self.loop = asyncio.get_running_loop()

        self.client.loop_start()

    # =====================================================
    # Stop
    # =====================================================

    def stop(self):

        logger.info("Stopping MQTT Subscriber...")

        self.client.loop_stop()
        self.client.disconnect()

    # =====================================================
    # Connected
    # =====================================================

    def on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):

        logger.info("MQTT Connected Successfully")

        client.subscribe(TELEMETRY_TOPIC)
        logger.info(f"Subscribed -> {TELEMETRY_TOPIC}")

        client.subscribe(BEACON_REQUEST_TOPIC)
        logger.info(f"Subscribed -> {BEACON_REQUEST_TOPIC}")

    # =====================================================
    # Disconnected
    # =====================================================

    def on_disconnect(
        self,
        client,
        userdata,
        disconnect_flags,
        reason_code,
        properties,
    ):

        logger.warning(
            f"MQTT Disconnected (reason={reason_code})"
        )

    # =====================================================
    # Message Received
    # =====================================================

    def on_message(
        self,
        client,
        userdata,
        message,
    ):

        if self.loop is None:

            logger.error("Async event loop is not initialized.")

            return

        try:

            payload = json.loads(
                message.payload.decode("utf-8")
            )

        except json.JSONDecodeError:

            logger.exception("Invalid JSON payload received.")

            return

        topic = message.topic

        logger.info(f"MQTT [{topic}] -> {payload}")
        if topic == TELEMETRY_TOPIC:
          heartbeat_monitor.update()

        try:

            if topic == TELEMETRY_TOPIC:

                self.loop.call_soon_threadsafe(
                    telemetry_queue.put_nowait,
                    payload,
                )

                return

            if topic == BEACON_REQUEST_TOPIC:

                self.loop.call_soon_threadsafe(
                    beacon_queue.put_nowait,
                    payload,
                )

                return

            logger.warning(
                f"Unhandled MQTT topic: {topic}"
            )

        except Exception as e:

            logger.exception(
                f"MQTT Subscriber Error: {e}"
            )


mqtt_subscriber = MQTTSubscriber()