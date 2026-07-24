"""
Digital Twin Animation Engine

Determines how each node should appear
inside the 3D Digital Twin.

This module does NOT render graphics.
It only returns visualization states.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.digital_twin.twin_manager import TwinNode


# ==========================================================
# Animation State
# ==========================================================

@dataclass
class AnimationState:

    color: str

    animation: str

    severity: str

    icon: str


# ==========================================================
# Animation Engine
# ==========================================================

class AnimationEngine:

    """
    Maps node health to frontend animation state.
    """

    def get_state(
        self,
        node: TwinNode,
    ) -> AnimationState:

        # Offline
        if node.status.upper() == "OFFLINE":

            return AnimationState(
                color="#808080",
                animation="blink",
                severity="offline",
                icon="wifi_off",
            )

        risk = node.risk_score

        # Healthy
        if risk < 20:

            return AnimationState(
                color="#22c55e",
                animation="idle",
                severity="healthy",
                icon="check_circle",
            )

        # Warning
        if risk < 50:

            return AnimationState(
                color="#facc15",
                animation="pulse",
                severity="warning",
                icon="warning",
            )

        # Critical
        if risk < 80:

            return AnimationState(
                color="#fb923c",
                animation="fast_pulse",
                severity="critical",
                icon="priority_high",
            )

        # Failure
        return AnimationState(
            color="#ef4444",
            animation="flash",
            severity="failure",
            icon="dangerous",
        )


animation_engine = AnimationEngine()