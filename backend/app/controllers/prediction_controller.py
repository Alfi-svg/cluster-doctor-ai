"""
Prediction Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prediction import Prediction
from app.schemas.prediction import (
    PredictionCreate,
    PredictionUpdate,
)
from app.services.prediction_service import prediction_service


class PredictionController:
    """
    Prediction Controller
    """

    # =====================================================
    # Create Prediction
    # =====================================================

    async def create_prediction(
        self,
        db: AsyncSession,
        data: PredictionCreate,
    ) -> Prediction:

        return await prediction_service.create_prediction(
            db=db,
            request=data,
        )

    # =====================================================
    # Get Prediction
    # =====================================================

    async def get_prediction(
        self,
        db: AsyncSession,
        prediction_id: int,
    ) -> Prediction | None:

        return await prediction_service.get_prediction(
            db=db,
            prediction_id=prediction_id,
        )

    # =====================================================
    # Latest Prediction
    # =====================================================

    async def get_latest_prediction(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> Prediction | None:

        return await prediction_service.get_latest_prediction(
            db=db,
            node_id=node_id,
        )

    # =====================================================
    # Node Predictions
    # =====================================================

    async def get_node_predictions(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> list[Prediction]:

        return await prediction_service.get_node_predictions(
            db=db,
            node_id=node_id,
        )

    # =====================================================
    # Model Predictions
    # =====================================================

    async def get_model_predictions(
        self,
        db: AsyncSession,
        model_name: str,
    ) -> list[Prediction]:

        return await prediction_service.get_model_predictions(
            db=db,
            model_name=model_name,
        )

    # =====================================================
    # High Risk Predictions
    # =====================================================

    async def get_high_risk_predictions(
        self,
        db: AsyncSession,
        threshold: float = 80.0,
    ) -> list[Prediction]:

        return await prediction_service.get_high_risk_predictions(
            db=db,
            threshold=threshold,
        )

    # =====================================================
    # Pending Predictions
    # =====================================================

    async def get_pending_predictions(
        self,
        db: AsyncSession,
    ) -> list[Prediction]:

        return await prediction_service.get_pending_predictions(
            db=db,
        )

    # =====================================================
    # Update Prediction
    # =====================================================

    async def update_prediction(
        self,
        db: AsyncSession,
        prediction_id: int,
        data: PredictionUpdate,
    ) -> Prediction | None:

        return await prediction_service.update_prediction(
            db=db,
            prediction_id=prediction_id,
            prediction_in=data,
        )

    # =====================================================
    # Delete Prediction
    # =====================================================

    async def delete_prediction(
        self,
        db: AsyncSession,
        prediction_id: int,
    ) -> None:

        await prediction_service.delete_prediction(
            db=db,
            prediction_id=prediction_id,
        )


prediction_controller = PredictionController()