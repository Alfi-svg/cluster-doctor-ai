"""
IoT Test API
"""

from fastapi import APIRouter

from app.iot.controller import iot_controller
from app.iot.schemas import IoTPayload

router = APIRouter(
    prefix="/iot",
    tags=["IoT"],
)


# =====================================================
# SAFE
# =====================================================

@router.post("/test-safe")
async def test_safe():

    data = await iot_controller.safe()

    return {
        "success": True,
        "data": data,
    }


# =====================================================
# ALERT
# =====================================================

@router.post("/test-alert")
async def test_alert():

    data = await iot_controller.alert(

        risk="HIGH",

        score=98,

        message="GPU Failure",

        cluster="cluster-01",

        node="node-01",

    )

    return {
        "success": True,
        "data": data,
    }


# =====================================================
# CUSTOM
# =====================================================

@router.post("/test-custom")
async def test_custom(
    payload: IoTPayload,
):

    data = await iot_controller.custom(
        payload
    )

    return {
        "success": True,
        "data": data,
    }