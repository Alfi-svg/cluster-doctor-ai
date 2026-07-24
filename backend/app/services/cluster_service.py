"""
Cluster Service
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cluster import Cluster
from app.models.user import User

from app.repositories.cluster_repository import cluster_repository

from app.schemas.cluster import (
    ClusterCreate,
    ClusterUpdate,
)


class ClusterService:
    """
    Business logic for Cluster.
    """

    # =====================================================
    # Create Cluster
    # =====================================================

    async def create_cluster(
        self,
        db: AsyncSession,
        cluster: ClusterCreate,
        owner: User,
    ) -> Cluster:

        existing = await cluster_repository.get_by_name(
            db,
            cluster.name,
        )

        if existing:
            raise ValueError("Cluster name already exists.")

        return await cluster_repository.create(
            db=db,
            name=cluster.name,
            description=cluster.description,
            location=cluster.location,
            owner_id=owner.id,
        )

    # =====================================================
    # Get Cluster
    # =====================================================

    async def get_cluster(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> Cluster:

        cluster = await cluster_repository.get(
            db,
            cluster_id,
        )

        if not cluster:
            raise ValueError("Cluster not found.")

        return cluster

    # =====================================================
    # Get All Clusters
    # =====================================================

    async def get_clusters(
        self,
        db: AsyncSession,
    ) -> list[Cluster]:

        return await cluster_repository.get_all(db)

    # =====================================================
    # Get User Clusters
    # =====================================================

    async def get_user_clusters(
        self,
        db: AsyncSession,
        owner_id: int,
    ) -> list[Cluster]:

        return await cluster_repository.get_by_owner(
            db,
            owner_id,
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

        cluster = await self.get_cluster(
            db,
            cluster_id,
        )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        return await cluster_repository.update(
            db=db,
            obj=cluster,
            **update_data,
        )

    # =====================================================
    # Delete Cluster
    # =====================================================

    async def delete_cluster(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> None:

        cluster = await self.get_cluster(
            db,
            cluster_id,
        )

        await cluster_repository.delete(
            db,
            cluster,
        )

    # =====================================================
    # Healthy Clusters
    # =====================================================

    async def healthy_clusters(
        self,
        db: AsyncSession,
    ) -> list[Cluster]:

        return await cluster_repository.get_healthy_clusters(
            db,
        )

    # =====================================================
    # Critical Clusters
    # =====================================================

    async def critical_clusters(
        self,
        db: AsyncSession,
    ) -> list[Cluster]:

        return await cluster_repository.get_critical_clusters(
            db,
        )

    # =====================================================
    # Update Health Score
    # =====================================================

    async def update_health(
        self,
        db: AsyncSession,
        cluster_id: int,
        score: float,
    ) -> Cluster:

        cluster = await self.get_cluster(
            db,
            cluster_id,
        )

        return await cluster_repository.update_health_score(
            db,
            cluster,
            score,
        )


cluster_service = ClusterService()