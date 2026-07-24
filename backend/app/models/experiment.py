"""
Experiment Model
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.enums import ExperimentStatus
from app.database.mixins import PrimaryKeyMixin
from app.database.mixins import TimestampMixin


class Experiment(
    Base,
    PrimaryKeyMixin,
    TimestampMixin,
):
    """
    AI Training / Research Experiment
    """

    __tablename__ = "experiments"

    # ---------------------------------------------------------
    # Ownership
    # ---------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cluster_id: Mapped[int] = mapped_column(
        ForeignKey("clusters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="experiments",
    )

    cluster = relationship(
        "Cluster",
        back_populates="experiments",
    )

    # ---------------------------------------------------------
    # Experiment Details
    # ---------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    framework: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    model_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    dataset_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Resources
    # ---------------------------------------------------------

    allocated_gpus: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    allocated_cpus: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    allocated_memory_gb: Mapped[float] = mapped_column(
        Float,
        default=4.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Progress
    # ---------------------------------------------------------

    progress: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    status: Mapped[ExperimentStatus] = mapped_column(
        Enum(ExperimentStatus),
        default=ExperimentStatus.RUNNING,
        nullable=False,
    )

    # ---------------------------------------------------------
    # AI Guardian
    # ---------------------------------------------------------

    guardian_score: Mapped[float] = mapped_column(
        Float,
        default=100.0,
        nullable=False,
    )

    failure_probability: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    recommendation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ---------------------------------------------------------

    def __repr__(self):
        return (
            f"<Experiment("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"status='{self.status.value}')>"
        )