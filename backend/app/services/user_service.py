"""
User Service

Business logic related to users.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import UserUpdate


class UserService:
    """
    User business service.
    """

    # =====================================================
    # Get User By ID
    # =====================================================

    async def get_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> User:

        user = await user_repository.get(
            db,
            user_id,
        )

        if user is None:
            raise ValueError("User not found.")

        return user

    # =====================================================
    # Get User By Email
    # =====================================================

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> User:

        user = await user_repository.get_by_email(
            db,
            email,
        )

        if user is None:
            raise ValueError("User not found.")

        return user

    # =====================================================
    # Get All Users
    # =====================================================

    async def get_all_users(
        self,
        db: AsyncSession,
    ) -> list[User]:

        return await user_repository.get_all(db)

    # =====================================================
    # Update Profile
    # =====================================================

    async def update_profile(
        self,
        db: AsyncSession,
        user: User,
        data: UserUpdate,
    ) -> User:

        update_data = data.model_dump(
            exclude_unset=True
        )

        updated_user = await user_repository.update(
            db,
            user,
            **update_data,
        )

        return updated_user

    # =====================================================
    # Activate User
    # =====================================================

    async def activate(
        self,
        db: AsyncSession,
        user: User,
    ) -> User:

        return await user_repository.update(
            db,
            user,
            is_active=True,
        )

    # =====================================================
    # Deactivate User
    # =====================================================

    async def deactivate(
        self,
        db: AsyncSession,
        user: User,
    ) -> User:

        return await user_repository.update(
            db,
            user,
            is_active=False,
        )

    # =====================================================
    # Delete User
    # =====================================================

    async def delete(
        self,
        db: AsyncSession,
        user: User,
    ) -> bool:

        return await user_repository.delete(
            db,
            user.id,
        )


user_service = UserService()