"""
Node Service
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import NodeStatus
from app.models.node import Node

from app.repositories.cluster_repository import cluster_repository
from app.repositories.node_repository import node_repository

from app.schemas.node import (
    NodeCreate,
    NodeUpdate,
)


class NodeService:
    """
    Business Logic for Node
    """

    # =====================================================
    # Create Node
    # =====================================================

    async def create_node(
        self,
        db: AsyncSession,
        data: NodeCreate,
    ) -> Node:

        existing = await node_repository.get_by_hostname(
            db,
            data.hostname,
        )

        if existing:
            raise ValueError("Hostname already exists.")

        cluster = await cluster_repository.get(
            db,
            data.cluster_id,
        )

        if not cluster:
            raise ValueError("Cluster not found.")

        return await node_repository.create(
            db=db,
            hostname=data.hostname,
            ip_address=data.ip_address,
            operating_system=data.operating_system,
            cpu_model=data.cpu_model,
            cpu_cores=data.cpu_cores,
            gpu_model=data.gpu_model,
            gpu_count=data.gpu_count,
            ram_gb=data.ram_gb,
            storage_gb=data.storage_gb,
            cluster_id=data.cluster_id,
        )

    # =====================================================
    # Get Node
    # =====================================================

    async def get_node(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> Node:

        node = await node_repository.get(
            db,
            node_id,
        )

        if not node:
            raise ValueError("Node not found.")

        return node

    # =====================================================
    # Get All Nodes
    # =====================================================

    async def get_nodes(
        self,
        db: AsyncSession,
    ) -> list[Node]:

        return await node_repository.get_all(db)

    # =====================================================
    # Get Cluster Nodes
    # =====================================================

    async def get_cluster_nodes(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> list[Node]:

        return await node_repository.get_by_cluster(
            db,
            cluster_id,
        )

    # =====================================================
    # Update Node
    # =====================================================

    async def update_node(
        self,
        db: AsyncSession,
        node_id: int,
        data: NodeUpdate,
    ) -> Node:

        node = await self.get_node(
            db,
            node_id,
        )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        return await node_repository.update(
            db=db,
            obj=node,
            **update_data,
        )

    # =====================================================
    # Delete Node
    # =====================================================

    async def delete_node(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> None:

        node = await self.get_node(
            db,
            node_id,
        )

        await node_repository.delete(
            db,
            node,
        )

    # =====================================================
    # Online Nodes
    # =====================================================

    async def online_nodes(
        self,
        db: AsyncSession,
    ) -> list[Node]:

        return await node_repository.get_online_nodes(db)

    # =====================================================
    # Offline Nodes
    # =====================================================

    async def offline_nodes(
        self,
        db: AsyncSession,
    ) -> list[Node]:

        return await node_repository.get_offline_nodes(db)

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        db: AsyncSession,
        node_id: int,
        status: NodeStatus,
    ) -> Node:

        node = await self.get_node(
            db,
            node_id,
        )

        return await node_repository.update_status(
            db,
            node,
            status,
        )

    # =====================================================
    # Update Metrics
    # =====================================================

    async def update_metrics(
        self,
        db: AsyncSession,
        node_id: int,
        cpu_usage: float,
        gpu_usage: float,
        memory_usage: float,
        temperature: float,
        power_consumption: float,
    ) -> Node:

        node = await self.get_node(
            db,
            node_id,
        )

        return await node_repository.update_metrics(
            db=db,
            node=node,
            cpu_usage=cpu_usage,
            gpu_usage=gpu_usage,
            memory_usage=memory_usage,
            temperature=temperature,
            power_consumption=power_consumption,
        )


node_service = NodeService()