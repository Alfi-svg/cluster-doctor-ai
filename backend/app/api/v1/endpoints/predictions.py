"""
Prediction Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_active_user,
    get_database,
)
from app.controllers.prediction_controller import prediction_controller
from app.models.user import User
from app.schemas.prediction import (
    PredictionCreate,
    PredictionResponse,
    PredictionUpdate,
)
from app.services.prediction_service import (
    EntityNotFoundError,
    TelemetryNotFoundError,
)

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


# =====================================================
# Create Prediction
# =====================================================

@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_prediction(
    data: PredictionCreate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await prediction_controller.create_prediction(
            db=db,
            data=data,
        )

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except TelemetryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Latest Prediction
# =====================================================

@router.get(
    "/latest/{node_id}",
    response_model=PredictionResponse,
)
async def latest_prediction(
    node_id: int,
    db: AsyncSession = Depends(get_database),
):
    prediction = await prediction_controller.get_latest_prediction(
        db=db,
        node_id=node_id,
    )

    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found.",
        )

    return prediction


# =====================================================
# Node Predictions
# =====================================================

@router.get(
    "/node/{node_id}",
    response_model=list[PredictionResponse],
)
async def node_predictions(
    node_id: int,
    db: AsyncSession = Depends(get_database),
):
    return await prediction_controller.get_node_predictions(
        db=db,
        node_id=node_id,
    )


# =====================================================
# Model Predictions
# =====================================================

@router.get(
    "/model/{model_name}",
    response_model=list[PredictionResponse],
)
async def model_predictions(
    model_name: str,
    db: AsyncSession = Depends(get_database),
):
    return await prediction_controller.get_model_predictions(
        db=db,
        model_name=model_name,
    )


# =====================================================
# High Risk Predictions
# =====================================================

@router.get(
    "/high-risk",
    response_model=list[PredictionResponse],
)
async def high_risk_predictions(
    threshold: float = Query(80.0, ge=0, le=100),
    db: AsyncSession = Depends(get_database),
):
    return await prediction_controller.get_high_risk_predictions(
        db=db,
        threshold=threshold,
    )


# =====================================================
# Pending Predictions
# =====================================================

@router.get(
    "/pending",
    response_model=list[PredictionResponse],
)
async def pending_predictions(
    db: AsyncSession = Depends(get_database),
):
    return await prediction_controller.get_pending_predictions(
        db=db,
    )


# =====================================================
# Update Prediction
# =====================================================

@router.put(
    "/{prediction_id}",
    response_model=PredictionResponse,
)
async def update_prediction(
    prediction_id: int,
    data: PredictionUpdate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await prediction_controller.update_prediction(
            db=db,
            prediction_id=prediction_id,
            data=data,
        )

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Delete Prediction
# =====================================================

@router.delete(
    "/{prediction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_prediction(
    prediction_id: int,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        await prediction_controller.delete_prediction(
            db=db,
            prediction_id=prediction_id,
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Get Prediction
# =====================================================

@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse,
)
async def get_prediction(
    prediction_id: int,
    db: AsyncSession = Depends(get_database),
):
    prediction = await prediction_controller.get_prediction(
        db=db,
        prediction_id=prediction_id,
    )

    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found.",
        )

    return prediction