"""
IoT MQTT Adapter
"""

from app.iot.schemas import IoTPayload
from app.mqtt.publisher import mqtt_publisher
from app.mqtt.topics import IOT_STATUS_TOPIC


class IoTMQTTAdapter:

    def publish(
        self,
        payload: IoTPayload,
    ):

        mqtt_publisher.publish(

            IOT_STATUS_TOPIC,

            payload.model_dump(),

        )


iot_mqtt_adapter = IoTMQTTAdapter()