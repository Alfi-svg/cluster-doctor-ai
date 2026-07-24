"""
Migration Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.migration_service import migration_service


class MigrationController:

    async def start(
        self,
        db: AsyncSession,
        prediction: dict,
    ):
        return await migration_service.start(
            db=db,
            prediction=prediction,
        )

    async def history(self):
        return await migration_service.history()

    async def details(
        self,
        migration_id: str,
    ):
        return await migration_service.details(
            migration_id
        )


migration_controller = MigrationController()