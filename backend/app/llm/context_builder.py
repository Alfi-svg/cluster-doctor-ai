"""
LLM Context Builder

Responsible for building structured context
for all AI services.
"""

from __future__ import annotations

from typing import Any


class ContextBuilder:
    """
    Builds structured context for LLM.
    """

    @staticmethod
    def prediction_context(
        *,
        cluster: dict | None = None,
        node: dict | None = None,
        telemetry: dict | None = None,
        prediction: dict | None = None,
    ) -> str:
        """
        Context for prediction explanation.
        """

        sections = []

        if cluster:
            sections.append(
                f"Cluster Information\n{cluster}"
            )

        if node:
            sections.append(
                f"Node Information\n{node}"
            )

        if telemetry:
            sections.append(
                f"Telemetry\n{telemetry}"
            )

        if prediction:
            sections.append(
                f"Prediction\n{prediction}"
            )

        return "\n\n".join(sections)

    @staticmethod
    def dashboard_context(
        *,
        cluster: dict,
        nodes: list[dict],
        predictions: list[dict],
    ) -> str:
        """
        Dashboard context.
        """

        return f"""
Cluster

{cluster}

Nodes

{nodes}

Predictions

{predictions}
"""

    @staticmethod
    def chat_context(
        *,
        cluster: dict | None = None,
        node: dict | None = None,
        telemetry: dict | None = None,
        prediction: dict | None = None,
        history: list[dict] | None = None,
    ) -> str:
        """
        Chat context.
        """

        context = []

        if cluster:
            context.append(f"Cluster\n{cluster}")

        if node:
            context.append(f"Node\n{node}")

        if telemetry:
            context.append(f"Telemetry\n{telemetry}")

        if prediction:
            context.append(f"Prediction\n{prediction}")

        if history:
            context.append(f"Chat History\n{history}")

        return "\n\n".join(context)

    @staticmethod
    def alert_context(
        *,
        alert: dict,
        node: dict,
    ) -> str:
        """
        Alert explanation context.
        """

        return f"""
Alert

{alert}

Node

{node}
"""

    @staticmethod
    def recovery_context(
        *,
        node: dict,
        prediction: dict,
        telemetry: dict,
    ) -> str:
        """
        Recovery plan context.
        """

        return f"""
Node

{node}

Prediction

{prediction}

Telemetry

{telemetry}
"""

    @staticmethod
    def report_context(
        *,
        cluster: dict,
        nodes: list[dict],
        telemetry: list[dict],
        predictions: list[dict],
    ) -> str:
        """
        Report generation context.
        """

        return f"""
Cluster

{cluster}

Nodes

{nodes}

Telemetry

{telemetry}

Predictions

{predictions}
"""


context_builder = ContextBuilder()