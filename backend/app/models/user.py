"""
User Model
"""

from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.enums import UserRole
from app.database.mixins import PrimaryKeyMixin
from app.database.mixins import TimestampMixin


class User(
    Base,
    PrimaryKeyMixin,
    TimestampMixin,
):
    """
    System User
    """

    __tablename__ = "users"

    # ---------------------------------------------------------
    # Basic Information
    # ---------------------------------------------------------

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Role
    # ---------------------------------------------------------

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.RESEARCHER,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    clusters = relationship(
        "Cluster",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    experiments = relationship(
        "Experiment",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"