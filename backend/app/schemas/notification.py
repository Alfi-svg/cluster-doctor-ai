"""
Notification Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic import Field

from app.database.enums import NotificationStatus
from app.database.enums import ThreatLevel
from app.schemas.common import BaseSchema


# ==========================================================
# Base Schema
# ==========================================================

class NotificationBase(BaseSchema):

    title: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    message: str = Field(
        ...,
        min_length=2,
    )

    category: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    threat_level: ThreatLevel = ThreatLevel.LOW


# ==========================================================
# Create
# ==========================================================

class NotificationCreate(NotificationBase):

    user_id: int

    cluster_id: Optional[int] = None

    node_id: Optional[int] = None

    prediction_id: Optional[int] = None


# ==========================================================
# Update
# ==========================================================

class NotificationUpdate(BaseSchema):

    status: Optional[NotificationStatus] = None


# ==========================================================
# Response
# ==========================================================

class NotificationResponse(NotificationBase):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    user_id: int

    cluster_id: Optional[int]

    node_id: Optional[int]

    prediction_id: Optional[int]

    status: NotificationStatus

    read_at: Optional[datetime]

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Dashboard Card
# ==========================================================

class NotificationCard(BaseSchema):

    id: int

    title: str

    category: str

    threat_level: ThreatLevel

    status: NotificationStatus

    created_at: datetime


# ==========================================================
# Summary
# ==========================================================

class NotificationSummary(BaseSchema):

    total_notifications: int

    unread_notifications: int

    critical_notifications: int

    high_notifications: int

    medium_notifications: int

    low_notifications: int


# ==========================================================
# List
# ==========================================================

class NotificationListResponse(BaseSchema):

    total: int

    notifications: list[NotificationResponse]