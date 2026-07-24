"""
Dashboard Service

Provides live dashboard data from repositories.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.cluster_repository import cluster_repository
from app.repositories.node_repository import node_repository
from app.repositories.prediction_repository import prediction_repository
from app.repositories.notification_repository import (
    notification_repository,
)


class DashboardService:
    """
    Dashboard Business Logic
    """

    async def overview(
        self,
        db: AsyncSession,
    ):
        """
        Dashboard Overview
        """

        total_clusters = await cluster_repository.count(db)

        total_nodes = await node_repository.count(db)

        healthy_clusters = len(
            await cluster_repository.get_healthy_clusters(db)
        )

        critical_clusters = len(
            await cluster_repository.get_critical_clusters(db)
        )

        online_nodes = len(
            await node_repository.get_online_nodes(db)
        )

        offline_nodes = len(
            await node_repository.get_offline_nodes(db)
        )

        pending_predictions = len(
            await prediction_repository.get_pending(db)
        )

        critical_notifications = len(
            await notification_repository.get_critical(db)
        )

        warning_clusters = (
            total_clusters
            - healthy_clusters
            - critical_clusters
        )

        return {

            "clusters": total_clusters,

            "nodes": total_nodes,

            "healthy_clusters": healthy_clusters,

            "warning_clusters": max(
                warning_clusters,
                0,
            ),

            "critical_clusters": critical_clusters,

            "online_nodes": online_nodes,

            "offline_nodes": offline_nodes,

            "pending_predictions": pending_predictions,

            "critical_notifications": critical_notifications,

            "system_health": round(

                (
                    healthy_clusters
                    / max(total_clusters, 1)
                )
                * 100,

                2,

            ),

        }


dashboard_service = DashboardService()