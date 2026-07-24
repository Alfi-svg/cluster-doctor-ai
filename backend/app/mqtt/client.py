import aiomqtt

from app.core.config import settings

mqtt_client = aiomqtt.Client(
    hostname=settings.MQTT_HOST,
    port=settings.MQTT_PORT,
)