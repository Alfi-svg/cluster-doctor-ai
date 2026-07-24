"""
Telemetry Service
"""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telemetry import Telemetry

from app.repositories.cluster_repository import cluster_repository
from app.repositories.node_repository import node_repository
from app.repositories.telemetry_repository import telemetry_repository

from app.schemas.telemetry import (
    TelemetryCreate,
)


class TelemetryService:
    """
    Business Logic for Telemetry
    """

    # =====================================================
    # Create Telemetry
    # =====================================================

    async def create_telemetry(
        self,
        db: AsyncSession,
        data: TelemetryCreate,
    ) -> Telemetry:

        cluster = await cluster_repository.get(
            db,
            data.cluster_id,
        )

        if not cluster:
            raise ValueError("Cluster not found.")

        node = await node_repository.get(
            db,
            data.node_id,
        )

        if not node:
            raise ValueError("Node not found.")

        telemetry = await telemetry_repository.create(
            db=db,
            **data.model_dump(),
        )

        # Update latest node metrics
        await node_repository.update_metrics(
            db=db,
            node=node,
            cpu_usage=data.cpu_usage,
            gpu_usage=data.gpu_usage,
            memory_usage=data.ram_usage,
            temperature=max(
                data.cpu_temperature,
                data.gpu_temperature,
            ),
            power_consumption=data.gpu_power,
        )

        return telemetry

    # =====================================================
    # Get Telemetry
    # =====================================================

    async def get_telemetry(
        self,
        db: AsyncSession,
        telemetry_id: int,
    ) -> Telemetry:

        telemetry = await telemetry_repository.get(
            db,
            telemetry_id,
        )

        if not telemetry:
            raise ValueError("Telemetry not found.")

        return telemetry

    # =====================================================
    # Latest Telemetry
    # =====================================================

    async def get_latest(
        self,
        db: AsyncSession,
        node_id: int,
    ) -> Telemetry:

        telemetry = await telemetry_repository.get_latest(
            db,
            node_id,
        )

        if not telemetry:
            raise ValueError("No telemetry found.")

        return telemetry

    # =====================================================
    # History
    # =====================================================

    async def get_history(
        self,
        db: AsyncSession,
        node_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Telemetry]:

        return await telemetry_repository.get_history(
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

        return await telemetry_repository.get_cluster_telemetry(
            db=db,
            cluster_id=cluster_id,
        )


telemetry_service = TelemetryService()