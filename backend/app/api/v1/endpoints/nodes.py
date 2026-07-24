"""
Node Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_active_user,
    get_database,
)

from app.controllers.node_controller import node_controller

from app.database.enums import NodeStatus
from app.models.user import User

from app.schemas.node import (
    NodeCreate,
    NodeResponse,
    NodeUpdate,
)

router = APIRouter(
    prefix="/nodes",
    tags=["Nodes"],
)


# =====================================================
# Create Node
# =====================================================

@router.post(
    "/",
    response_model=NodeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_node(
    data: NodeCreate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await node_controller.create_node(
            db=db,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# Get All Nodes
# =====================================================

@router.get(
    "/",
    response_model=list[NodeResponse],
)
async def get_nodes(
    db: AsyncSession = Depends(get_database),
):
    return await node_controller.get_nodes(
        db=db,
    )


# =====================================================
# Get Node By ID
# =====================================================

@router.get(
    "/{node_id}",
    response_model=NodeResponse,
)
async def get_node(
    node_id: int,
    db: AsyncSession = Depends(get_database),
):
    try:
        return await node_controller.get_node(
            db=db,
            node_id=node_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Get Cluster Nodes
# =====================================================

@router.get(
    "/cluster/{cluster_id}",
    response_model=list[NodeResponse],
)
async def get_cluster_nodes(
    cluster_id: int,
    db: AsyncSession = Depends(get_database),
):
    return await node_controller.get_cluster_nodes(
        db=db,
        cluster_id=cluster_id,
    )


# =====================================================
# Update Node
# =====================================================

@router.put(
    "/{node_id}",
    response_model=NodeResponse,
)
async def update_node(
    node_id: int,
    data: NodeUpdate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await node_controller.update_node(
            db=db,
            node_id=node_id,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Delete Node
# =====================================================

@router.delete(
    "/{node_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_node(
    node_id: int,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        await node_controller.delete_node(
            db=db,
            node_id=node_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Online Nodes
# =====================================================

@router.get(
    "/online/list",
    response_model=list[NodeResponse],
)
async def online_nodes(
    db: AsyncSession = Depends(get_database),
):
    return await node_controller.online_nodes(
        db=db,
    )


# =====================================================
# Offline Nodes
# =====================================================

@router.get(
    "/offline/list",
    response_model=list[NodeResponse],
)
async def offline_nodes(
    db: AsyncSession = Depends(get_database),
):
    return await node_controller.offline_nodes(
        db=db,
    )


# =====================================================
# Update Node Status
# =====================================================

@router.patch(
    "/{node_id}/status",
    response_model=NodeResponse,
)
async def update_status(
    node_id: int,
    status_value: NodeStatus,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await node_controller.update_status(
            db=db,
            node_id=node_id,
            status=status_value,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )