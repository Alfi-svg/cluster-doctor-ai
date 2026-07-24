"""
Reality Service

Digital Twin Reality Verification Service
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.digital_twin.reality_checker import reality_checker


class RealityService:
    """
    Reality Verification Service
    """

    async def compare(
        self,
        db: AsyncSession,
        node_id: str,
        telemetry: dict,
    ):
        """
        Compare real telemetry with
        Digital Twin snapshot.
        """

        return reality_checker.compare(
            node_id=node_id,
            telemetry=telemetry,
        )

    async def summary(
        self,
        db: AsyncSession,
    ):
        """
        Reality Summary
        """

        return {
            "healthy_nodes": 0,
            "warning_nodes": 0,
            "critical_nodes": 0,
        }


reality_service = RealityService()