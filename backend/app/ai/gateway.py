from typing import Any

from app.ai.experiment_guardian import ExperimentGuardianService
from app.ai.failure_prediction import FailurePredictionService
from app.ai.security_detection import SecurityDetectionService


class AIGateway:
    """
    Central AI Gateway.

    Single entry point for all AI services.
    """

    def __init__(self):
        self.failure_service = FailurePredictionService()
        self.security_service = SecurityDetectionService()
        self.guardian_service = ExperimentGuardianService()

    # ---------------------------------------------------
    # Failure Prediction
    # ---------------------------------------------------

    def predict_failure(
        self,
        telemetry: dict[str, Any],
    ) -> dict:

        return self.failure_service.predict(telemetry)

    # ---------------------------------------------------
    # Security / Anomaly Detection
    # ---------------------------------------------------

    def detect_anomaly(
        self,
        telemetry: dict[str, Any],
    ) -> dict:

        return self.security_service.detect(telemetry)

    # ---------------------------------------------------
    # Experiment Guardian
    # ---------------------------------------------------

    def evaluate_experiment(
        self,
        experiment: dict[str, Any],
    ) -> dict:

        return self.guardian_service.evaluate(experiment)