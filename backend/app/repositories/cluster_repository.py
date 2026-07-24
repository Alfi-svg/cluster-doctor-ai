"""
Cluster Repository
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import ClusterStatus
from app.models.cluster import Cluster
from app.repositories.base import BaseRepository


class ClusterRepository(BaseRepository[Cluster]):
    """
    Repository for Cluster model.
    """

    def __init__(self):
        super().__init__(Cluster)

    # =====================================================
    # Get Cluster By Name
    # =====================================================

    async def get_by_name(
        self,
        db: AsyncSession,
        name: str,
    ) -> Cluster | None:

        result = await db.execute(

            select(Cluster).where(
                Cluster.name == name
            )

        )

        return result.scalar_one_or_none()

    # =====================================================
    # Get Clusters By Owner
    # =====================================================

    async def get_by_owner(
        self,
        db: AsyncSession,
        owner_id: int,
    ) -> list[Cluster]:

        result = await db.execute(

            select(Cluster).where(
                Cluster.owner_id == owner_id
            )

        )

        return result.scalars().all()

    # =====================================================
    # Healthy Clusters
    # =====================================================

    async def get_healthy_clusters(
        self,
        db: AsyncSession,
    ) -> list[Cluster]:

        result = await db.execute(

            select(Cluster).where(
                Cluster.status == ClusterStatus.HEALTHY
            )

        )

        return result.scalars().all()

    # =====================================================
    # Critical Clusters
    # =====================================================

    async def get_critical_clusters(
        self,
        db: AsyncSession,
    ) -> list[Cluster]:

        result = await db.execute(

            select(Cluster).where(
                Cluster.status == ClusterStatus.CRITICAL
            )

        )

        return result.scalars().all()

    # =====================================================
    # Update Health Score
    # =====================================================

    async def update_health_score(
        self,
        db: AsyncSession,
        cluster: Cluster,
        score: float,
    ) -> Cluster:

        cluster.health_score = score

        if score >= 90:
            cluster.status = ClusterStatus.HEALTHY

        elif score >= 70:
            cluster.status = ClusterStatus.WARNING

        else:
            cluster.status = ClusterStatus.CRITICAL

        await db.commit()

        await db.refresh(cluster)

        return cluster


cluster_repository = ClusterRepository()