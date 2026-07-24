"""
Common Shared Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


# ==========================================================
# Base Schema
# ==========================================================

class BaseSchema(BaseModel):
    """
    Base schema for all response models.
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )


# ==========================================================
# Timestamp Schema
# ==========================================================

class TimestampSchema(BaseSchema):
    """
    Adds created/updated timestamps.
    """

    created_at: datetime | None = None
    updated_at: datetime | None = None


# ==========================================================
# Generic Message Response
# ==========================================================

class MessageResponse(BaseSchema):
    """
    Generic message response.
    """

    success: bool = True
    message: str


# ==========================================================
# Delete Response
# ==========================================================

class DeleteResponse(MessageResponse):
    """
    Delete response.
    """

    deleted_id: int | None = None


# ==========================================================
# Generic Success Response
# ==========================================================

class SuccessResponse(MessageResponse):
    """
    Generic success response with payload.
    """

    data: Any | None = None


# ==========================================================
# Generic Error Response
# ==========================================================

class ErrorResponse(BaseSchema):
    """
    Generic error response.
    """

    success: bool = False
    message: str
    errors: Any | None = None