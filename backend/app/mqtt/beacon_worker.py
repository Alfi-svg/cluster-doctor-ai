"""
Beacon Worker

Processes ESP32 beacon requests and returns
the latest AI prediction to the Smart Rack Beacon.
"""

import asyncio
from datetime import datetime

from app.core.logging import logger
from app.database.session import SessionLocal

from app.mqtt.beacon_queue import beacon_queue
from app.mqtt.publisher import mqtt_publisher
from app.mqtt.topics import BEACON_RESPONSE_TOPIC

from app.services.prediction_service import prediction_service


class BeaconWorker:
    """
    Processes ESP32 beacon requests.
    """

    def __init__(self):

        self.task: asyncio.Task | None = None
        self.running = False

    # =====================================================
    # Start
    # =====================================================

    async def start(self):

        if self.running:
            return

        self.running = True

        self.task = asyncio.create_task(self.run())

        logger.info("Beacon Worker Started")

    # =====================================================
    # Stop
    # =====================================================

    async def stop(self):

        self.running = False

        if self.task:

            self.task.cancel()

            try:
                await self.task
            except asyncio.CancelledError:
                pass

        logger.info("Beacon Worker Stopped")

    # =====================================================
    # Main Loop
    # =====================================================

    async def run(self):

        while self.running:

            request = await beacon_queue.get()

            try:

                await self.process(request)

            except Exception:

                logger.exception(
                    "Beacon Worker Processing Error"
                )

            finally:

                beacon_queue.task_done()

    # =====================================================
    # Process Request
    # =====================================================

    async def process(
        self,
        request: dict,
    ):

        logger.info(f"Beacon Request: {request}")

        request_id = request.get("request_id")
        node_id = request.get("node_id")

        # --------------------------------------------
        # Validate
        # --------------------------------------------

        if node_id is None:

            mqtt_publisher.publish(
                topic=BEACON_RESPONSE_TOPIC,
                payload={
                    "request_id": request_id,
                    "status": "error",
                    "message": "node_id is required",
                    "timestamp": datetime.utcnow().isoformat(),
                },
            )

            return

        # --------------------------------------------
        # Database
        # --------------------------------------------

        async with SessionLocal() as db:

            prediction = await prediction_service.get_latest_prediction(
                db=db,
                node_id=node_id,
            )

            # ----------------------------------------
            # Not Found
            # ----------------------------------------

            if prediction is None:

                mqtt_publisher.publish(
                    topic=BEACON_RESPONSE_TOPIC,
                    payload={
                        "request_id": request_id,
                        "status": "not_found",
                        "node_id": node_id,
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                )

                logger.warning(
                    f"No prediction found for node {node_id}"
                )

                return

            # ----------------------------------------
            # Success
            # ----------------------------------------

            response = {

                "request_id": request_id,

                "status": "success",

                "timestamp": datetime.utcnow().isoformat(),

                "cluster_id": prediction.cluster_id,

                "node_id": prediction.node_id,

                "risk_score": prediction.risk_score,

                "confidence": prediction.confidence,

                "probability": prediction.probability,

                "prediction": prediction.predicted_label,

                "recommendation": prediction.recommendation,

                "explanation": prediction.explanation,
            }

            mqtt_publisher.publish(
                topic=BEACON_RESPONSE_TOPIC,
                payload=response,
            )

            logger.info(
                f"Beacon Response Sent -> Node {node_id}"
            )


beacon_worker = BeaconWorker()