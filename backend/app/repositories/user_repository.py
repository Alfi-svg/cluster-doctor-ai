"""
User Repository
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model.
    """

    def __init__(self):
        super().__init__(User)

    # =====================================================
    # Get User By Email
    # =====================================================

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> Optional[User]:

        result = await db.execute(

            select(User).where(
                User.email == email
            )

        )

        return result.scalar_one_or_none()

    # =====================================================
    # Get Active Users
    # =====================================================

    async def get_active_users(
        self,
        db: AsyncSession,
    ) -> list[User]:

        result = await db.execute(

            select(User).where(
                User.is_active == True
            )

        )

        return result.scalars().all()

    # =====================================================
    # Get Superusers
    # =====================================================

    async def get_superusers(
        self,
        db: AsyncSession,
    ) -> list[User]:

        result = await db.execute(

            select(User).where(
                User.is_superuser == True
            )

        )

        return result.scalars().all()


user_repository = UserRepository()