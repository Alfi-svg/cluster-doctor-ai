"""
Notification Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification

from app.schemas.notification import NotificationCreate

from app.services.notification_service import notification_service


class NotificationController:
    """
    Notification Controller
    """

    # =====================================================
    # Create Notification
    # =====================================================

    async def create_notification(
        self,
        db: AsyncSession,
        data: NotificationCreate,
    ) -> Notification:

        return await notification_service.create_notification(
            db=db,
            data=data,
        )

    # =====================================================
    # Get Notification
    # =====================================================

    async def get_notification(
        self,
        db: AsyncSession,
        notification_id: int,
    ) -> Notification:

        return await notification_service.get_notification(
            db=db,
            notification_id=notification_id,
        )

    # =====================================================
    # User Notifications
    # =====================================================

    async def get_user_notifications(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Notification]:

        return await notification_service.get_user_notifications(
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

        return await notification_service.get_unread_notifications(
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

        return await notification_service.get_critical_notifications(
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

        return await notification_service.mark_as_read(
            db=db,
            notification_id=notification_id,
        )

    # =====================================================
    # Delete Notification
    # =====================================================

    async def delete_notification(
        self,
        db: AsyncSession,
        notification_id: int,
    ) -> None:

        await notification_service.delete_notification(
            db=db,
            notification_id=notification_id,
        )


notification_controller = NotificationController()