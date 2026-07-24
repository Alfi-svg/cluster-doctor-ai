"""
Digital Twin Manager

Keeps the live state of every cluster and node in memory.
This is the central state engine for the Digital Twin.

Flow:

MQTT
    ↓
Telemetry
    ↓
TwinManager
    ↓
WebSocket
    ↓
Frontend
"""

from __future__ import annotations

from asyncio import Lock
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


# ==========================================================
# Twin Node
# ==========================================================

@dataclass
class TwinNode:
    node_id: str

    status: str = "ONLINE"

    cpu: float = 0.0
    memory: float = 0.0
    gpu: float = 0.0
    temperature: float = 0.0
    power: float = 0.0

    risk_score: float = 0.0
    prediction: str = "Healthy"

    recommendation: str = ""

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


# ==========================================================
# Twin Cluster
# ==========================================================

@dataclass
class TwinCluster:
    cluster_id: str

    health: float = 100.0

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    nodes: dict[str, TwinNode] = field(default_factory=dict)


# ==========================================================
# Twin Manager
# ==========================================================

class TwinManager:

    def __init__(self) -> None:

        self._clusters: dict[str, TwinCluster] = {}

        self._lock = Lock()

    # ------------------------------------------------------

    async def register_cluster(self, cluster_id: str):

        async with self._lock:

            if cluster_id not in self._clusters:

                self._clusters[cluster_id] = TwinCluster(
                    cluster_id=cluster_id
                )

    # ------------------------------------------------------

    async def register_node(
        self,
        cluster_id: str,
        node_id: str,
    ):

        await self.register_cluster(cluster_id)

        async with self._lock:

            cluster = self._clusters[cluster_id]

            if node_id not in cluster.nodes:

                cluster.nodes[node_id] = TwinNode(
                    node_id=node_id
                )

    # ------------------------------------------------------

    async def update_node(
        self,
        cluster_id: str,
        node_id: str,
        **kwargs: Any,
    ):

        await self.register_node(cluster_id, node_id)

        async with self._lock:

            node = self._clusters[cluster_id].nodes[node_id]

            for key, value in kwargs.items():

                if hasattr(node, key):

                    setattr(node, key, value)

            node.updated_at = datetime.utcnow().isoformat()

            self._update_cluster_health(cluster_id)

    # ------------------------------------------------------

    def _update_cluster_health(
        self,
        cluster_id: str,
    ):

        cluster = self._clusters[cluster_id]

        if not cluster.nodes:

            cluster.health = 100.0
            return

        risks = [
            node.risk_score
            for node in cluster.nodes.values()
        ]

        avg_risk = sum(risks) / len(risks)

        cluster.health = round(100 - avg_risk, 2)

        cluster.updated_at = datetime.utcnow().isoformat()

    # ------------------------------------------------------

    async def get_cluster(
        self,
        cluster_id: str,
    ) -> dict:

        async with self._lock:

            cluster = self._clusters.get(cluster_id)

            if not cluster:

                return {}

            return {
                "cluster_id": cluster.cluster_id,
                "health": cluster.health,
                "updated_at": cluster.updated_at,
                "nodes": [
                    asdict(node)
                    for node in cluster.nodes.values()
                ],
            }

    # ------------------------------------------------------

    async def get_all_clusters(self):

        async with self._lock:

            return [
                await self.get_cluster(cluster.cluster_id)
                for cluster in self._clusters.values()
            ]

    # ------------------------------------------------------

    async def remove_node(
        self,
        cluster_id: str,
        node_id: str,
    ):

        async with self._lock:

            cluster = self._clusters.get(cluster_id)

            if not cluster:

                return

            cluster.nodes.pop(node_id, None)

            self._update_cluster_health(cluster_id)

    # ------------------------------------------------------

    async def clear(self):

        async with self._lock:

            self._clusters.clear()

    # ------------------------------------------------------

    async def get_node(
        self,
        node_id: str,
    ) -> dict:

        async with self._lock:

            for cluster in self._clusters.values():

                if node_id in cluster.nodes:

                    return asdict(
                        cluster.nodes[node_id]
                    )

            return {}

# ==========================================================
# Singleton
# ==========================================================

twin_manager = TwinManager()