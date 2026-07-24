"""
Digital Twin Service
"""

from app.digital_twin.room_service import room_service
from app.digital_twin.snapshot import snapshot_manager
from app.digital_twin.twin_manager import twin_manager


class TwinService:

    # =====================================================
    # All Clusters
    # =====================================================

    async def get_clusters(self):

        return await twin_manager.get_all_clusters()

    # =====================================================
    # Single Cluster
    # =====================================================

    async def get_cluster(
        self,
        cluster_id: str,
    ):

        return await twin_manager.get_cluster(
            cluster_id
        )

    # =====================================================
    # All Rooms
    # =====================================================

    async def get_rooms(self):

        return await room_service.get_all_rooms()

    # =====================================================
    # Room
    # =====================================================

    async def get_room(
        self,
        room_id: str,
    ):

        return await room_service.get_room_snapshot(
            room_id
        )

    # =====================================================
    # Snapshot
    # =====================================================

    async def get_snapshot(
        self,
        node_id: str,
    ):

        return snapshot_manager.to_dict(
            node_id
        )
    # =====================================================
# Node
# =====================================================

    async def get_node(
     self,
     node_id: str,
):

     return await twin_manager.get_node(
        node_id
    )


twin_service = TwinService()