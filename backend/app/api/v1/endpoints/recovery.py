"""
Recovery API

AI Recovery Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.recovery_controller import recovery_controller
from app.database.session import get_db

router = APIRouter(
    prefix="/recovery",
    tags=["Recovery"],
)


@router.post("/start/{node_id}")
async def start_recovery(
    node_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Start recovery process.
    """

    result = await recovery_controller.start(
        db=db,
        node_id=node_id,
    )

    return {
        "success": True,
        "data": result,
    }


@router.get("/status/{node_id}")
async def recovery_status(
    node_id: str,
):
    """
    Get recovery status.
    """

    result = await recovery_controller.status(
        node_id=node_id,
    )

    return {
        "success": True,
        "data": result,
    }


@router.get("/history/{node_id}")
async def recovery_history(
    node_id: str,
):
    """
    Recovery history.
    """

    result = await recovery_controller.history(
        node_id=node_id,
    )

    return {
        "success": True,
        "data": result,
    }