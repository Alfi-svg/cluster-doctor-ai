"""
Prediction Service
"""

import logging
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.feature_mapper import FeatureMapper
from app.ai.gateway import AIGateway
from app.ai.recommendation_engine import RecommendationEngine
from app.database.enums import PredictionStatus
from app.models.prediction import Prediction

from app.repositories.cluster_repository import (
    ClusterRepository,
    cluster_repository,
)
from app.repositories.node_repository import (
    NodeRepository,
    node_repository,
)
from app.repositories.telemetry_repository import (
    TelemetryRepository,
    telemetry_repository,
)
from app.repositories.prediction_repository import (
    PredictionRepository,
    prediction_repository,
)

from app.schemas.prediction import (
    PredictionRequest,
    PredictionUpdate,
)

from app.services.explanation_service import explanation_service


logger = logging.getLogger(__name__)


class EntityNotFoundError(Exception):
    pass


class TelemetryNotFoundError(Exception):
    pass


class PredictionService:

    def __init__(
        self,
        cluster_repo: ClusterRepository = cluster_repository,
        node_repo: NodeRepository = node_repository,
        telemetry_repo: TelemetryRepository = telemetry_repository,
        prediction_repo: PredictionRepository = prediction_repository,
    ):
        self.cluster_repo = cluster_repo
        self.node_repo = node_repo
        self.telemetry_repo = telemetry_repo
        self.prediction_repo = prediction_repo

        self.feature_mapper = FeatureMapper()
        self.ai_gateway = AIGateway()
        self.recommendation_engine = RecommendationEngine()

    # =====================================================
    # Convert Telemetry
    # =====================================================

    @staticmethod
    def _telemetry_to_dict(
        telemetry: Any,
    ) -> dict[str, Any]:

        if hasattr(telemetry, "to_dict"):
            return telemetry.to_dict()

        return {
            "cpu_usage": getattr(telemetry, "cpu_usage", 0),
            "cpu_temperature": getattr(telemetry, "cpu_temperature", 0),
            "gpu_usage": getattr(telemetry, "gpu_usage", 0),
            "gpu_temperature": getattr(telemetry, "gpu_temperature", 0),
            "gpu_memory_usage": getattr(telemetry, "gpu_memory_usage", 0),
            "gpu_power": getattr(telemetry, "gpu_power", 0),
            "ram_usage": getattr(telemetry, "ram_usage", 0),
            "network_in": getattr(telemetry, "network_in", 0),
            "network_out": getattr(telemetry, "network_out", 0),
            "latency": getattr(telemetry, "latency", 0),
        }

    # =====================================================
    # Create Prediction
    # =====================================================

    async def create_prediction(
        self,
        db: AsyncSession,
        request: PredictionRequest,
    ) -> Prediction:

        # ------------------------------------------
        # Validate Cluster
        # ------------------------------------------
        cluster = await self.cluster_repo.get(
            db,
            request.cluster_id,
        )

        if cluster is None:
            raise EntityNotFoundError(
                f"Cluster {request.cluster_id} not found."
            )

        # ------------------------------------------
        # Validate Node
        # ------------------------------------------
        node = await self.node_repo.get(
            db,
            request.node_id,
        )

        if node is None:
            raise EntityNotFoundError(
                f"Node {request.node_id} not found."
            )

        # ------------------------------------------
        # Latest Telemetry
        # ------------------------------------------
        telemetry = await self.telemetry_repo.get_latest(
            db,
            request.node_id,
        )

        if telemetry is None:
            raise TelemetryNotFoundError(
                "Telemetry not found."
            )

        telemetry_dict = self._telemetry_to_dict(
            telemetry
        )

        # ------------------------------------------
        # Feature Mapping
        # ------------------------------------------
        failure_features = self.feature_mapper.failure_features(
            telemetry_dict
        )

        security_features = self.feature_mapper.security_features(
            telemetry_dict
        )

        guardian_features = self.feature_mapper.guardian_features(
            telemetry_dict
        )

        # ------------------------------------------
        # AI Models
        # ------------------------------------------
        failure_result = self.ai_gateway.predict_failure(
            failure_features
        )

        security_result = self.ai_gateway.detect_anomaly(
            security_features
        )

        guardian_result = self.ai_gateway.evaluate_experiment(
            guardian_features
        )

        # ------------------------------------------
        # Recommendation Engine
        # ------------------------------------------
        prediction = self.recommendation_engine.generate(
            failure=failure_result,
            security=security_result,
            guardian=guardian_result,
        )

        # ------------------------------------------
        # AI Explanation (LLM), with a deterministic
        # fallback to the rule-based recommendation
        # engine output if the LLM call fails (e.g.
        # no API key configured) so prediction
        # creation never hard-fails.
        # ------------------------------------------
        explanation_text = prediction["explanation"]
        recommendation_text = prediction["recommendation"]

        try:
            llm_result = await explanation_service.explain_prediction(
                telemetry=telemetry_dict,
                prediction=prediction,
            )

            explanation_text = llm_result.summary

            if llm_result.recommendations:
                recommendation_text = "\n".join(
                    item.title
                    for item in llm_result.recommendations
                )

        except Exception:
            logger.warning(
                "LLM explanation unavailable, "
                "falling back to rule-based recommendation.",
                exc_info=True,
            )

        # ------------------------------------------
        # Save Prediction
        # ------------------------------------------
        saved_prediction = await self.prediction_repo.create(
            db,
            cluster_id=request.cluster_id,
            node_id=request.node_id,
            model_name=prediction["model_name"],
            prediction_type=prediction["prediction_type"],
            status=PredictionStatus.COMPLETED,
            confidence=prediction["confidence"],
            risk_score=prediction["risk_score"],
            probability=prediction["probability"],
            predicted_label=prediction["predicted_label"],
            recommendation=recommendation_text,
            explanation=explanation_text,
            predicted_at=datetime.utcnow(),
        )

        return saved_prediction

    # =====================================================
    # Get Prediction
    # =====================================================

    async def get_prediction(
        self,
        db: AsyncSession,
        prediction_id: int,
    ) -> Prediction | None:

        return await self.prediction_repo.get(
            db,
            prediction_id,
        )

    # =====================================================
    # Latest Prediction
    # =====================================================

    async def get_latest_prediction(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> Prediction | None:

        return await self.prediction_repo.get_latest(
            db,
            node_id,
        )

    # =====================================================
    # Node Predictions
    # =====================================================

    async def get_node_predictions(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> list[Prediction]:

        return await self.prediction_repo.get_by_node(
            db,
            node_id,
        )

    # =====================================================
    # Model Predictions
    # =====================================================

    async def get_model_predictions(
        self,
        db: AsyncSession,
        model_name: str,
    ) -> list[Prediction]:

        return await self.prediction_repo.get_by_model(
            db,
            model_name,
        )

    # =====================================================
    # High Risk Predictions
    # =====================================================

    async def get_high_risk_predictions(
        self,
        db: AsyncSession,
        threshold: float = 80.0,
    ) -> list[Prediction]:

        return await self.prediction_repo.get_high_risk(
            db,
            threshold,
        )

    # =====================================================
    # Pending Predictions
    # =====================================================

    async def get_pending_predictions(
        self,
        db: AsyncSession,
    ) -> list[Prediction]:

        return await self.prediction_repo.get_pending(
            db,
        )

    # =====================================================
    # Update Prediction
    # =====================================================

    async def update_prediction(
        self,
        db: AsyncSession,
        prediction_id: int,
        prediction_in: PredictionUpdate,
    ) -> Prediction:

        prediction = await self.prediction_repo.get(
            db,
            prediction_id,
        )

        if prediction is None:
            raise EntityNotFoundError(
                f"Prediction {prediction_id} not found."
            )

        update_data = prediction_in.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        updated_prediction = await self.prediction_repo.update(
            db,
            prediction,
            **update_data,
        )

        return updated_prediction

    # =====================================================
    # Delete Prediction
    # =====================================================

    async def delete_prediction(
        self,
        db: AsyncSession,
        prediction_id: int,
    ) -> None:

        prediction = await self.prediction_repo.get(
            db,
            prediction_id,
        )

        if prediction is None:
            raise EntityNotFoundError(
                f"Prediction {prediction_id} not found."
            )

        await self.prediction_repo.delete(
            db,
            prediction,
        )


prediction_service = PredictionService()