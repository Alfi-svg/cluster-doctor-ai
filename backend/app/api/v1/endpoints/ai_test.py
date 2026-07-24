from fastapi import APIRouter
from app.ai.failure_prediction import FailurePredictionService

router = APIRouter(
    prefix="/ai-test",
    tags=["AI Test"]
)

failure = FailurePredictionService()

@router.post("/failure")
async def test_failure(data: dict):
    return failure.predict(data)