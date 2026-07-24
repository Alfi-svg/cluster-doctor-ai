from typing import Any


class RecommendationEngine:
    """
    Combines outputs from all AI models and generates
    the final prediction for the backend.
    """

    @staticmethod
    def generate(
        failure: dict[str, Any],
        security: dict[str, Any],
        guardian: dict[str, Any],
    ) -> dict[str, Any]:

        recommendations: list[str] = []
        explanations: list[str] = []

        # -------------------------------------------------
        # Default Values
        # -------------------------------------------------

        model_name = "Failure Predictor"
        prediction_type = "Failure"
        predicted_label = "Healthy"

        confidence = 0.0
        probability = 0.0
        risk_score = 0.0

        # =================================================
        # SECURITY HAS HIGHEST PRIORITY
        # =================================================

        if security["anomaly"]:

            model_name = "Isolation Forest"

            prediction_type = "Security"

            predicted_label = "Security Anomaly"

            confidence = 98.0

            probability = 100.0

            risk_score = 100.0

            recommendations.extend(
                [
                    "Investigate suspicious traffic immediately.",
                    "Run node security diagnostics.",
                    "Review firewall and network logs.",
                    "Temporarily isolate the affected node.",
                ]
            )

            explanations.append(
                "Isolation Forest detected abnormal behaviour."
            )

        # =================================================
        # FAILURE PREDICTION
        # =================================================

        elif failure["failure"]:

            model_name = "Failure Predictor"

            prediction_type = "Hardware Failure"

            predicted_label = "Failure Expected"

            probability = round(
                failure["probability"] * 100,
                2,
            )

            confidence = probability

            risk_score = round(
                failure["risk_score"],
                2,
            )

            recommendations.extend(
                [
                    "Inspect GPU cooling.",
                    "Reduce workload.",
                    "Check power consumption.",
                    "Restart node if necessary.",
                ]
            )

            explanations.append(
                "Hardware failure prediction model detected high failure probability."
            )

        # =================================================
        # EXPERIMENT GUARDIAN
        # =================================================

        elif guardian["risk"]:

            model_name = "Experiment Guardian"

            prediction_type = "Experiment"

            predicted_label = "Training Risk"

            probability = round(
                guardian["probability"] * 100,
                2,
            )

            confidence = probability

            risk_score = round(
                guardian["risk_score"],
                2,
            )

            recommendations.extend(
                [
                    "Reduce GPU memory utilization.",
                    "Lower batch size.",
                    "Monitor training process.",
                    "Consider gradient accumulation.",
                ]
            )

            explanations.append(
                "Experiment Guardian predicts unstable training."
            )

        # =================================================
        # HEALTHY NODE
        # =================================================

        else:

            model_name = "AI Ensemble"

            prediction_type = "Health"

            predicted_label = "Healthy"

            confidence = 99.0

            probability = 0.0

            risk_score = 0.0

            recommendations.append(
                "Node operating normally."
            )

            explanations.append(
                "All AI models indicate healthy operation."
            )

        # =================================================

        return {

            "model_name": model_name,

            "prediction_type": prediction_type,

            "predicted_label": predicted_label,

            "confidence": round(
                confidence,
                2,
            ),

            "probability": round(
                probability,
                2,
            ),

            "risk_score": round(
                risk_score,
                2,
            ),

            "recommendation": "\n".join(
                recommendations
            ),

            "explanation": "\n".join(
                explanations
            ),
        }