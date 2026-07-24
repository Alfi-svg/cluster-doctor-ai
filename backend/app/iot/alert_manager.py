"""
IoT Alert Manager

Central alert dispatcher.

Prediction
    ↓
AlertManager
    ├── MQTT
    ├── Notification
    ├── WebSocket
    └── Future SMS / Email
"""

from datetime import datetime

from app.iot.schemas import IoTPayload
from app.iot.mqtt_adapter import iot_mqtt_adapter


class AlertManager:

    # =====================================================
    # SAFE
    # =====================================================

    def safe(
        self,
        cluster: str = "",
        node: str = "",
        message: str = "Cluster Healthy",
    ):

        payload = IoTPayload(

            status="SAFE",

            risk="LOW",

            score=0,

            cluster=cluster,

            node=node,

            message=message,

            timestamp=datetime.utcnow().isoformat(),

        )

        iot_mqtt_adapter.publish(
            payload
        )

    # =====================================================
    # ALERT
    # =====================================================

    def alert(
        self,
        risk: str,
        score: float,
        message: str,
        cluster: str,
        node: str,
    ):

        payload = IoTPayload(

            status="ALERT",

            risk=risk,

            score=score,

            cluster=cluster,

            node=node,

            message=message,

            timestamp=datetime.utcnow().isoformat(),

        )

        iot_mqtt_adapter.publish(
            payload
        )


alert_manager = AlertManager()