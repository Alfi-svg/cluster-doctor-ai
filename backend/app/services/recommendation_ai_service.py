"""
AI Recommendation Service
"""

from __future__ import annotations

import logging

from app.llm.client import llm_client
from app.llm.context_builder import context_builder
from app.llm.parser import parser
from app.llm.prompts import (
    SYSTEM_PROMPT,
    build_recommendation_prompt,
)
from app.llm.schemas import LLMExplanation

logger = logging.getLogger(__name__)


class RecommendationAIService:
    """
    Generates AI recommendations based on
    telemetry and prediction results.
    """

    async def generate_recommendation(
        self,
        *,
        cluster: dict | None = None,
        node: dict | None = None,
        telemetry: dict | None = None,
        prediction: dict | None = None,
    ) -> LLMExplanation:

        logger.info("Generating AI recommendation...")

        context = context_builder.prediction_context(
            cluster=cluster,
            node=node,
            telemetry=telemetry,
            prediction=prediction,
        )

        prompt = build_recommendation_prompt(
            prediction=prediction or {},
            telemetry=context,
        )

        raw_response = await llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            prompt=prompt,
            temperature=0.2,
            max_tokens=1000,
        )

        recommendation = parser.explanation(raw_response)

        logger.info("AI recommendation generated.")

        return recommendation


recommendation_ai_service = RecommendationAIService()