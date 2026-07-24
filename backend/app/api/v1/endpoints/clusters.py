"""
Cluster Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_active_user,
    get_database,
)

from app.controllers.cluster_controller import cluster_controller

from app.models.user import User

from app.schemas.cluster import (
    ClusterCreate,
    ClusterResponse,
    ClusterUpdate,
)

router = APIRouter(
    prefix="/clusters",
    tags=["Clusters"],
)


# =====================================================
# Create Cluster
# =====================================================

@router.post(
    "/",
    response_model=ClusterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cluster(
    data: ClusterCreate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await cluster_controller.create_cluster(
            db=db,
            current_user=current_user,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# Get My Clusters
# =====================================================

@router.get(
    "/me",
    response_model=list[ClusterResponse],
)
async def get_my_clusters(
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    return await cluster_controller.get_user_clusters(
        db=db,
        current_user=current_user,
    )


# =====================================================
# Get All Clusters
# =====================================================

@router.get(
    "/",
    response_model=list[ClusterResponse],
)
async def get_clusters(
    db: AsyncSession = Depends(get_database),
):
    return await cluster_controller.get_clusters(
        db=db,
    )


# =====================================================
# Get Cluster By ID
# =====================================================

@router.get(
    "/{cluster_id}",
    response_model=ClusterResponse,
)
async def get_cluster(
    cluster_id: int,
    db: AsyncSession = Depends(get_database),
):
    try:
        return await cluster_controller.get_cluster(
            db=db,
            cluster_id=cluster_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Update Cluster
# =====================================================

@router.put(
    "/{cluster_id}",
    response_model=ClusterResponse,
)
async def update_cluster(
    cluster_id: int,
    data: ClusterUpdate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await cluster_controller.update_cluster(
            db=db,
            cluster_id=cluster_id,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Delete Cluster
# =====================================================

@router.delete(
    "/{cluster_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cluster(
    cluster_id: int,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
):
    try:
        await cluster_controller.delete_cluster(
            db=db,
            cluster_id=cluster_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Healthy Clusters
# =====================================================

@router.get(
    "/healthy/list",
    response_model=list[ClusterResponse],
)
async def healthy_clusters(
    db: AsyncSession = Depends(get_database),
):
    return await cluster_controller.healthy_clusters(db)


# =====================================================
# Critical Clusters
# =====================================================

@router.get(
    "/critical/list",
    response_model=list[ClusterResponse],
)
async def critical_clusters(
    db: AsyncSession = Depends(get_database),
):
    return await cluster_controller.critical_clusters(db)