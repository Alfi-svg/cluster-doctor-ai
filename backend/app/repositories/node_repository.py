"""
Node Repository
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import NodeStatus
from app.models.node import Node
from app.repositories.base import BaseRepository


class NodeRepository(BaseRepository[Node]):

    def __init__(self):
        super().__init__(Node)

    # =====================================================
    # Get by Hostname
    # =====================================================

    async def get_by_hostname(
        self,
        db: AsyncSession,
        hostname: str,
    ) -> Node | None:

        result = await db.execute(
            select(Node).where(
                Node.hostname == hostname
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # Get by Cluster
    # =====================================================

    async def get_by_cluster(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> list[Node]:

        result = await db.execute(
            select(Node).where(
                Node.cluster_id == cluster_id
            )
        )

        return result.scalars().all()

    # =====================================================
    # Online Nodes
    # =====================================================

    async def get_online_nodes(
        self,
        db: AsyncSession,
    ) -> list[Node]:

        result = await db.execute(
            select(Node).where(
                Node.status == NodeStatus.ONLINE
            )
        )

        return result.scalars().all()

    # =====================================================
    # Offline Nodes
    # =====================================================

    async def get_offline_nodes(
        self,
        db: AsyncSession,
    ) -> list[Node]:

        result = await db.execute(
            select(Node).where(
                Node.status == NodeStatus.OFFLINE
            )
        )

        return result.scalars().all()

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        db: AsyncSession,
        node: Node,
        status: NodeStatus,
    ) -> Node:

        node.status = status

        await db.commit()
        await db.refresh(node)

        return node

    # =====================================================
    # Update Metrics
    # =====================================================

    async def update_metrics(
        self,
        db: AsyncSession,
        node: Node,
        cpu_usage: float,
        gpu_usage: float,
        memory_usage: float,
        temperature: float,
        power_consumption: float,
    ) -> Node:

        node.cpu_usage = cpu_usage
        node.gpu_usage = gpu_usage
        node.memory_usage = memory_usage
        node.temperature = temperature
        node.power_consumption = power_consumption

        await db.commit()
        await db.refresh(node)

        return node


node_repository = NodeRepository()