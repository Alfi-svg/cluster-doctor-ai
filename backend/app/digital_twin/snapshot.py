"""
Digital Twin Snapshot

Stores the latest Digital Twin state for each node.

This snapshot represents the virtual state of a node
and is later compared against real telemetry by the
Reality Checker.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict


# ==========================================================
# Snapshot Model
# ==========================================================


@dataclass
class TwinSnapshot:

    cluster_id: str
    node_id: str

    cpu_usage: float

    cpu_temperature: float

    gpu_usage: float

    gpu_temperature: float

    ram_usage: float

    disk_usage: float

    network_in: float

    network_out: float

    health_score: float

    risk_score: float

    timestamp: datetime


# ==========================================================
# Snapshot Manager
# ==========================================================


class SnapshotManager:
    """
    In-memory Digital Twin Snapshot Store.

    Key:
        node_id

    Value:
        TwinSnapshot
    """

    def __init__(self):

       self._snapshots: Dict[str, TwinSnapshot] = {}
    # ------------------------------------------------------

    def update(
        self,
        snapshot: TwinSnapshot,
    ) -> None:

        self._snapshots[snapshot.node_id] = snapshot

    # ------------------------------------------------------

    def get(
        self,
        node_id: str,
    ) -> TwinSnapshot | None:

        return self._snapshots.get(node_id)

    # ------------------------------------------------------

    def exists(
        self,
        node_id: str,
    ) -> bool:

        return node_id in self._snapshots

    # ------------------------------------------------------

    def remove(
        self,
        node_id: str,
    ) -> None:

        self._snapshots.pop(node_id, None)

    # ------------------------------------------------------

    def clear(self) -> None:

        self._snapshots.clear()

    # ------------------------------------------------------

    def all(self) -> list[TwinSnapshot]:

        return list(self._snapshots.values())

    # ------------------------------------------------------

    def count(self) -> int:

        return len(self._snapshots)

    # ------------------------------------------------------

    def to_dict(
        self,
        node_id: str,
    ) -> dict | None:

        snapshot = self.get(node_id)

        if snapshot is None:
            return None

        return asdict(snapshot)


snapshot_manager = SnapshotManager()