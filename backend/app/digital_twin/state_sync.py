"""
Digital Twin State Synchronization

Synchronizes runtime telemetry and AI prediction
with the Digital Twin and Snapshot Manager.

Flow

Telemetry
    ↓
State Sync
    ↓
Twin Manager
    ↓
Snapshot Manager
    ↓
WebSocket
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.digital_twin.twin_manager import twin_manager
from app.digital_twin.snapshot import (
    TwinSnapshot,
    snapshot_manager,
)


class StateSync:
    """
    Synchronizes runtime state with
    the Digital Twin.
    """

    # =====================================================
    # Telemetry
    # =====================================================

    async def sync_telemetry(
        self,
        cluster_id: str,
        node_id: str,
        telemetry: dict[str, Any],
    ) -> None:

        cpu = float(telemetry.get("cpu", 0))
        memory = float(telemetry.get("memory", 0))
        gpu = float(telemetry.get("gpu", 0))
        temperature = float(telemetry.get("temperature", 0))
        power = float(telemetry.get("power", 0))

        # -------------------------------
        # Update Twin
        # -------------------------------

        await twin_manager.update_node(
            cluster_id=cluster_id,
            node_id=node_id,
            cpu=cpu,
            memory=memory,
            gpu=gpu,
            temperature=temperature,
            power=power,
            updated_at=datetime.utcnow().isoformat(),
        )

        # -------------------------------
        # Update Snapshot
        # -------------------------------

        previous = snapshot_manager.get((node_id))

        snapshot = TwinSnapshot(
            cluster_id=cluster_id,
            node_id=node_id,
            cpu_usage=cpu,
            cpu_temperature=temperature,
            gpu_usage=gpu,
            gpu_temperature=temperature,
            ram_usage=memory,
            disk_usage=float(
                telemetry.get(
                    "disk_usage",
                    getattr(previous, "disk_usage", 0),
                )
            ),
            network_in=float(
                telemetry.get(
                    "network_in",
                    getattr(previous, "network_in", 0),
                )
            ),
            network_out=float(
                telemetry.get(
                    "network_out",
                    getattr(previous, "network_out", 0),
                )
            ),
            health_score=getattr(previous, "health_score", 100),
            risk_score=getattr(previous, "risk_score", 0),
            timestamp=datetime.utcnow(),
        )

        snapshot_manager.update(snapshot)

    # =====================================================
    # Prediction
    # =====================================================

    async def sync_prediction(
        self,
        cluster_id: str,
        node_id: str,
        prediction: dict[str, Any],
    ) -> None:

        risk_score = float(
            prediction.get("risk_score", 0)
        )

        await twin_manager.update_node(
            cluster_id=cluster_id,
            node_id=node_id,
            risk_score=risk_score,
            prediction=prediction.get(
                "prediction",
                "Healthy",
            ),
            recommendation=prediction.get(
                "recommendation",
                "",
            ),
            updated_at=datetime.utcnow().isoformat(),
        )

        previous = snapshot_manager.get(node_id)

        if previous is None:
            return

        snapshot = TwinSnapshot(
            cluster_id=previous.cluster_id,
            node_id=previous.node_id,
            cpu_usage=previous.cpu_usage,
            cpu_temperature=previous.cpu_temperature,
            gpu_usage=previous.gpu_usage,
            gpu_temperature=previous.gpu_temperature,
            ram_usage=previous.ram_usage,
            disk_usage=previous.disk_usage,
            network_in=previous.network_in,
            network_out=previous.network_out,
            health_score=max(
                0,
                100 - risk_score,
            ),
            risk_score=risk_score,
            timestamp=datetime.utcnow(),
        )

        snapshot_manager.update(snapshot)

    # =====================================================
    # Health
    # =====================================================

    async def sync_health(
        self,
        cluster_id: str,
        node_id: str,
        health: float,
    ) -> None:

        await twin_manager.update_node(
            cluster_id=cluster_id,
            node_id=node_id,
            risk_score=max(
                0,
                100 - health,
            ),
        )

        previous = snapshot_manager.get(node_id)

        if previous is None:
            return

        previous.health_score = health
        previous.risk_score = max(
            0,
            100 - health,
        )
        previous.timestamp = datetime.utcnow()

        snapshot_manager.update(previous)

    # =====================================================
    # Status
    # =====================================================

    async def mark_online(
        self,
        cluster_id: str,
        node_id: str,
    ) -> None:

        await twin_manager.update_node(
            cluster_id=cluster_id,
            node_id=node_id,
            status="ONLINE",
        )

    async def mark_offline(
        self,
        cluster_id: str,
        node_id: str,
    ) -> None:

        await twin_manager.update_node(
            cluster_id=cluster_id,
            node_id=node_id,
            status="OFFLINE",
        )

    # =====================================================
    # Getters
    # =====================================================

    async def get_cluster(
        self,
        cluster_id: str,
    ):
        return await twin_manager.get_cluster(
            cluster_id
        )

    async def get_all_clusters(self):
        return await twin_manager.get_all_clusters()

    # =====================================================
    # Snapshot API
    # =====================================================

    def get_snapshot(
        self,
        node_id: str,
    ) -> TwinSnapshot | None:

        return snapshot_manager.get(node_id)

    def get_all_snapshots(self):

        return snapshot_manager.all()


state_sync = StateSync()