"""
AI Report Service

Generates AI-powered infrastructure reports.
"""

from __future__ import annotations

import logging

from app.llm.client import llm_client
from app.llm.context_builder import context_builder
from app.llm.parser import parser
from app.llm.prompts import (
    SYSTEM_PROMPT,
    build_report_prompt,
)
from app.llm.schemas import AIReport

logger = logging.getLogger(__name__)


class ReportService:
    """
    AI service responsible for generating
    infrastructure reports using LLM.
    """

    async def generate_report(
        self,
        *,
        cluster: dict,
        nodes: list[dict],
        telemetry: list[dict],
        predictions: list[dict],
    ) -> AIReport:
        """
        Generate an AI infrastructure report.
        """

        logger.info("Generating AI infrastructure report...")

        context = context_builder.report_context(
            cluster=cluster,
            nodes=nodes,
            telemetry=telemetry,
            predictions=predictions,
        )

        prompt = build_report_prompt(
            cluster=cluster,
            telemetry=telemetry,
            predictions=predictions,
        )

        raw_response = await llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            prompt=prompt,
            temperature=0.2,
            max_tokens=1500,
        )

        report = parser.report(raw_response)

        logger.info("AI report generated successfully.")

        return report


report_service = ReportService()