"""
Prediction Pipeline

Runs the complete prediction workflow by delegating
to PredictionService.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.prediction_service import prediction_service
from app.schemas.prediction import PredictionRequest
from app.models.prediction import Prediction


class PredictionPipeline:
    """
    Executes AI prediction pipeline.
    """

    async def run(
        self,
        db: AsyncSession,
        cluster_id: int,
        node_id: int,
    ) -> Prediction:

        request = PredictionRequest(
            cluster_id=cluster_id,
            node_id=node_id,
        )

        prediction = await prediction_service.create_prediction(
            db=db,
            request=request,
        )

        return prediction