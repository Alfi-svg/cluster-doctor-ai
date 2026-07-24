"""
Digital Twin API
"""

from fastapi import APIRouter

from app.controllers.twin_controller import twin_controller

router = APIRouter(
    prefix="/twin",
    tags=["Digital Twin"],
)

# =====================================================
# All Clusters
# =====================================================

@router.get("/clusters")
async def clusters():

    return {
        "success": True,
        "data": await twin_controller.clusters(),
    }


# =====================================================
# Single Cluster
# =====================================================

@router.get("/clusters/{cluster_id}")
async def cluster(
    cluster_id: str,
):

    return {
        "success": True,
        "data": await twin_controller.cluster(
            cluster_id
        ),
    }


# =====================================================
# All Rooms
# =====================================================

@router.get("/rooms")
async def rooms():

    return {
        "success": True,
        "data": await twin_controller.rooms(),
    }


# =====================================================
# Single Room
# =====================================================

@router.get("/rooms/{room_id}")
async def room(
    room_id: str,
):

    return {
        "success": True,
        "data": await twin_controller.room(
            room_id
        ),
    }
# =====================================================
# Node
# =====================================================

@router.get("/node/{node_id}")
async def node(
    node_id: str,
):

    return {
        "success": True,
        "data": await twin_controller.node(
            node_id
        ),
    }

# =====================================================
# Snapshot
# =====================================================

@router.get("/snapshot/{node_id}")
async def snapshot(
    node_id: str,
):

    return {
        "success": True,
        "data": await twin_controller.snapshot(
            node_id
        ),
    }