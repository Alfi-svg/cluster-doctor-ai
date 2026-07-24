

from __future__ import annotations

from dataclasses import asdict, dataclass


# ==========================================================
# Rack Position
# ==========================================================

@dataclass
class NodePosition:

    rack: str

    row: int

    column: int

    x: float

    y: float

    z: float


# ==========================================================
# Node Mapper
# ==========================================================

class NodeMapper:

    def __init__(self):

        self._positions: dict[str, NodePosition] = {}

    # ------------------------------------------------------

    def register_node(
        self,
        node_id: str,
        rack: str,
        row: int,
        column: int,
        x: float,
        y: float,
        z: float,
    ):

        self._positions[node_id] = NodePosition(
            rack=rack,
            row=row,
            column=column,
            x=x,
            y=y,
            z=z,
        )

    # ------------------------------------------------------

    def get_position(
        self,
        node_id: str,
    ):

        position = self._positions.get(node_id)

        if not position:
            return None

        return asdict(position)

    # ------------------------------------------------------

    def update_position(
        self,
        node_id: str,
        **kwargs,
    ):

        position = self._positions.get(node_id)

        if not position:
            return

        for key, value in kwargs.items():

            if hasattr(position, key):
                setattr(position, key, value)

    # ------------------------------------------------------

    def remove_node(
        self,
        node_id: str,
    ):

        self._positions.pop(node_id, None)

    # ------------------------------------------------------

    def get_all(self):

        return {
            node_id: asdict(position)
            for node_id, position in self._positions.items()
        }


node_mapper = NodeMapper()