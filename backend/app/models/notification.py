"""
Notification Model
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.enums import NotificationStatus
from app.database.enums import ThreatLevel
from app.database.mixins import PrimaryKeyMixin
from app.database.mixins import TimestampMixin


class Notification(
    Base,
    PrimaryKeyMixin,
    TimestampMixin,
):
    """
    AI Generated Notifications & Alerts
    """

    __tablename__ = "notifications"

    # ---------------------------------------------------------
    # Owner
    # ---------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="notifications",
    )

    # ---------------------------------------------------------
    # Related Resources
    # ---------------------------------------------------------

    cluster_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "clusters.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    node_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "nodes.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    prediction_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "predictions.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Notification Content
    # ---------------------------------------------------------

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Priority
    # ---------------------------------------------------------

    threat_level: Mapped[ThreatLevel] = mapped_column(
        Enum(ThreatLevel),
        default=ThreatLevel.LOW,
        nullable=False,
    )

    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus),
        default=NotificationStatus.UNREAD,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Read Information
    # ---------------------------------------------------------

    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    cluster = relationship("Cluster")

    node = relationship("Node")

    prediction = relationship("Prediction")

    # ---------------------------------------------------------

    def __repr__(self):
        return (
            f"<Notification("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status.value}')>"
        )