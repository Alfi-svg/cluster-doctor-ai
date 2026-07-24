"""
User Endpoints
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_database,
    get_current_active_user,
    get_current_admin,
)

from app.controllers.user_controller import (
    user_controller,
)

from app.models.user import User

from app.schemas.user import (
    UserResponse,
    UserUpdate,
)

router = APIRouter()


# =====================================================
# Current User
# =====================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(get_current_active_user),
):

    return await user_controller.get_me(
        current_user=current_user,
    )


# =====================================================
# Get User By ID
# =====================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_database),
    _: User = Depends(get_current_admin),
):

    return await user_controller.get_user(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Get All Users
# =====================================================

@router.get(
    "",
    response_model=list[UserResponse],
)
async def get_all_users(
    db: AsyncSession = Depends(get_database),
    _: User = Depends(get_current_admin),
):

    return await user_controller.get_all_users(
        db=db,
    )


# =====================================================
# Update Current User
# =====================================================

@router.put(
    "/me",
    response_model=UserResponse,
)
async def update_profile(
    data: UserUpdate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):

    return await user_controller.update_profile(
        db=db,
        current_user=current_user,
        data=data,
    )


# =====================================================
# Activate User
# =====================================================

@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
)
async def activate_user(
    user_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_database),
    _: User = Depends(get_current_admin),
):

    return await user_controller.activate_user(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Deactivate User
# =====================================================

@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
)
async def deactivate_user(
    user_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_database),
    _: User = Depends(get_current_admin),
):

    return await user_controller.deactivate_user(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Delete User
# =====================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_database),
    _: User = Depends(get_current_admin),
):

    await user_controller.delete_user(
        db=db,
        user_id=user_id,
    )

    return None