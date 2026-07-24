"""
Safe Target Selector

Selects the safest node for workload migration.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CandidateNode:
    node_id: int
    health_score: float
    cpu_usage: float
    ram_usage: float
    status: str = "online"


class SafeTargetSelector:
    """
    Select the safest migration target.

    Score Formula

    health_score * 0.6

    +

    free_memory * 0.4
    """

    @staticmethod
    def calculate_score(
        node: CandidateNode,
    ) -> float:

        free_memory = 100 - node.ram_usage

        score = (
            node.health_score * 0.6
            +
            free_memory * 0.4
        )

        return round(score, 2)

    def select(
        self,
        candidates: list[CandidateNode],
    ) -> CandidateNode | None:

        available = [
            node
            for node in candidates
            if node.status == "online"
        ]

        if not available:
            return None

        available.sort(
            key=self.calculate_score,
            reverse=True,
        )

        return available[0]


safe_target_selector = SafeTargetSelector()