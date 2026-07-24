"""
AI Chat Endpoint
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.services.chat_service import chat_service

router = APIRouter(
    prefix="/chatbot",
    tags=["AI Chat"],
)


@router.post("/")
async def chatbot(
    payload: dict,
    current_user: User = Depends(get_current_user),
):
    """
    AI Chat Endpoint
    """

    try:

        response = await chat_service.chat(
            question=payload.get("question", ""),
            history=payload.get("history", []),
            cluster=payload.get("cluster"),
            node=payload.get("node"),
            telemetry=payload.get("telemetry"),
            prediction=payload.get("prediction"),
        )

        return SuccessResponse(
            message="Chat response generated successfully.",
            data=response.model_dump(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )