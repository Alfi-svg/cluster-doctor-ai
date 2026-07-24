"""
WebSocket Pipeline

Broadcasts AI events to all connected dashboard clients.
"""

from datetime import datetime

from app.models.notification import Notification
from app.models.prediction import Prediction
from app.websocket.manager import manager


class WebsocketPipeline:
    """
    Sends real-time events to dashboard clients.
    """

    async def broadcast(
        self,
        prediction: Prediction,
        notification: Notification | None = None,
    ) -> None:
        """
        Broadcast prediction + notification.
        """

        payload = {
            "event": "prediction",
            "timestamp": datetime.utcnow().isoformat(),

            "prediction": {
                "id": prediction.id,
                "cluster_id": prediction.cluster_id,
                "node_id": prediction.node_id,
                "risk_score": prediction.risk_score,
                "confidence": prediction.confidence,
                "probability": prediction.probability,
                "prediction_type": str(prediction.prediction_type),
                "predicted_label": prediction.predicted_label,
                "recommendation": prediction.recommendation,
                "status": str(prediction.status),
            },

            "notification": None,
        }

        if notification:

            payload["notification"] = {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "category": notification.category,
                "threat_level": str(notification.threat_level),
                "status": str(notification.status),
            }

        await manager.broadcast(payload)