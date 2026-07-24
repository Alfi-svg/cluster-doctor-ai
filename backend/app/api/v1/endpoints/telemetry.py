"""
Telemetry Endpoints
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_active_user,
    get_database,
)

from app.controllers.telemetry_controller import telemetry_controller

from app.models.user import User

from app.schemas.telemetry import (
    TelemetryCreate,
    TelemetryResponse,
)

router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"],
)


# =====================================================
# Create Telemetry
# =====================================================

@router.post(
    "/",
    response_model=TelemetryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_telemetry(
    data: TelemetryCreate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await telemetry_controller.create_telemetry(
            db=db,
            data=data,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# Get Telemetry By ID
# =====================================================

@router.get(
    "/{telemetry_id}",
    response_model=TelemetryResponse,
)
async def get_telemetry(
    telemetry_id: int,
    db: AsyncSession = Depends(get_database),
):
    try:
        return await telemetry_controller.get_telemetry(
            db=db,
            telemetry_id=telemetry_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Latest Telemetry
# =====================================================

@router.get(
    "/latest/{node_id}",
    response_model=TelemetryResponse,
)
async def latest_telemetry(
    node_id: int,
    db: AsyncSession = Depends(get_database),
):
    try:
        return await telemetry_controller.get_latest(
            db=db,
            node_id=node_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Telemetry History
# =====================================================

@router.get(
    "/history/{node_id}",
    response_model=list[TelemetryResponse],
)
async def telemetry_history(
    node_id: int,
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    db: AsyncSession = Depends(get_database),
):
    return await telemetry_controller.get_history(
        db=db,
        node_id=node_id,
        start_time=start_time,
        end_time=end_time,
    )


# =====================================================
# Cluster Telemetry
# =====================================================

@router.get(
    "/cluster/{cluster_id}",
    response_model=list[TelemetryResponse],
)
async def cluster_telemetry(
    cluster_id: int,
    db: AsyncSession = Depends(get_database),
):
    return await telemetry_controller.get_cluster_telemetry(
        db=db,
        cluster_id=cluster_id,
    )