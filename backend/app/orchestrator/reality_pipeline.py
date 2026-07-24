"""
Reality Pipeline

Runs the Twin Reality Verification workflow.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.digital_twin.reality_checker import reality_checker


class RealityPipeline:

    async def run(
        self,
        db: AsyncSession,
        node_id: str,
        telemetry: dict,
    ) -> dict:

        result = reality_checker.compare(
            node_id=node_id,
            telemetry=telemetry,
        )

        return result


reality_pipeline = RealityPipeline()