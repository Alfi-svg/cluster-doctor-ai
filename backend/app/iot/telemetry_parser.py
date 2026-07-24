"""
Telemetry Parser

Converts raw IoT telemetry into the backend
TelemetryCreate schema.
"""

from __future__ import annotations

from app.core.logging import logger
from app.schemas.telemetry import TelemetryCreate


class TelemetryParser:
    """
    Parse raw IoT payload into TelemetryCreate.
    """

    def parse(
        self,
        payload: dict,
    ) -> TelemetryCreate:

        try:

            telemetry = TelemetryCreate(

                cluster_id=payload["cluster_id"],
                node_id=payload["node_id"],

                cpu_usage=payload.get("cpu_usage", 0.0),
                cpu_temperature=payload.get("cpu_temperature", 0.0),
                cpu_frequency=payload.get("cpu_frequency", 0.0),

                gpu_usage=payload.get("gpu_usage", 0.0),
                gpu_temperature=payload.get("gpu_temperature", 0.0),
                gpu_memory_usage=payload.get("gpu_memory_usage", 0.0),
                gpu_power=payload.get("gpu_power", 0.0),

                ram_usage=payload.get("ram_usage", 0.0),
                swap_usage=payload.get("swap_usage", 0.0),

                disk_usage=payload.get("disk_usage", 0.0),
                disk_read_speed=payload.get("disk_read_speed", 0.0),
                disk_write_speed=payload.get("disk_write_speed", 0.0),

                network_in=payload.get("network_in", 0.0),
                network_out=payload.get("network_out", 0.0),

                latency=payload.get("latency", 0.0),
                packet_loss=payload.get("packet_loss", 0.0),
            )

            return telemetry

        except Exception as e:

            logger.exception(
                f"Telemetry parsing failed: {e}"
            )

            raise


telemetry_parser = TelemetryParser()