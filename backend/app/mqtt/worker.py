"""
MQTT Worker

Consumes telemetry messages from the queue,
stores them in the database,
then executes the complete AI pipeline.

Workflow

MQTT
    ↓
Queue
    ↓
Telemetry Service
    ↓
AI Orchestrator
        ↓
    Prediction
        ↓
    Notification
        ↓
    WebSocket
"""

import asyncio
from typing import Any

from app.core.logging import logger
from app.database.session import SessionLocal

from app.services.telemetry_service import telemetry_service
from app.orchestrator import ai_orchestrator
from app.iot.telemetry_parser import telemetry_parser


class MQTTWorker:
    """
    Background worker for processing MQTT telemetry.
    """

    def __init__(self):
        self.running = False
        self.task: asyncio.Task | None = None

    # =====================================================
    # Start
    # =====================================================

    async def start(self):

        if self.running:
            return

        logger.info("Starting MQTT Worker...")

        self.running = True
        self.task = asyncio.create_task(self.run())

    # =====================================================
    # Stop
    # =====================================================

    async def stop(self):

        logger.info("Stopping MQTT Worker...")

        self.running = False

        from .queue import telemetry_queue

        telemetry_queue.put_nowait(None)

        if self.task:
            await self.task

    # =====================================================
    # Main Loop
    # =====================================================

    async def run(self):

        from .queue import telemetry_queue

        while self.running:

            payload: dict[str, Any] | None = await telemetry_queue.get()

            if payload is None:
                telemetry_queue.task_done()
                break

            try:

                # -----------------------------------------
                # Parse Telemetry
                # -----------------------------------------

                telemetry = telemetry_parser.parse(payload)

                async with SessionLocal() as db:

                    # -----------------------------------------
                    # Save Telemetry
                    # -----------------------------------------

                    await telemetry_service.create_telemetry(
                        db=db,
                        data=telemetry,
                    )

                    logger.info(
                        "Telemetry Saved (Node=%s, Cluster=%s)",
                        telemetry.node_id,
                        telemetry.cluster_id,
                    )

                    # -----------------------------------------
                    # Execute AI Pipeline
                    # -----------------------------------------

                    prediction = await ai_orchestrator.process(
                        db=db,
                        cluster_id=telemetry.cluster_id,
                        node_id=telemetry.node_id,
                    )

                    logger.info(
                        "Prediction Completed (Node=%s, Risk=%s)",
                        telemetry.node_id,
                        prediction.risk_score,
                    )

            except Exception as e:

                logger.exception(
                    "MQTT Worker Processing Failed: %s",
                    str(e),
                )

            finally:

                telemetry_queue.task_done()


mqtt_worker = MQTTWorker()