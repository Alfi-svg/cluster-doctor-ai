from typing import Any

import pandas as pd

from app.ai.model_loader import ModelLoader


class FailurePredictionService:
    """
    AI service for GPU/Node failure prediction.
    """

    def __init__(self):
        self.bundle = ModelLoader.get_failure_predictor()

        self.model = self.bundle["model"]
        self.features = self.bundle["features"]

    def predict(self, telemetry: dict[str, Any]) -> dict:

        # Check missing features
        missing = [
            feature
            for feature in self.features
            if feature not in telemetry
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        # Preserve feature order
        values = {
            feature: telemetry[feature]
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
            "failure": bool(prediction),
            "probability": probability,
            "risk_score": round(
                probability * 100, 2
            ) if probability is not None else None,
        }