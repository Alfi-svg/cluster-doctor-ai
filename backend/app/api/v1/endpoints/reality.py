"""
Reality API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.reality_controller import reality_controller
from app.database.session import get_db

router = APIRouter(
    prefix="/reality",
    tags=["Reality"],
)


@router.post("/compare/{node_id}")
async def compare_node(
    node_id: str,
    telemetry: dict,
    db: AsyncSession = Depends(get_db),
):
    """
    Compare live telemetry
    with Digital Twin.
    """

    result = await reality_controller.compare(
        db=db,
        node_id=node_id,
        telemetry=telemetry,
    )

    return {
        "success": True,
        "data": result,
    }


@router.get("/summary")
async def summary(
    db: AsyncSession = Depends(get_db),
):
    """
    Reality Summary
    """

    result = await reality_controller.summary(
        db=db,
    )

    return {
        "success": True,
        "data": result,
    }