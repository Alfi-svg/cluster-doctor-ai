from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Cluster Doctor API",
        "timestamp": datetime.utcnow(),
    }