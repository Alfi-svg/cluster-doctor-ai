"""
Checkpoint Manager
"""

from __future__ import annotations


class CheckpointManager:

    def restore(
        self,
        workload_id: str,
    ) -> dict:

        return {

            "workload_id": workload_id,

            "checkpoint_restored": True,

            "lost_steps": 0,
        }


checkpoint_manager = CheckpointManager()