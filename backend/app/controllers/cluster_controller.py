"""
Cluster Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cluster import Cluster
from app.models.user import User

from app.schemas.cluster import (
    ClusterCreate,
    ClusterUpdate,
)

from app.services.cluster_service import cluster_service


class ClusterController:
    """
    Cluster Controller
    """

    # =====================================================
    # Create Cluster
    # =====================================================

    async def create_cluster(
        self,
        db: AsyncSession,
        current_user: User,
        data: ClusterCreate,
    ) -> Cluster:

        return await cluster_service.create_cluster(
            db=db,
            cluster=data,
            owner=current_user,
        )

    # =====================================================
    # Get Cluster
    # =====================================================

    async def get_cluster(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> Cluster:

        return await cluster_service.get_cluster(
            db=db,
            cluster_id=cluster_id,
        )

    # =====================================================
    # Get All Clusters
    # =====================================================

    async def get_clusters(
        self,
        db: AsyncSession,
    ) -> list[Cluster]:

        return await cluster_service.get_clusters(db)

    # =====================================================
    # Get User Clusters
    # =====================================================

    async def get_user_clusters(
        self,
        db: AsyncSession,
        current_user: User,
    ) -> list[Cluster]:

        return await cluster_service.get_user_clusters(
            db=db,
            owner_id=current_user.id,
        )

    # =====================================================
    # Update Cluster
    # =====================================================

    async def update_cluster(
        self,
        db: AsyncSession,
        cluster_id: int,
        data: ClusterUpdate,
    ) -> Cluster:

        return await cluster_service.update_cluster(
            db=db,
            cluster_id=cluster_id,
            data=data,
        )

    # =====================================================
    # Delete Cluster
    # =====================================================

    async def delete_cluster(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> None:

        await cluster_service.delete_cluster(
            db=db,
            cluster_id=cluster_id,
        )

    # =====================================================
    # Healthy Clusters
    # =====================================================

    async def healthy_clusters(
        self,
        db: AsyncSession,
    ) -> list[Cluster]:

        return await cluster_service.healthy_clusters(db)

    # =====================================================
    # Critical Clusters
    # =====================================================

    async def critical_clusters(
        self,
        db: AsyncSession,
    ) -> list[Cluster]:

        return await cluster_service.critical_clusters(db)

    # =====================================================
    # Update Health
    # =====================================================

    async def update_health(
        self,
        db: AsyncSession,
        cluster_id: int,
        score: float,
    ) -> Cluster:

        return await cluster_service.update_health(
            db=db,
            cluster_id=cluster_id,
            score=score,
        )


cluster_controller = ClusterController()