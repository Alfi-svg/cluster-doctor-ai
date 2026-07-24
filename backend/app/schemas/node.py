"""
Node Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic import Field

from app.database.enums import NodeStatus
from app.schemas.common import BaseSchema


# ==========================================================
# Base Schema
# ==========================================================

class NodeBase(BaseSchema):

    hostname: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    ip_address: str = Field(
        ...,
        max_length=45,
    )

    operating_system: Optional[str] = None

    cpu_model: Optional[str] = None

    cpu_cores: int = 0

    gpu_model: Optional[str] = None

    gpu_count: int = 0

    ram_gb: float = 0.0

    storage_gb: float = 0.0


# ==========================================================
# Create
# ==========================================================

class NodeCreate(NodeBase):

    cluster_id: int


# ==========================================================
# Update
# ==========================================================

class NodeUpdate(BaseSchema):

    hostname: Optional[str] = None

    ip_address: Optional[str] = None

    operating_system: Optional[str] = None

    cpu_model: Optional[str] = None

    cpu_cores: Optional[int] = None

    gpu_model: Optional[str] = None

    gpu_count: Optional[int] = None

    ram_gb: Optional[float] = None

    storage_gb: Optional[float] = None

    status: Optional[NodeStatus] = None


# ==========================================================
# Response
# ==========================================================

class NodeResponse(NodeBase):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    cluster_id: int

    cpu_usage: float

    gpu_usage: float

    memory_usage: float

    temperature: float

    power_consumption: float

    status: NodeStatus

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Dashboard Summary
# ==========================================================

class NodeSummary(NodeResponse):

    latest_prediction: Optional[str] = None

    latest_risk_score: Optional[float] = None

    latest_confidence: Optional[float] = None


# ==========================================================
# Health
# ==========================================================

class NodeHealth(BaseSchema):

    node_id: int

    hostname: str

    status: NodeStatus

    cpu_usage: float

    gpu_usage: float

    memory_usage: float

    temperature: float

    power_consumption: float

    health_score: float


# ==========================================================
# List
# ==========================================================

class NodeListResponse(BaseSchema):

    total: int

    nodes: list[NodeResponse]