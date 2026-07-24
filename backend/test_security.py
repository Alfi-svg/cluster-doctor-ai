from app.ai.recommendation_engine import RecommendationEngine

failure = {
    "failure": True,
    "probability": 0.91,
    "risk_score": 91,
}

security = {
    "anomaly": False,
}

guardian = {
    "risk": False,
    "probability": 0.05,
    "risk_score": 5,
}

result = RecommendationEngine.generate(
    failure,
    security,
    guardian,
)

print(result)