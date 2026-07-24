"""
LLM Response Parser
"""

from __future__ import annotations

import json
import logging

from app.llm.schemas import (
    AIReport,
    AlertExplanation,
    ChatResponse,
    DashboardSummary,
    LLMExplanation,
    RecoveryPlan,
)

logger = logging.getLogger(__name__)


class LLMParser:
    """
    Converts raw LLM responses into structured schemas.
    """

    @staticmethod
    def _parse_json(raw: str) -> dict:
        """
        Parse JSON response from LLM.
        """

        try:
            return json.loads(raw)

        except json.JSONDecodeError:

            logger.exception("Invalid JSON returned by LLM")

            raise ValueError(
                "LLM did not return valid JSON."
            )

    # =====================================================
    # Prediction Explanation
    # =====================================================

    def explanation(
        self,
        raw: str,
    ) -> LLMExplanation:

        data = self._parse_json(raw)

        return LLMExplanation.model_validate(data)

    # =====================================================
    # Dashboard
    # =====================================================

    def dashboard(
        self,
        raw: str,
    ) -> DashboardSummary:

        data = self._parse_json(raw)

        return DashboardSummary.model_validate(data)

    # =====================================================
    # Chat
    # =====================================================

    def chat(
        self,
        raw: str,
    ) -> ChatResponse:

        data = self._parse_json(raw)

        return ChatResponse.model_validate(data)

    # =====================================================
    # Alert
    # =====================================================

    def alert(
        self,
        raw: str,
    ) -> AlertExplanation:

        data = self._parse_json(raw)

        return AlertExplanation.model_validate(data)

    # =====================================================
    # Recovery
    # =====================================================

    def recovery(
        self,
        raw: str,
    ) -> RecoveryPlan:

        data = self._parse_json(raw)

        return RecoveryPlan.model_validate(data)

    # =====================================================
    # Report
    # =====================================================

    def report(
        self,
        raw: str,
    ) -> AIReport:

        data = self._parse_json(raw)

        return AIReport.model_validate(data)


parser = LLMParser()