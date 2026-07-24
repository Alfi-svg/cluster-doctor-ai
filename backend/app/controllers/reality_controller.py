"""
Reality Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.reality_service import reality_service


class RealityController:

    async def compare(
        self,
        db: AsyncSession,
        node_id: str,
        telemetry: dict,
    ):
        return await reality_service.compare(
            db=db,
            node_id=node_id,
            telemetry=telemetry,
        )

    async def summary(
        self,
        db: AsyncSession,
    ):
        return await reality_service.summary(
            db=db,
        )


reality_controller = RealityController()