"""
IoT Service

Provides methods for publishing
SAFE / ALERT events to IoT devices.
"""

from app.iot.schemas import IoTPayload
from app.iot.mqtt_adapter import iot_mqtt_adapter


class IoTService:

    # =====================================================
    # SAFE
    # =====================================================

    async def safe(self):

        payload = IoTPayload(

            status="SAFE",

            risk="LOW",

            score=0,

            message="Cluster Healthy",

        )

        iot_mqtt_adapter.publish(
            payload
        )

        return payload.model_dump()

    # =====================================================
    # ALERT
    # =====================================================

    async def alert(

        self,

        risk: str,

        score: float,

        message: str,

        cluster: str = "",

        node: str = "",

    ):

        payload = IoTPayload(

            status="ALERT",

            risk=risk,

            score=score,

            message=message,

            cluster=cluster,

            node=node,

        )

        iot_mqtt_adapter.publish(
            payload
        )

        return payload.model_dump()

    # =====================================================
    # CUSTOM
    # =====================================================

    async def custom(
        self,
        payload: IoTPayload,
    ):

        iot_mqtt_adapter.publish(
            payload
        )

        return payload.model_dump()


iot_service = IoTService()