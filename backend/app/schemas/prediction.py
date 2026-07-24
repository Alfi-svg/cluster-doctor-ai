"""
Prediction Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import Field

from app.database.enums import PredictionStatus
from app.schemas.common import BaseSchema


# ==========================================================
# Base Schema
# ==========================================================


class PredictionBase(BaseSchema):

    model_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    prediction_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=100,
    )

    risk_score: float = Field(
        ...,
        ge=0,
        le=100,
    )

    probability: float = Field(
        ...,
        ge=0,
        le=100,
    )

    predicted_label: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    recommendation: Optional[str] = None

    explanation: Optional[str] = None


# ==========================================================
# Request
# ==========================================================


class PredictionRequest(BaseSchema):

    cluster_id: int

    node_id: int


# ==========================================================
# Create
# ==========================================================


class PredictionCreate(PredictionBase):

    cluster_id: int

    node_id: int

    status: PredictionStatus = PredictionStatus.PENDING

    predicted_at: Optional[datetime] = None


# ==========================================================
# Update
# ==========================================================


class PredictionUpdate(BaseSchema):

    status: Optional[PredictionStatus] = None

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    risk_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    probability: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    predicted_label: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    recommendation: Optional[str] = None

    explanation: Optional[str] = None


# ==========================================================
# Response
# ==========================================================


class PredictionResponse(PredictionBase):

    id: int

    cluster_id: int

    node_id: int

    status: PredictionStatus

    predicted_at: datetime

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Summary
# ==========================================================


class PredictionSummary(BaseSchema):

    id: int

    model_name: str

    prediction_type: str

    predicted_label: str

    confidence: float

    risk_score: float

    probability: float

    status: PredictionStatus

    predicted_at: datetime


# ==========================================================
# List Response
# ==========================================================


class PredictionListResponse(BaseSchema):

    total: int

    predictions: list[PredictionResponse]