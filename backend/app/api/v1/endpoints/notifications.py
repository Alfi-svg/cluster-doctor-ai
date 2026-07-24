"""
Notification Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_active_user,
    get_database,
)
from app.controllers.notification_controller import (
    notification_controller,
)
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# =====================================================
# Create Notification
# =====================================================

@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_notification(
    data: NotificationCreate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await notification_controller.create_notification(
            db=db,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# Get Notification By ID
# =====================================================

@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
async def get_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_database),
):
    try:
        return await notification_controller.get_notification(
            db=db,
            notification_id=notification_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# User Notifications
# =====================================================

@router.get(
    "/user/{user_id}",
    response_model=list[NotificationResponse],
)
async def get_user_notifications(
    user_id: int,
    db: AsyncSession = Depends(get_database),
):
    return await notification_controller.get_user_notifications(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Unread Notifications
# =====================================================

@router.get(
    "/user/{user_id}/unread",
    response_model=list[NotificationResponse],
)
async def get_unread_notifications(
    user_id: int,
    db: AsyncSession = Depends(get_database),
):
    return await notification_controller.get_unread_notifications(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Critical Notifications
# =====================================================

@router.get(
    "/critical",
    response_model=list[NotificationResponse],
)
async def get_critical_notifications(
    db: AsyncSession = Depends(get_database),
):
    return await notification_controller.get_critical_notifications(
        db=db,
    )


# =====================================================
# Mark Notification As Read
# =====================================================

@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
async def mark_as_read(
    notification_id: int,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await notification_controller.mark_as_read(
            db=db,
            notification_id=notification_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Delete Notification
# =====================================================

@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        await notification_controller.delete_notification(
            db=db,
            notification_id=notification_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )