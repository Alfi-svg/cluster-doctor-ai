"""
Cluster AI Doctor AI Orchestrator

Central AI Workflow

Telemetry
    ↓
Prediction
    ↓
Healing
    ↓
Reality Verification
    ↓
Notification
    ↓
MQTT
    ↓
WebSocket
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger

from app.orchestrator.prediction_pipeline import PredictionPipeline
from app.orchestrator.notification_pipeline import NotificationPipeline
from app.orchestrator.websocket_pipeline import WebsocketPipeline
from app.orchestrator.mqtt_pipeline import MQTTPipeline
from app.orchestrator.healing_pipeline import healing_pipeline
from app.orchestrator.reality_pipeline import reality_pipeline


class AIOrchestrator:

    def __init__(self):

        self.prediction_pipeline = PredictionPipeline()

        self.healing_pipeline = healing_pipeline

        self.reality_pipeline = reality_pipeline

        self.notification_pipeline = NotificationPipeline()

        self.websocket_pipeline = WebsocketPipeline()

        self.mqtt_pipeline = MQTTPipeline()

    async def process(
        self,
        db: AsyncSession,
        cluster_id: int,
        node_id: int,
    ):
        """
        Complete AI workflow.
        """

        logger.info(
            f"[AI] Processing node={node_id}"
        )

        # =====================================================
        # Prediction
        # =====================================================

        prediction = await self.prediction_pipeline.run(
            db=db,
            cluster_id=cluster_id,
            node_id=node_id,
        )

        # =====================================================
        # Healing
        # =====================================================

        healing = await self.healing_pipeline.run(
            db=db,
            prediction=prediction,
        )

        # =====================================================
        # Temporary Telemetry
        # TODO:
        # Replace with TelemetryRepository.get_latest()
        # =====================================================

        telemetry = {
            "cpu": 45,
            "memory": 35,
            "temperature": 52,
        }

        # =====================================================
        # Reality Verification
        # =====================================================

        reality = await self.reality_pipeline.run(
            db=db,
            node_id=node_id,
            telemetry=telemetry,
        )

        # =====================================================
        # Notification
        # =====================================================

        notification = await self.notification_pipeline.run(
            db=db,
            prediction=prediction,
        )

        # =====================================================
        # MQTT
        # =====================================================

        await self.mqtt_pipeline.publish(
            prediction=prediction,
            notification=notification,
        )

        # =====================================================
        # WebSocket
        # =====================================================

        await self.websocket_pipeline.broadcast(
            prediction=prediction,
            notification=notification,
        )

        logger.info(
            f"[AI] Completed node={node_id}"
        )

        return {
            "prediction": prediction,
            "healing": healing,
            "reality": reality,
            "notification": notification,
        }