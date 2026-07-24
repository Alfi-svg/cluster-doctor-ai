"""
AI Explanation Service
"""

from __future__ import annotations

import logging

from app.llm.client import llm_client
from app.llm.context_builder import context_builder
from app.llm.parser import parser
from app.llm.prompts import (
    SYSTEM_PROMPT,
    build_prediction_prompt,
)
from app.llm.schemas import LLMExplanation

logger = logging.getLogger(__name__)


class ExplanationService:
    """
    AI service for generating prediction explanations.
    """

    async def explain_prediction(
        self,
        *,
        cluster: dict | None = None,
        node: dict | None = None,
        telemetry: dict | None = None,
        prediction: dict | None = None,
    ) -> LLMExplanation:
        """
        Generate AI explanation from prediction data.
        """

        logger.info("Generating AI explanation...")

        telemetry_context = context_builder.prediction_context(
            cluster=cluster,
            node=node,
            telemetry=telemetry,
            prediction=prediction,
        )

        prompt = build_prediction_prompt(
            prediction=prediction or {},
            telemetry=telemetry_context,
        )

        raw_response = await llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            prompt=prompt,
            temperature=0.2,
            max_tokens=1000,
        )

        explanation = parser.explanation(raw_response)

        logger.info("AI explanation generated successfully.")

        return explanation


explanation_service = ExplanationService()