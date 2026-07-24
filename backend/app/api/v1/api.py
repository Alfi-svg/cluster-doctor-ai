"""
Main API Router (Version 1)
"""

from fastapi import APIRouter

from app.api.v1.endpoints.ai_test import router as ai_test_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.chatbot import router as chatbot_router
from app.api.v1.endpoints.clusters import router as clusters_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.nodes import router as nodes_router
from app.api.v1.endpoints.notifications import router as notifications_router
from app.api.v1.endpoints.predictions import router as predictions_router
from app.api.v1.endpoints.telemetry import router as telemetry_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.migration import router as migration_router   # NEW
from app.api.v1.endpoints import simulator
from app.api.v1.endpoints.recovery import router as recovery_router
from app.api.v1.endpoints.reality import router as reality_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.twin import router as twin_router
from app.api.v1.endpoints.iot import router as iot_router

# =====================================================
# Main API Router
# =====================================================

api_router = APIRouter()

# =====================================================
# Register Routers
# =====================================================

api_router.include_router(auth_router)

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)
api_router.include_router(
    recovery_router,
)
api_router.include_router(
    reality_router,
)
api_router.include_router(
    dashboard_router,
)
api_router.include_router(
    twin_router,
)
api_router.include_router(clusters_router)

api_router.include_router(nodes_router)

api_router.include_router(telemetry_router)

api_router.include_router(predictions_router)

api_router.include_router(notifications_router)

api_router.include_router(health_router)

api_router.include_router(ai_test_router)

api_router.include_router(chatbot_router)
api_router.include_router(
    iot_router,
)

# =====================================================
# Migration API (NEW)
# =====================================================

api_router.include_router(migration_router)

# =====================================================
# Simulator
# =====================================================

api_router.include_router(
    simulator.router,
    prefix="/simulator",
    tags=["Simulator"],
)