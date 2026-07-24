"""
Twin Reality Checker

Compares the Digital Twin snapshot against
the latest real telemetry.

This module powers the Hackathon
Twin Reality Verification feature.
"""

from __future__ import annotations

from app.digital_twin.snapshot import snapshot_manager
from app.digital_twin.twin_gap import twin_gap


class RealityChecker:

    # =====================================================
    # Compare CPU
    # =====================================================

    def compare_cpu(
        self,
        node_id: str,
        actual_cpu: float,
    ) -> dict:

        snapshot = snapshot_manager.get(node_id)

        if snapshot is None:

            return {
                "success": False,
                "message": "Snapshot not found.",
            }

        predicted = snapshot.cpu_usage

        gap = twin_gap.percentage(
            predicted,
            actual_cpu,
        )

        accuracy = twin_gap.accuracy(
            predicted,
            actual_cpu,
        )

        return {
            "success": True,
            "metric": "CPU",
            "predicted": predicted,
            "actual": actual_cpu,
            "gap": gap,
            "accuracy": accuracy,
            "status": (
                "Healthy"
                if gap < 10
                else "Warning"
            ),
        }

    # =====================================================
    # Compare RAM
    # =====================================================

    def compare_ram(
        self,
        node_id: str,
        actual_ram: float,
    ) -> dict:

        snapshot = snapshot_manager.get(node_id)

        if snapshot is None:

            return {
                "success": False,
                "message": "Snapshot not found.",
            }

        predicted = snapshot.ram_usage

        gap = twin_gap.percentage(
            predicted,
            actual_ram,
        )

        accuracy = twin_gap.accuracy(
            predicted,
            actual_ram,
        )

        return {
            "success": True,
            "metric": "RAM",
            "predicted": predicted,
            "actual": actual_ram,
            "gap": gap,
            "accuracy": accuracy,
            "status": (
                "Healthy"
                if gap < 10
                else "Warning"
            ),
        }

    # =====================================================
    # Compare Temperature
    # =====================================================

    def compare_temperature(
        self,
        node_id: str,
        actual_temperature: float,
    ) -> dict:

        snapshot = snapshot_manager.get(node_id)

        if snapshot is None:

            return {
                "success": False,
                "message": "Snapshot not found.",
            }

        predicted = snapshot.cpu_temperature

        gap = twin_gap.percentage(
            predicted,
            actual_temperature,
        )

        accuracy = twin_gap.accuracy(
            predicted,
            actual_temperature,
        )

        return {
            "success": True,
            "metric": "Temperature",
            "predicted": predicted,
            "actual": actual_temperature,
            "gap": gap,
            "accuracy": accuracy,
            "status": (
                "Healthy"
                if gap < 10
                else "Warning"
            ),
        }

    # =====================================================
    # Full Comparison
    # =====================================================

    def compare(
        self,
        node_id: str,
        telemetry: dict,
    ) -> dict:

        cpu = self.compare_cpu(
            node_id,
            float(
                telemetry.get("cpu", 0)
            ),
        )

        ram = self.compare_ram(
            node_id,
            float(
                telemetry.get("memory", 0)
            ),
        )

        temperature = self.compare_temperature(
            node_id,
            float(
                telemetry.get("temperature", 0)
            ),
        )

        if not cpu["success"]:

            return cpu

        average_gap = round(
            (
                cpu["gap"]
                + ram["gap"]
                + temperature["gap"]
            )
            / 3,
            2,
        )

        average_accuracy = round(
            (
                cpu["accuracy"]
                + ram["accuracy"]
                + temperature["accuracy"]
            )
            / 3,
            2,
        )

        return {

            "success": True,

            "cpu": cpu,

            "ram": ram,

            "temperature": temperature,

            "average_gap": average_gap,

            "average_accuracy": average_accuracy,

            "status": (
                "Healthy"
                if average_gap < 10
                else "Warning"
            ),
        }


reality_checker = RealityChecker()