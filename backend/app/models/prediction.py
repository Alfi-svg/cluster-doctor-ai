"""
Prediction Model
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.enums import PredictionStatus
from app.database.mixins import PrimaryKeyMixin
from app.database.mixins import TimestampMixin


class Prediction(
    Base,
    PrimaryKeyMixin,
    TimestampMixin,
):
    """
    AI Prediction generated from telemetry.
    """

    __tablename__ = "predictions"

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
        back_populates="predictions",
    )

    node = relationship(
        "Node",
        back_populates="predictions",
    )

    # ---------------------------------------------------------
    # AI Information
    # ---------------------------------------------------------

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    prediction_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[PredictionStatus] = mapped_column(
        Enum(PredictionStatus),
        default=PredictionStatus.PENDING,
        nullable=False,
    )

    # ---------------------------------------------------------
    # AI Scores
    # ---------------------------------------------------------

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    probability: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # ---------------------------------------------------------
    # AI Output
    # ---------------------------------------------------------

    predicted_label: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    recommendation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Time
    # ---------------------------------------------------------

    predicted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------

    def __repr__(self):
        return (
            f"<Prediction("
            f"id={self.id}, "
            f"model='{self.model_name}', "
            f"confidence={self.confidence:.2f})>"
        )