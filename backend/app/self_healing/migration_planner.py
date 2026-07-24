"""
Migration Planner
"""

from __future__ import annotations

from app.self_healing.safe_target_selector import (
    CandidateNode,
    safe_target_selector,
)


class MigrationPlanner:

    def plan(
        self,
        source_node: int,
        candidates: list[CandidateNode],
    ) -> dict:

        target = safe_target_selector.select(
            candidates
        )

        if target is None:

            return {
                "success": False,
                "source_node": source_node,
                "target_node": None,
                "reason": "No healthy target available.",
            }

        return {
            "success": True,
            "source_node": source_node,
            "target_node": target.node_id,
            "health_score": target.health_score,
            "score": safe_target_selector.calculate_score(
                target
            ),
        }


migration_planner = MigrationPlanner()