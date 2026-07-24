from typing import Any

import pandas as pd

from app.ai.model_loader import ModelLoader


class SecurityDetectionService:
    """
    AI service for anomaly detection using Isolation Forest.
    """

    def __init__(self):
        bundle = ModelLoader.get_anomaly_detector()

        self.model = bundle["model"]
        self.scaler = bundle["scaler"]
        self.features = bundle["features"]

    def detect(self, telemetry: dict[str, Any]) -> dict:
        """
        Detect anomalous network / cluster behavior.

        Returns:
            {
                anomaly: bool,
                prediction: int,
                anomaly_score: float
            }
        """

        # Validate required features
        missing = [
            feature
            for feature in self.features
            if feature not in telemetry
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        # Keep feature order
        values = {
            feature: telemetry[feature]
            for feature in self.features
        }

        df = pd.DataFrame([values])

        # Scale input
        scaled = self.scaler.transform(df)

        # Isolation Forest Prediction
        prediction = int(self.model.predict(scaled)[0])

        # Score
        score = float(self.model.decision_function(scaled)[0])

        # Isolation Forest
        # 1 = Normal
        # -1 = Anomaly

        return {
            "prediction": prediction,
            "anomaly": prediction == -1,
            "status": "Anomaly" if prediction == -1 else "Normal",
            "anomaly_score": round(score, 4),
        }