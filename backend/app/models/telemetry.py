"""
Telemetry Model
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.mixins import PrimaryKeyMixin


class Telemetry(
    Base,
    PrimaryKeyMixin,
):
    """
    Real-time telemetry collected from compute nodes.
    """

    __tablename__ = "telemetry"

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    cluster_id: Mapped[int] = mapped_column(
        ForeignKey(
            "clusters.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    node_id: Mapped[int] = mapped_column(
        ForeignKey(
            "nodes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    cluster = relationship(
        "Cluster",
        back_populates="telemetry",
    )

    node = relationship(
        "Node",
        back_populates="telemetry",
    )

    # ---------------------------------------------------------
    # CPU Metrics
    # ---------------------------------------------------------

    cpu_usage = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    cpu_temperature = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    cpu_frequency = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # GPU Metrics
    # ---------------------------------------------------------

    gpu_usage = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    gpu_temperature = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    gpu_memory_usage = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    gpu_power = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Memory
    # ---------------------------------------------------------

    ram_usage = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    swap_usage = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Storage
    # ---------------------------------------------------------

    disk_usage = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    disk_read_speed = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    disk_write_speed = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Network
    # ---------------------------------------------------------

    network_in = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    network_out = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    latency = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    packet_loss = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Timestamp
    # ---------------------------------------------------------

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------

    def __repr__(self):
        return (
            f"<Telemetry("
            f"id={self.id}, "
            f"node_id={self.node_id}, "
            f"cpu={self.cpu_usage:.1f}%, "
            f"gpu={self.gpu_usage:.1f}%"
            f")>"
        )