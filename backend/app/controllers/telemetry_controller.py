"""
Telemetry Controller
"""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telemetry import Telemetry

from app.schemas.telemetry import TelemetryCreate

from app.services.telemetry_service import telemetry_service


class TelemetryController:
    """
    Telemetry Controller
    """

    # =====================================================
    # Create Telemetry
    # =====================================================

    async def create_telemetry(
        self,
        db: AsyncSession,
        data: TelemetryCreate,
    ) -> Telemetry:

        return await telemetry_service.create_telemetry(
            db=db,
            data=data,
        )

    # =====================================================
    # Get Telemetry By ID
    # =====================================================

    async def get_telemetry(
        self,
        db: AsyncSession,
        telemetry_id: int,
    ) -> Telemetry:

        return await telemetry_service.get_telemetry(
            db=db,
            telemetry_id=telemetry_id,
        )

    # =====================================================
    # Latest Telemetry
    # =====================================================

    async def get_latest(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> Telemetry:

        return await telemetry_service.get_latest(
            db=db,
            node_id=node_id,
        )

    # =====================================================
    # Telemetry History
    # =====================================================

    async def get_history(
        self,
        db: AsyncSession,
        node_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Telemetry]:

        return await telemetry_service.get_history(
            db=db,
            node_id=node_id,
            start_time=start_time,
            end_time=end_time,
        )

    # =====================================================
    # Cluster Telemetry
    # =====================================================

    async def get_cluster_telemetry(
        self,
        db: AsyncSession,
        cluster_id: int,
    ) -> list[Telemetry]:

        return await telemetry_service.get_cluster_telemetry(
            db=db,
            cluster_id=cluster_id,
        )


telemetry_controller = TelemetryController()