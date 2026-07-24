"""
LLM Response Schemas
"""

from __future__ import annotations

from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


# ==========================================================
# Recommendation Item
# ==========================================================


class RecommendationItem(BaseModel):
    """
    Single recommendation.
    """

    title: str
    description: str
    priority: str = "MEDIUM"


# ==========================================================
# LLM Explanation
# ==========================================================


class LLMExplanation(BaseModel):
    """
    Structured explanation returned by LLM.
    """

    summary: str

    root_cause: Optional[str] = None

    risk_level: Optional[str] = None

    confidence: Optional[float] = None

    recommendations: List[RecommendationItem] = Field(
        default_factory=list
    )


# ==========================================================
# Dashboard Summary
# ==========================================================


class DashboardSummary(BaseModel):
    """
    Dashboard AI Summary
    """

    overall_health: str

    summary: str

    critical_nodes: List[str] = Field(
        default_factory=list
    )

    warnings: List[str] = Field(
        default_factory=list
    )

    recommendations: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# Chat Response
# ==========================================================


class ChatResponse(BaseModel):
    """
    AI Chat response.
    """

    answer: str

    confidence: Optional[float] = None

    sources: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# Alert Explanation
# ==========================================================


class AlertExplanation(BaseModel):
    """
    AI Alert Explanation
    """

    severity: str

    explanation: str

    recommendation: str


# ==========================================================
# Recovery Plan
# ==========================================================


class RecoveryPlan(BaseModel):
    """
    AI Generated Recovery Plan
    """

    summary: str

    estimated_downtime: Optional[str] = None

    confidence: Optional[float] = None

    steps: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# AI Report
# ==========================================================


class AIReport(BaseModel):
    """
    AI Generated Report
    """

    executive_summary: str

    findings: List[str] = Field(
        default_factory=list
    )

    recommendations: List[str] = Field(
        default_factory=list
    )

    conclusion: str