"""
Migration API
"""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.migration_controller import migration_controller
from app.database.session import get_db

router = APIRouter(
    prefix="/migration",
    tags=["Migration"],
)


@router.post("/start")
async def start_migration(
    prediction: dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    result = await migration_controller.start(
        db=db,
        prediction=prediction,
    )

    return {
        "success": True,
        "result": result,
    }


@router.get("/history")
async def migration_history():

    history = await migration_controller.history()

    return {
        "success": True,
        "history": history,
    }


@router.get("/{migration_id}")
async def migration_details(
    migration_id: str,
):

    details = await migration_controller.details(
        migration_id
    )

    return {
        "success": True,
        "data": details,
    }