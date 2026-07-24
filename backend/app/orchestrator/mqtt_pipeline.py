"""
MQTT Pipeline

Publishes AI events to:

- Smart Beacon
- IoT Alert Device
"""

from datetime import datetime

from app.models.notification import Notification
from app.models.prediction import Prediction

from app.mqtt.publisher import mqtt_publisher

from app.mqtt.topics import (
    BEACON_RESPONSE_TOPIC,
    IOT_STATUS_TOPIC,
)


class MQTTPipeline:

    async def publish(
        self,
        prediction: Prediction,
        notification: Notification | None = None,
    ):

        # ------------------------------------
        # AI Level
        # ------------------------------------

        level = "healthy"

        if prediction.risk_score >= 90:

            level = "critical"

        elif prediction.risk_score >= 75:

            level = "warning"

        # ------------------------------------
        # Existing Beacon Payload
        # ------------------------------------

        beacon_payload = {

            "event": "prediction",

            "timestamp": datetime.utcnow().isoformat(),

            "node_id": prediction.node_id,

            "cluster_id": prediction.cluster_id,

            "risk_score": prediction.risk_score,

            "confidence": prediction.confidence,

            "prediction": prediction.predicted_label,

            "recommendation": prediction.recommendation,

            "level": level,

            "notification": None,

        }

        if notification:

            beacon_payload["notification"] = {

                "title": notification.title,

                "message": notification.message,

                "threat_level": str(
                    notification.threat_level
                ),

            }

        # ------------------------------------
        # Publish Beacon
        # ------------------------------------

        mqtt_publisher.publish(

            topic=BEACON_RESPONSE_TOPIC,

            payload=beacon_payload,

        )

        # ------------------------------------
        # IoT Alert Payload
        # ------------------------------------

        if prediction.risk_score >= 75:

            iot_payload = {

                "status": "ALERT",

                "risk": level.upper(),

                "score": prediction.risk_score,

                "cluster": str(
                    prediction.cluster_id
                ),

                "node": str(
                    prediction.node_id
                ),

                "message": prediction.predicted_label,

                "timestamp": datetime.utcnow().isoformat(),

            }

        else:

            iot_payload = {

                "status": "SAFE",

                "risk": "LOW",

                "score": prediction.risk_score,

                "cluster": str(
                    prediction.cluster_id
                ),

                "node": str(
                    prediction.node_id
                ),

                "message": "Cluster Healthy",

                "timestamp": datetime.utcnow().isoformat(),

            }

        mqtt_publisher.publish(

            topic=IOT_STATUS_TOPIC,

            payload=iot_payload,

        )