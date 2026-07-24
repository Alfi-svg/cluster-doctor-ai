"""
Digital Twin Controller
"""

from app.services.twin_service import twin_service


class TwinController:

    async def clusters(self):

        return await twin_service.get_clusters()

    async def cluster(
        self,
        cluster_id: str,
    ):

        return await twin_service.get_cluster(
            cluster_id
        )

    async def rooms(self):

        return await twin_service.get_rooms()

    async def room(
        self,
        room_id: str,
    ):

        return await twin_service.get_room(
            room_id
        )

    async def snapshot(
        self,
        node_id: str,
    ):

        return await twin_service.get_snapshot(
            node_id
        )
    async def node(
      self,
      node_id: str,
):

     return await twin_service.get_node(
        node_id
    )


twin_controller = TwinController()