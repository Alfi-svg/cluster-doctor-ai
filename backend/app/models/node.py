"""
Node Model
"""

from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.enums import NodeStatus
from app.database.mixins import PrimaryKeyMixin
from app.database.mixins import TimestampMixin


class Node(
    Base,
    PrimaryKeyMixin,
    TimestampMixin,
):
    """
    Physical or Virtual Compute Node
    """

    __tablename__ = "nodes"

    # ---------------------------------------------------------
    # Basic Information
    # ---------------------------------------------------------

    hostname: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),   # Supports IPv4 & IPv6
        nullable=False,
        unique=True,
    )

    operating_system: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Hardware Information
    # ---------------------------------------------------------

    cpu_model: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    cpu_cores: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    gpu_model: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    gpu_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    ram_gb: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    storage_gb: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Live Metrics
    # ---------------------------------------------------------

    cpu_usage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    gpu_usage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    memory_usage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    power_consumption: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    status: Mapped[NodeStatus] = mapped_column(
        Enum(NodeStatus),
        default=NodeStatus.ONLINE,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Cluster
    # ---------------------------------------------------------

    cluster_id: Mapped[int] = mapped_column(
        ForeignKey(
            "clusters.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    cluster = relationship(
        "Cluster",
        back_populates="nodes",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    telemetry = relationship(
        "Telemetry",
        back_populates="node",
        cascade="all, delete-orphan",
    )

    predictions = relationship(
        "Prediction",
        back_populates="node",
        cascade="all, delete-orphan",
    )

    # ---------------------------------------------------------

    def __repr__(self):
        return (
            f"<Node("
            f"id={self.id}, "
            f"hostname='{self.hostname}', "
            f"status='{self.status.value}')>"
        )