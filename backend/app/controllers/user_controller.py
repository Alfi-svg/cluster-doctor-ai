"""
User Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

from app.schemas.user import UserUpdate

from app.services.user_service import user_service


class UserController:
    """
    User Controller.

    Coordinates user-related requests.
    """

    # =====================================================
    # Get Current User
    # =====================================================

    async def get_me(
        self,
        current_user: User,
    ) -> User:

        return current_user

    # =====================================================
    # Get User By ID
    # =====================================================

    async def get_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> User:

        return await user_service.get_user(
            db=db,
            user_id=user_id,
        )

    # =====================================================
    # Get All Users
    # =====================================================

    async def get_all_users(
        self,
        db: AsyncSession,
    ) -> list[User]:

        return await user_service.get_all_users(
            db=db,
        )

    # =====================================================
    # Update Profile
    # =====================================================

    async def update_profile(
        self,
        db: AsyncSession,
        current_user: User,
        data: UserUpdate,
    ) -> User:

        return await user_service.update_profile(
            db=db,
            user=current_user,
            data=data,
        )

    # =====================================================
    # Activate User
    # =====================================================

    async def activate_user(
        self,
        db: AsyncSession,
        user: User,
    ) -> User:

        return await user_service.activate(
            db=db,
            user=user,
        )

    # =====================================================
    # Deactivate User
    # =====================================================

    async def deactivate_user(
        self,
        db: AsyncSession,
        user: User,
    ) -> User:

        return await user_service.deactivate(
            db=db,
            user=user,
        )

    # =====================================================
    # Delete User
    # =====================================================

    async def delete_user(
        self,
        db: AsyncSession,
        user: User,
    ) -> bool:

        return await user_service.delete(
            db=db,
            user=user,
        )


user_controller = UserController()