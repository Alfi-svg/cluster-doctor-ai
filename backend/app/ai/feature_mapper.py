from typing import Any


class FeatureMapper:
    """
    Converts telemetry data into the feature format
    expected by the trained AI models.
    """

    # =====================================================
    # Failure Prediction
    # =====================================================

    @staticmethod
    def failure_features(
        telemetry: dict[str, Any],
    ) -> dict:

        return {
            "gpu_temperature": telemetry.get(
                "gpu_temperature", 0
            ),

            "fan_speed": telemetry.get(
                "fan_speed",
                2200,
            ),

            "power_draw": telemetry.get(
                "gpu_power",
                telemetry.get("power_draw", 0),
            ),

            "cpu_utility": telemetry.get(
                "cpu_usage",
                telemetry.get("cpu_utility", 0),
            ),
        }

    # =====================================================
    # Experiment Guardian
    # =====================================================

    @staticmethod
    def guardian_features(
        telemetry: dict[str, Any],
    ) -> dict:

        return {

            "gpu_memory_util": telemetry.get(
                "gpu_memory_usage",
                0,
            ),

            "cpu_memory_util": telemetry.get(
                "ram_usage",
                0,
            ),

            "allocated_cores": telemetry.get(
                "allocated_cores",
                8,
            ),

            "batch_size": telemetry.get(
                "batch_size",
                32,
            ),

            "epoch_progress": telemetry.get(
                "epoch_progress",
                50,
            ),
        }

    # =====================================================
    # Security Detection
    # =====================================================

    @staticmethod
    def security_features(
        telemetry: dict[str, Any],
    ) -> dict:

        network_in = telemetry.get("network_in", 0)
        network_out = telemetry.get("network_out", 0)

        return {

            "dur": telemetry.get("duration", 1),

            "spkts": int(network_out / 100),

            "dpkts": int(network_in / 100),

            "sbytes": network_out,

            "dbytes": network_in,

            "rate": telemetry.get("latency", 0),

            "sttl": 64,

            "dttl": 64,

            "sload": network_out,

            "dload": network_in,

            "tcprtt": telemetry.get(
                "latency",
                0,
            ),

            "synack": telemetry.get(
                "latency",
                0,
            ) / 2,

            "ackdat": telemetry.get(
                "latency",
                0,
            ) / 2,
        }