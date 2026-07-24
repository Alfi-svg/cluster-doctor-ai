"""
Prediction Repository
"""

from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import PredictionStatus
from app.models.prediction import Prediction
from app.repositories.base import BaseRepository


class PredictionRepository(BaseRepository[Prediction]):
    """
    Repository for Prediction model.
    """

    def __init__(self):
        super().__init__(Prediction)

    # =====================================================
    # Latest Prediction
    # =====================================================

    async def get_latest(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> Prediction | None:

        result = await db.execute(
            select(Prediction)
            .where(Prediction.node_id == node_id)
            .order_by(desc(Prediction.predicted_at))
            .limit(1)
        )

        return result.scalar_one_or_none()

    # =====================================================
    # Get By Node
    # =====================================================

    async def get_by_node(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> list[Prediction]:

        result = await db.execute(
            select(Prediction)
            .where(Prediction.node_id == node_id)
        )

        return result.scalars().all()

    # =====================================================
    # Get By Model
    # =====================================================

    async def get_by_model(
        self,
        db: AsyncSession,
        model_name: str,
    ) -> list[Prediction]:

        result = await db.execute(
            select(Prediction)
            .where(Prediction.model_name == model_name)
        )

        return result.scalars().all()

    # =====================================================
    # High Risk Predictions
    # =====================================================

    async def get_high_risk(
        self,
        db: AsyncSession,
        threshold: float = 80.0,
    ) -> list[Prediction]:

        result = await db.execute(
            select(Prediction)
            .where(Prediction.risk_score >= threshold)
        )

        return result.scalars().all()

    # =====================================================
    # Pending Predictions
    # =====================================================

    async def get_pending(
        self,
        db: AsyncSession,
    ) -> list[Prediction]:

        result = await db.execute(
            select(Prediction)
            .where(
                Prediction.status == PredictionStatus.PENDING
            )
        )

        return result.scalars().all()


prediction_repository = PredictionRepository()