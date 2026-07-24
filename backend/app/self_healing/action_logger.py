"""
Action Logger
"""

from __future__ import annotations

from app.services.explanation_service import (
    explanation_service,
)


class ActionLogger:

    async def build_log(
        self,
        action: str,
        data: dict,
    ) -> dict:

        explanation = await explanation_service.generate_action_log(
            action=action,
            data=data,
        )

        return {

            "action": action,

            "data": data,

            "reason": explanation,
        }


action_logger = ActionLogger()