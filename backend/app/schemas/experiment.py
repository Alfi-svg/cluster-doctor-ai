"""
Experiment Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic import Field

from app.database.enums import ExperimentStatus
from app.schemas.common import BaseSchema


# ==========================================================
# Base Schema
# ==========================================================

class ExperimentBase(BaseSchema):

    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = None

    framework: Optional[str] = None

    model_name: Optional[str] = None

    dataset_name: Optional[str] = None


# ==========================================================
# Create
# ==========================================================

class ExperimentCreate(ExperimentBase):

    cluster_id: int

    allocated_gpus: int = Field(default=1, ge=1)

    allocated_cpus: int = Field(default=1, ge=1)

    allocated_memory_gb: float = Field(default=4.0, ge=1)


# ==========================================================
# Update
# ==========================================================

class ExperimentUpdate(BaseSchema):

    name: Optional[str] = None

    description: Optional[str] = None

    progress: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    status: Optional[ExperimentStatus] = None

    recommendation: Optional[str] = None


# ==========================================================
# Response
# ==========================================================

class ExperimentResponse(ExperimentBase):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    user_id: int

    cluster_id: int

    allocated_gpus: int

    allocated_cpus: int

    allocated_memory_gb: float

    progress: float

    status: ExperimentStatus

    guardian_score: float

    failure_probability: float

    recommendation: Optional[str]

    started_at: datetime

    finished_at: Optional[datetime]

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Dashboard
# ==========================================================

class ExperimentDashboard(BaseSchema):

    id: int

    name: str

    framework: Optional[str]

    model_name: Optional[str]

    dataset_name: Optional[str]

    progress: float

    status: ExperimentStatus

    guardian_score: float

    failure_probability: float


# ==========================================================
# Summary
# ==========================================================

class ExperimentSummary(BaseSchema):

    total_experiments: int

    running: int

    completed: int

    failed: int

    average_guardian_score: float


# ==========================================================
# List
# ==========================================================

class ExperimentListResponse(BaseSchema):

    total: int

    experiments: list[ExperimentResponse]