"""
Experiment Service

Business logic for AI experiments.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import ExperimentStatus

from app.models.cluster import Cluster
from app.models.experiment import Experiment
from app.models.user import User

from app.repositories.experiment_repository import (
    experiment_repository,
)

from app.schemas.experiment import (
    ExperimentCreate,
    ExperimentUpdate,
)

from app.ai.experiment_guardian import experiment_guardian


class ExperimentService:
    """
    Experiment business service.
    """

    # =====================================================
    # Create Experiment
    # =====================================================

    async def create_experiment(
        self,
        db: AsyncSession,
        user: User,
        cluster: Cluster,
        data: ExperimentCreate,
    ) -> Experiment:

        experiment = await experiment_repository.create(
            db,
            user_id=user.id,
            cluster_id=cluster.id,
            name=data.name,
            description=data.description,
            status=ExperimentStatus.PENDING,
            progress=0.0,
        )

        return experiment

    # =====================================================
    # Get Experiment
    # =====================================================

    async def get_experiment(
        self,
        db: AsyncSession,
        experiment_id: int,
    ) -> Experiment:

        experiment = await experiment_repository.get(
            db,
            experiment_id,
        )

        if experiment is None:
            raise ValueError("Experiment not found.")

        return experiment

    # =====================================================
    # Get User Experiments
    # =====================================================

    async def get_user_experiments(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Experiment]:

        return await experiment_repository.get_by_user(
            db,
            user_id,
        )

    # =====================================================
    # Start Experiment
    # =====================================================

    async def start_experiment(
        self,
        db: AsyncSession,
        experiment: Experiment,
    ) -> Experiment:

        await experiment_guardian.start(experiment)

        return await experiment_repository.update(
            db,
            experiment,
            status=ExperimentStatus.RUNNING,
        )

    # =====================================================
    # Update Progress
    # =====================================================

    async def update_progress(
        self,
        db: AsyncSession,
        experiment: Experiment,
        progress: float,
    ) -> Experiment:

        progress = max(0.0, min(progress, 100.0))

        return await experiment_repository.update(
            db,
            experiment,
            progress=progress,
        )

    # =====================================================
    # Complete Experiment
    # =====================================================

    async def complete_experiment(
        self,
        db: AsyncSession,
        experiment: Experiment,
    ) -> Experiment:

        return await experiment_repository.update(
            db,
            experiment,
            status=ExperimentStatus.COMPLETED,
            progress=100.0,
        )

    # =====================================================
    # Fail Experiment
    # =====================================================

    async def fail_experiment(
        self,
        db: AsyncSession,
        experiment: Experiment,
    ) -> Experiment:

        return await experiment_repository.update(
            db,
            experiment,
            status=ExperimentStatus.FAILED,
        )

    # =====================================================
    # Cancel Experiment
    # =====================================================

    async def cancel_experiment(
        self,
        db: AsyncSession,
        experiment: Experiment,
    ) -> Experiment:

        return await experiment_repository.update(
            db,
            experiment,
            status=ExperimentStatus.CANCELLED,
        )

    # =====================================================
    # Update Experiment
    # =====================================================

    async def update_experiment(
        self,
        db: AsyncSession,
        experiment: Experiment,
        data: ExperimentUpdate,
    ) -> Experiment:

        update_data = data.model_dump(
            exclude_unset=True,
        )

        return await experiment_repository.update(
            db,
            experiment,
            **update_data,
        )


experiment_service = ExperimentService()