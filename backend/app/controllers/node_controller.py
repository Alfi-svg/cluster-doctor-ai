"""
Node Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import NodeStatus
from app.models.node import Node

from app.schemas.node import (
    NodeCreate,
    NodeUpdate,
)

from app.services.node_service import node_service


class NodeController:
    """
    Node Controller
    """

    # =====================================================
    # Create Node
    # =====================================================

    async def create_node(
        self,
        db: AsyncSession,
        data: NodeCreate,
    ) -> Node:

        return await node_service.create_node(
            db=db,
            data=data,
        )

    # =====================================================
    # Get Node
    # =====================================================

    async def get_node(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> Node:

        return await node_service.get_node(
            db=db,
            node_id=node_id,
        )

    # =====================================================
    # Get All Nodes
    # =====================================================

    async def get_nodes(
        self,
        db: AsyncSession,
    ) -> list[Node]:

        return await node_service.get_nodes(db)

    # =====================================================
    # Get Cluster Nodes
    # =====================================================

    async def get_cluster_nodes(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> list[Node]:

        return await node_service.get_cluster_nodes(
            db=db,
            cluster_id=cluster_id,
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

        return await node_service.update_node(
            db=db,
            node_id=node_id,
            data=data,
        )

    # =====================================================
    # Delete Node
    # =====================================================

    async def delete_node(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> None:

        await node_service.delete_node(
            db=db,
            node_id=node_id,
        )

    # =====================================================
    # Online Nodes
    # =====================================================

    async def online_nodes(
        self,
        db: AsyncSession,
    ) -> list[Node]:

        return await node_service.online_nodes(db)

    # =====================================================
    # Offline Nodes
    # =====================================================

    async def offline_nodes(
        self,
        db: AsyncSession,
    ) -> list[Node]:

        return await node_service.offline_nodes(db)

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        db: AsyncSession,
        node_id: int,
        status: NodeStatus,
    ) -> Node:

        return await node_service.update_status(
            db=db,
            node_id=node_id,
            status=status,
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

        return await node_service.update_metrics(
            db=db,
            node_id=node_id,
            cpu_usage=cpu_usage,
            gpu_usage=gpu_usage,
            memory_usage=memory_usage,
            temperature=temperature,
            power_consumption=power_consumption,
        )


node_controller = NodeController()