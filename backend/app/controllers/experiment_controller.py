"""
Experiment Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cluster import Cluster
from app.models.experiment import Experiment
from app.models.user import User

from app.schemas.experiment import (
    ExperimentCreate,
    ExperimentUpdate,
)

from app.services.experiment_service import (
    experiment_service,
)


class ExperimentController:
    """
    Experiment Controller.

    Coordinates experiment-related requests.
    """

    # =====================================================
    # Create Experiment
    # =====================================================

    async def create_experiment(
        self,
        db: AsyncSession,
        current_user: User,
        cluster: Cluster,
        data: ExperimentCreate,
    ) -> Experiment:

        return await experiment_service.create_experiment(
            db=db,
            user=current_user,
            cluster=cluster,
            data=data,
        )

    # =====================================================
    # Get Experiment
    # =====================================================

    async def get_experiment(
        self,
        db: AsyncSession,
        experiment_id: int,
    ) -> Experiment:

        return await experiment_service.get_experiment(
            db=db,
            experiment_id=experiment_id,
        )

    # =====================================================
    # Get User Experiments
    # =====================================================

    async def get_user_experiments(
        self,
        db: AsyncSession,
        current_user: User,
    ) -> list[Experiment]:

        return await experiment_service.get_user_experiments(
            db=db,
            user_id=current_user.id,
        )

    # =====================================================
    # Start Experiment
    # =====================================================

    async def start_experiment(
        self,
        db: AsyncSession,
        experiment: Experiment,
    ) -> Experiment:

        return await experiment_service.start_experiment(
            db=db,
            experiment=experiment,
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

        return await experiment_service.update_progress(
            db=db,
            experiment=experiment,
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

        return await experiment_service.complete_experiment(
            db=db,
            experiment=experiment,
        )

    # =====================================================
    # Fail Experiment
    # =====================================================

    async def fail_experiment(
        self,
        db: AsyncSession,
        experiment: Experiment,
    ) -> Experiment:

        return await experiment_service.fail_experiment(
            db=db,
            experiment=experiment,
        )

    # =====================================================
    # Cancel Experiment
    # =====================================================

    async def cancel_experiment(
        self,
        db: AsyncSession,
        experiment: Experiment,
    ) -> Experiment:

        return await experiment_service.cancel_experiment(
            db=db,
            experiment=experiment,
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

        return await experiment_service.update_experiment(
            db=db,
            experiment=experiment,
            data=data,
        )


experiment_controller = ExperimentController()