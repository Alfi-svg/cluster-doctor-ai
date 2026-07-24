"""
Recovery Controller

Handles recovery requests from API
and delegates business logic to Recovery Service.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.recovery_service import recovery_service


class RecoveryController:

    async def start(
        self,
        db: AsyncSession,
        node_id: str,
    ):
        """
        Start recovery.
        """

        return await recovery_service.start(
            db=db,
            node_id=node_id,
        )

    async def status(
        self,
        node_id: str,
    ):
        """
        Recovery status.
        """

        return await recovery_service.status(
            node_id=node_id,
        )

    async def history(
        self,
        node_id: str,
    ):
        """
        Recovery history.
        """

        return await recovery_service.history(
            node_id=node_id,
        )


recovery_controller = RecoveryController()