"""
Generic Base Repository

Provides common CRUD operations for all models.
"""

from typing import Any
from typing import Generic
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic Repository
    """

    def __init__(
        self,
        model: Type[ModelType],
    ):
        self.model = model

    # =====================================================
    # CREATE
    # =====================================================

    async def create(
        self,
        db: AsyncSession,
        **kwargs: Any,
    ) -> ModelType:

        obj = self.model(**kwargs)

        db.add(obj)

        await db.commit()

        await db.refresh(obj)

        return obj

    # =====================================================
    # GET BY ID
    # =====================================================

    async def get(
        self,
        db: AsyncSession,
        obj_id: int,
    ) -> Optional[ModelType]:

        result = await db.execute(

            select(self.model).where(
                self.model.id == obj_id
            )

        )

        return result.scalar_one_or_none()

    # =====================================================
    # GET ALL
    # =====================================================

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:

        result = await db.execute(

            select(self.model)
            .offset(skip)
            .limit(limit)

        )

        return result.scalars().all()

    # =====================================================
    # UPDATE
    # =====================================================

    async def update(
        self,
        db: AsyncSession,
        obj: ModelType,
        **kwargs: Any,
    ) -> ModelType:

        for key, value in kwargs.items():

            setattr(
                obj,
                key,
                value,
            )

        await db.commit()

        await db.refresh(obj)

        return obj

    # =====================================================
    # DELETE
    # =====================================================

    async def delete(
        self,
        db: AsyncSession,
        obj: ModelType,
    ) -> None:

        await db.delete(obj)

        await db.commit()

    # =====================================================
    # EXISTS
    # =====================================================

    async def exists(
        self,
        db: AsyncSession,
        obj_id: int,
    ) -> bool:

        obj = await self.get(
            db,
            obj_id,
        )

        return obj is not None

    # =====================================================
    # COUNT
    # =====================================================

    async def count(
        self,
        db: AsyncSession,
    ) -> int:

        result = await db.execute(
            select(self.model)
        )

        return len(
            result.scalars().all()
        )