"""
Telemetry MQTT Handler

Receives telemetry payloads from MQTT and
synchronizes the Digital Twin.
"""

from __future__ import annotations

from app.core.logging import logger
from app.digital_twin.state_sync import state_sync


class TelemetryHandler:
    """
    Handle telemetry messages received from MQTT.
    """

    async def handle(self, payload: dict) -> None:

        try:

            cluster_id = payload.get("cluster_id")
            node_id = payload.get("node_id")

            if not cluster_id or not node_id:

                logger.warning(
                    "Telemetry payload missing cluster_id or node_id."
                )
                return

            await state_sync.sync_telemetry(
                cluster_id=cluster_id,
                node_id=node_id,
                telemetry=payload,
            )

            logger.info(
                f"Telemetry synced -> {cluster_id}/{node_id}"
            )

        except Exception as e:

            logger.exception(
                f"Telemetry Handler Error: {e}"
            )


telemetry_handler = TelemetryHandler()