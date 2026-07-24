"""
Notification Service
"""

from datetime import datetime, UTC

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import NotificationStatus
from app.models.notification import Notification

from app.repositories.notification_repository import (
    notification_repository,
)
from app.repositories.user_repository import (
    user_repository,
)

from app.schemas.notification import (
    NotificationCreate,
)


class NotificationService:
    """
    Business Logic for Notifications
    """

    # =====================================================
    # Create Notification
    # =====================================================

    async def create_notification(
        self,
        db: AsyncSession,
        data: NotificationCreate,
    ) -> Notification:

        user = await user_repository.get(
            db,
            data.user_id,
        )

        if not user:
            raise ValueError("User not found.")

        return await notification_repository.create(
            db=db,
            **data.model_dump(),
        )

    # =====================================================
    # Get Notification
    # =====================================================

    async def get_notification(
        self,
        db: AsyncSession,
        notification_id: int,
    ) -> Notification:

        notification = await notification_repository.get(
            db,
            notification_id,
        )

        if not notification:
            raise ValueError("Notification not found.")

        return notification

    # =====================================================
    # User Notifications
    # =====================================================

    async def get_user_notifications(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Notification]:

        return await notification_repository.get_by_user(
            db=db,
            user_id=user_id,
        )

    # =====================================================
    # Unread Notifications
    # =====================================================

    async def get_unread_notifications(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Notification]:

        return await notification_repository.get_unread(
            db=db,
            user_id=user_id,
        )

    # =====================================================
    # Critical Notifications
    # =====================================================

    async def get_critical_notifications(
        self,
        db: AsyncSession,
    ) -> list[Notification]:

        return await notification_repository.get_critical(
            db=db,
        )

    # =====================================================
    # Mark As Read
    # =====================================================

    async def mark_as_read(
        self,
        db: AsyncSession,
        notification_id: int,
    ) -> Notification:

        notification = await self.get_notification(
            db,
            notification_id,
        )

        notification.read_at = datetime.now(UTC)

        return await notification_repository.mark_as_read(
            db=db,
            notification=notification,
        )

    # =====================================================
    # Delete Notification
    # =====================================================

    async def delete_notification(
        self,
        db: AsyncSession,
        notification_id: int,
    ) -> None:

        notification = await self.get_notification(
            db,
            notification_id,
        )

        await notification_repository.delete(
            db,
            notification,
        )


notification_service = NotificationService()