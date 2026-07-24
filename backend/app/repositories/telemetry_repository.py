"""
Telemetry Repository
"""

from datetime import datetime

from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telemetry import Telemetry
from app.repositories.base import BaseRepository


class TelemetryRepository(BaseRepository[Telemetry]):
    """
    Repository for Telemetry model.
    """

    def __init__(self):
        super().__init__(Telemetry)

    # =====================================================
    # Latest Telemetry
    # =====================================================

    async def get_latest(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> Telemetry | None:

        result = await db.execute(

            select(Telemetry)
            .where(Telemetry.node_id == node_id)
            .order_by(desc(Telemetry.recorded_at))
            .limit(1)

        )

        return result.scalar_one_or_none()

    # =====================================================
    # History
    # =====================================================

    async def get_history(
        self,
        db: AsyncSession,
        node_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Telemetry]:

        result = await db.execute(

            select(Telemetry).where(
                Telemetry.node_id == node_id,
                Telemetry.recorded_at >= start_time,
                Telemetry.recorded_at <= end_time,
            )

        )

        return result.scalars().all()

    # =====================================================
    # Cluster Telemetry
    # =====================================================

    async def get_cluster_telemetry(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> list[Telemetry]:

        result = await db.execute(

            select(Telemetry).where(
                Telemetry.cluster_id == cluster_id
            )

        )

        return result.scalars().all()


telemetry_repository = TelemetryRepository()