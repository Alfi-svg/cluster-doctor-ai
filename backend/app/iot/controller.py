"""
IoT Controller
"""

from app.iot.schemas import IoTPayload
from app.iot.service import iot_service


class IoTController:

    async def safe(self):

        return await iot_service.safe()

    async def alert(

        self,

        risk: str,

        score: float,

        message: str,

        cluster: str = "",

        node: str = "",

    ):

        return await iot_service.alert(

            risk=risk,

            score=score,

            message=message,

            cluster=cluster,

            node=node,

        )

    async def custom(
        self,
        payload: IoTPayload,
    ):

        return await iot_service.custom(
            payload
        )


iot_controller = IoTController()