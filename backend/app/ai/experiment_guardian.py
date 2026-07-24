from typing import Any

import pandas as pd

from app.ai.model_loader import ModelLoader


class ExperimentGuardianService:
    """
    AI service for monitoring ML experiment health.
    Predicts whether an experiment is at risk of failure.
    """

    def __init__(self):
        bundle = ModelLoader.get_experiment_guardian()

        self.model = bundle["model"]
        self.features = bundle["features"]

    def evaluate(self, experiment: dict[str, Any]) -> dict:
        """
        Evaluate experiment risk.

        Returns:
        {
            prediction: int,
            risk: bool,
            probability: float,
            risk_score: float
        }
        """

        missing = [
            feature
            for feature in self.features
            if feature not in experiment
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        values = {
            feature: experiment[feature]
            for feature in self.features
        }

        df = pd.DataFrame([values])

        prediction = int(self.model.predict(df)[0])

        probability = None

        if hasattr(self.model, "predict_proba"):
            probability = float(
                self.model.predict_proba(df)[0][1]
            )

        return {
            "prediction": prediction,
            "risk": bool(prediction),
            "probability": probability,
            "risk_score": round(probability * 100, 2)
            if probability is not None
            else None,
            "status": "High Risk" if prediction else "Healthy",
        }

    async def start(self, experiment: Any) -> None:
        pass


experiment_guardian = ExperimentGuardianService()