"""
Dashboard AI Service
"""

from __future__ import annotations

import logging

from app.llm.client import llm_client
from app.llm.context_builder import context_builder
from app.llm.parser import parser
from app.llm.prompts import (
    SYSTEM_PROMPT,
    build_dashboard_prompt,
)
from app.llm.schemas import DashboardSummary

logger = logging.getLogger(__name__)


class DashboardAIService:
    """
    Generates AI-powered dashboard summaries.
    """

    async def generate_dashboard_summary(
        self,
        *,
        cluster: dict,
        nodes: list[dict],
        telemetry: list[dict],
        predictions: list[dict],
    ) -> DashboardSummary:
        """
        Generate dashboard summary using LLM.
        """

        logger.info("Generating dashboard AI summary...")

        context = context_builder.dashboard_context(
            cluster=cluster,
            nodes=nodes,
            predictions=predictions,
        )

        prompt = build_dashboard_prompt(
            cluster=cluster,
            nodes=nodes,
            telemetry=telemetry,
            predictions=predictions,
        )

        raw_response = await llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            prompt=prompt,
            temperature=0.2,
            max_tokens=1200,
        )

        summary = parser.dashboard(raw_response)

        logger.info("Dashboard summary generated successfully.")

        return summary


dashboard_ai_service = DashboardAIService()