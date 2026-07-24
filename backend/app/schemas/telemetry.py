"""
Telemetry Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic import Field

from app.schemas.common import BaseSchema


# ==========================================================
# Base Schema
# ==========================================================

class TelemetryBase(BaseSchema):

    cpu_usage: float = Field(..., ge=0, le=100)

    cpu_temperature: float = Field(..., ge=0)

    cpu_frequency: float = Field(..., ge=0)

    gpu_usage: float = Field(..., ge=0, le=100)

    gpu_temperature: float = Field(..., ge=0)

    gpu_memory_usage: float = Field(..., ge=0, le=100)

    gpu_power: float = Field(..., ge=0)

    ram_usage: float = Field(..., ge=0, le=100)

    swap_usage: float = Field(..., ge=0, le=100)

    disk_usage: float = Field(..., ge=0, le=100)

    disk_read_speed: float = Field(..., ge=0)

    disk_write_speed: float = Field(..., ge=0)

    network_in: float = Field(..., ge=0)

    network_out: float = Field(..., ge=0)

    latency: float = Field(..., ge=0)

    packet_loss: float = Field(..., ge=0, le=100)


# ==========================================================
# Create
# ==========================================================

class TelemetryCreate(TelemetryBase):

    cluster_id: int

    node_id: int


# ==========================================================
# Response
# ==========================================================

class TelemetryResponse(TelemetryBase):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    cluster_id: int

    node_id: int

    recorded_at: datetime


# ==========================================================
# Live Dashboard
# ==========================================================

class TelemetryRealtime(BaseSchema):

    node_id: int

    hostname: str

    cpu_usage: float

    gpu_usage: float

    memory_usage: float

    temperature: float

    network_in: float

    network_out: float

    timestamp: datetime


# ==========================================================
# History
# ==========================================================

class TelemetryHistory(BaseSchema):

    node_id: int

    start_time: datetime

    end_time: datetime

    records: list[TelemetryResponse]


# ==========================================================
# List
# ==========================================================

class TelemetryListResponse(BaseSchema):

    total: int

    telemetry: list[TelemetryResponse]