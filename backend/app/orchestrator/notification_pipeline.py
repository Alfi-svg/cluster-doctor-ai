"""
Notification Pipeline
"""

from app.database.enums import ThreatLevel
from app.models.prediction import Prediction
from app.repositories.cluster_repository import cluster_repository
from app.schemas.notification import NotificationCreate
from app.services.notification_service import notification_service


class NotificationPipeline:

    async def run(
        self,
        db,
        prediction: Prediction,
    ):

        cluster = await cluster_repository.get(
            db,
            prediction.cluster_id,
        )

        if cluster is None:
            return None

        threat = ThreatLevel.LOW

        if prediction.risk_score >= 90:
            threat = ThreatLevel.CRITICAL

        elif prediction.risk_score >= 75:
            threat = ThreatLevel.HIGH

        elif prediction.risk_score >= 50:
            threat = ThreatLevel.MEDIUM

        notification = NotificationCreate(

            user_id=cluster.owner_id,

            cluster_id=prediction.cluster_id,

            node_id=prediction.node_id,

            prediction_id=prediction.id,

            title="AI Risk Alert",

            message=prediction.recommendation,

            category="Prediction",

            threat_level=threat,
        )

        return await notification_service.create_notification(
            db,
            notification,
        )