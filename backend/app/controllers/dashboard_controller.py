"""
Dashboard Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.dashboard_service import dashboard_service


class DashboardController:

    async def overview(
        self,
        db: AsyncSession,
    ):
        """
        Dashboard Overview
        """

        return await dashboard_service.overview(
            db=db,
        )


dashboard_controller = DashboardController()