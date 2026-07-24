"""
Notification Repository
"""

from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import NotificationStatus
from app.database.enums import ThreatLevel
from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """
    Repository for Notification model.
    """

    def __init__(self):
        super().__init__(Notification)

    # =====================================================
    # User Notifications
    # =====================================================

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Notification]:

        result = await db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(desc(Notification.created_at))
        )

        return result.scalars().all()

    # =====================================================
    # Unread Notifications
    # =====================================================

    async def get_unread(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Notification]:

        result = await db.execute(
            select(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.status == NotificationStatus.UNREAD,
            )
            .order_by(desc(Notification.created_at))
        )

        return result.scalars().all()

    # =====================================================
    # Critical Notifications
    # =====================================================

    async def get_critical(
        self,
        db: AsyncSession,
    ) -> list[Notification]:

        result = await db.execute(
            select(Notification)
            .where(
                Notification.threat_level == ThreatLevel.CRITICAL
            )
            .order_by(desc(Notification.created_at))
        )

        return result.scalars().all()

    # =====================================================
    # Mark As Read
    # =====================================================

    async def mark_as_read(
        self,
        db: AsyncSession,
        notification: Notification,
    ) -> Notification:

        notification.status = NotificationStatus.READ

        await db.commit()
        await db.refresh(notification)

        return notification


notification_repository = NotificationRepository()