"""
User Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field

from app.database.enums import UserRole
from app.schemas.common import BaseSchema


# ==========================================================
# Base Schema
# ==========================================================

class UserBase(BaseSchema):

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    email: EmailStr


# ==========================================================
# Create User
# ==========================================================

class UserCreate(UserBase):

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


# ==========================================================
# Login
# ==========================================================

class UserLogin(BaseSchema):

    email: EmailStr

    password: str


# ==========================================================
# Update User
# ==========================================================

class UserUpdate(BaseSchema):

    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=128,
    )

    is_active: Optional[bool] = None


# ==========================================================
# Response
# ==========================================================

class UserResponse(UserBase):

    model_config = ConfigDict(from_attributes=True)

    id: int

    role: UserRole

    is_active: bool

    is_superuser: bool

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Profile
# ==========================================================

class UserProfile(UserResponse):

    total_clusters: int = 0

    total_experiments: int = 0

    total_notifications: int = 0


# ==========================================================
# List Response
# ==========================================================

class UserListResponse(BaseSchema):

    total: int

    users: list[UserResponse]