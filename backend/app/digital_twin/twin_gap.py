"""
Twin Gap Calculator

Calculates prediction accuracy between
Digital Twin and real telemetry.
"""

from __future__ import annotations


class TwinGap:

    @staticmethod
    def percentage(
        predicted: float,
        actual: float,
    ) -> float:

        if predicted == 0:
            return 0.0

        gap = abs(predicted - actual)

        return round(
            (gap / predicted) * 100,
            2,
        )

    @staticmethod
    def accuracy(
        predicted: float,
        actual: float,
    ) -> float:

        gap = TwinGap.percentage(
            predicted,
            actual,
        )

        return round(
            max(0, 100 - gap),
            2,
        )


twin_gap = TwinGap()