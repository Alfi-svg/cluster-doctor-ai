from fastapi import APIRouter

from app.iot.simulator import telemetry_simulator

router = APIRouter()


@router.post("/publish")
async def publish():

    data = telemetry_simulator.publish()

    return {
        "message": "Telemetry Published",
        "payload": data,
    }