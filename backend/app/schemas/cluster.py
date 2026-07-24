"""
Cluster Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic import Field

from app.database.enums import ClusterStatus
from app.schemas.common import BaseSchema


# ==========================================================
# Base Schema
# ==========================================================

class ClusterBase(BaseSchema):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    location: Optional[str] = Field(
        default=None,
        max_length=150,
    )


# ==========================================================
# Create
# ==========================================================

class ClusterCreate(ClusterBase):
    pass


# ==========================================================
# Update
# ==========================================================

class ClusterUpdate(BaseSchema):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    location: Optional[str] = None

    status: Optional[ClusterStatus] = None


# ==========================================================
# Response
# ==========================================================

class ClusterResponse(ClusterBase):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    owner_id: int

    health_score: float

    status: ClusterStatus

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Dashboard Summary
# ==========================================================

class ClusterSummary(ClusterResponse):

    total_nodes: int = 0

    active_nodes: int = 0

    offline_nodes: int = 0

    running_experiments: int = 0

    active_alerts: int = 0


# ==========================================================
# Health Response
# ==========================================================

class ClusterHealth(BaseSchema):

    cluster_id: int

    cluster_name: str

    health_score: float

    status: ClusterStatus

    cpu_usage: float

    gpu_usage: float

    memory_usage: float

    average_temperature: float


# ==========================================================
# List Response
# ==========================================================

class ClusterListResponse(BaseSchema):

    total: int

    clusters: list[ClusterResponse]