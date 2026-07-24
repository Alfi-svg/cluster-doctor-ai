"""
Cluster Model
"""

from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.enums import ClusterStatus
from app.database.mixins import PrimaryKeyMixin
from app.database.mixins import TimestampMixin


class Cluster(
    Base,
    PrimaryKeyMixin,
    TimestampMixin,
):
    """
    AI Compute Cluster
    """

    __tablename__ = "clusters"

    # ---------------------------------------------------------
    # Basic Information
    # ---------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    health_score: Mapped[float] = mapped_column(
        Float,
        default=100.0,
        nullable=False,
    )

    status: Mapped[ClusterStatus] = mapped_column(
        Enum(ClusterStatus),
        default=ClusterStatus.HEALTHY,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Ownership
    # ---------------------------------------------------------

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    owner = relationship(
        "User",
        back_populates="clusters",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    nodes = relationship(
        "Node",
        back_populates="cluster",
        cascade="all, delete-orphan",
    )

    telemetry = relationship(
        "Telemetry",
        back_populates="cluster",
        cascade="all, delete-orphan",
    )

    predictions = relationship(
        "Prediction",
        back_populates="cluster",
        cascade="all, delete-orphan",
    )

    experiments = relationship(
        "Experiment",
        back_populates="cluster",
        cascade="all, delete-orphan",
    )

    # ---------------------------------------------------------

    def __repr__(self):
        return (
            f"<Cluster(id={self.id}, "
            f"name='{self.name}', "
            f"status='{self.status.value}')>"
        )