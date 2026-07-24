"""
Dashboard API

Provides all dashboard information.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.dashboard_controller import dashboard_controller
from app.database.session import get_db

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# =====================================================
# Dashboard Overview
# =====================================================

@router.get("/overview")
async def dashboard_overview(
    db: AsyncSession = Depends(get_db),
):
    """
    Main dashboard overview.
    """

    result = await dashboard_controller.overview(
        db=db,
    )

    return {
        "success": True,
        "data": result,
    }


# =====================================================
# Dashboard Health
# =====================================================

@router.get("/health")
async def dashboard_health(
    db: AsyncSession = Depends(get_db),
):
    """
    Cluster health summary.
    """

    result = await dashboard_controller.overview(
        db=db,
    )

    return {
        "success": True,
        "healthy_clusters": result["healthy_clusters"],
        "warning_clusters": result["warning_clusters"],
        "critical_clusters": result["critical_clusters"],
        "online_nodes": result["online_nodes"],
        "offline_nodes": result["offline_nodes"],
        "system_health": result["system_health"],
    }


# =====================================================
# Dashboard Statistics
# =====================================================

@router.get("/statistics")
async def dashboard_statistics(
    db: AsyncSession = Depends(get_db),
):
    """
    Dashboard statistics.
    """

    result = await dashboard_controller.overview(
        db=db,
    )

    return {
        "success": True,
        "clusters": result["clusters"],
        "nodes": result["nodes"],
        "pending_predictions": result["pending_predictions"],
        "critical_notifications": result["critical_notifications"],
    }


# =====================================================
# Dashboard Summary
# =====================================================

@router.get("/summary")
async def dashboard_summary(
    db: AsyncSession = Depends(get_db),
):
    """
    Dashboard summary.
    """

    result = await dashboard_controller.overview(
        db=db,
    )

    return {
        "success": True,
        "summary": result,
    }