"""
Experiment Repository
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import ExperimentStatus
from app.models.experiment import Experiment
from app.repositories.base import BaseRepository


class ExperimentRepository(BaseRepository[Experiment]):
    """
    Repository for Experiment model.
    """

    def __init__(self):
        super().__init__(Experiment)

    # =====================================================
    # Get By User
    # =====================================================

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Experiment]:

        result = await db.execute(
            select(Experiment).where(
                Experiment.user_id == user_id
            )
        )

        return result.scalars().all()

    # =====================================================
    # Get By Cluster
    # =====================================================

    async def get_by_cluster(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> list[Experiment]:

        result = await db.execute(
            select(Experiment).where(
                Experiment.cluster_id == cluster_id
            )
        )

        return result.scalars().all()

    # =====================================================
    # Running Experiments
    # =====================================================

    async def get_running(
        self,
        db: AsyncSession,
    ) -> list[Experiment]:

        result = await db.execute(
            select(Experiment).where(
                Experiment.status == ExperimentStatus.RUNNING
            )
        )

        return result.scalars().all()

    # =====================================================
    # Completed Experiments
    # =====================================================

    async def get_completed(
        self,
        db: AsyncSession,
    ) -> list[Experiment]:

        result = await db.execute(
            select(Experiment).where(
                Experiment.status == ExperimentStatus.COMPLETED
            )
        )

        return result.scalars().all()

    # =====================================================
    # Failed Experiments
    # =====================================================

    async def get_failed(
        self,
        db: AsyncSession,
    ) -> list[Experiment]:

        result = await db.execute(
            select(Experiment).where(
                Experiment.status == ExperimentStatus.FAILED
            )
        )

        return result.scalars().all()

    # =====================================================
    # Update Progress
    # =====================================================

    async def update_progress(
        self,
        db: AsyncSession,
        experiment: Experiment,
        progress: float,
    ) -> Experiment:

        experiment.progress = progress

        await db.commit()
        await db.refresh(experiment)

        return experiment


experiment_repository = ExperimentRepository()