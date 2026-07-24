"""
Digital Twin Room Service

Manages room → rack → node hierarchy for the Digital Twin.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from app.digital_twin.twin_manager import twin_manager


# ==========================================================
# Rack
# ==========================================================

@dataclass
class Rack:

    rack_id: str

    name: str

    x: float

    y: float

    z: float

    nodes: list[str] = field(default_factory=list)


# ==========================================================
# Room
# ==========================================================

@dataclass
class Room:

    room_id: str

    name: str

    racks: dict[str, Rack] = field(default_factory=dict)


# ==========================================================
# Room Service
# ==========================================================

class RoomService:

    def __init__(self):

        self.rooms: dict[str, Room] = {}

    # ------------------------------------------------------

    def create_room(
        self,
        room_id: str,
        name: str,
    ):

        if room_id not in self.rooms:

            self.rooms[room_id] = Room(
                room_id=room_id,
                name=name,
            )

    # ------------------------------------------------------

    def create_rack(
        self,
        room_id: str,
        rack_id: str,
        name: str,
        x: float,
        y: float,
        z: float,
    ):

        if room_id not in self.rooms:

            raise ValueError(f"Room '{room_id}' not found.")

        room = self.rooms[room_id]

        room.racks[rack_id] = Rack(
            rack_id=rack_id,
            name=name,
            x=x,
            y=y,
            z=z,
        )

    # ------------------------------------------------------

    def assign_node(
        self,
        room_id: str,
        rack_id: str,
        node_id: str,
    ):

        rack = self.rooms[room_id].racks[rack_id]

        if node_id not in rack.nodes:

            rack.nodes.append(node_id)

    # ------------------------------------------------------

    async def get_room_snapshot(
        self,
        room_id: str,
    ) -> dict[str, Any]:

        room = self.rooms.get(room_id)

        if room is None:
            return {}

        result = {
            "room_id": room.room_id,
            "name": room.name,
            "racks": [],
        }

        for rack in room.racks.values():

            rack_data = asdict(rack)

            rack_nodes = []

            for node_id in rack.nodes:

                cluster_id = node_id.split("-")[0]

                cluster = await twin_manager.get_cluster(cluster_id)

                for node in cluster.get("nodes", []):

                    if node["node_id"] == node_id:
                        rack_nodes.append(node)

            rack_data["nodes"] = rack_nodes

            result["racks"].append(rack_data)

        return result

    # ------------------------------------------------------

    async def get_all_rooms(self):

        rooms = []

        for room_id in self.rooms:

            rooms.append(
                await self.get_room_snapshot(room_id)
            )

        return rooms


room_service = RoomService()