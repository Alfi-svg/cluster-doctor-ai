"""
LLM Utility Functions
"""

from __future__ import annotations

import json
import re
from typing import Any


def remove_markdown(text: str) -> str:
    """
    Remove markdown code fences from LLM response.
    """

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def extract_json(text: str) -> dict[str, Any]:
    """
    Extract JSON object from LLM response.
    """

    text = remove_markdown(text)

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found.")

    return json.loads(match.group())


def safe_float(value: Any) -> float | None:
    """
    Safely convert to float.
    """

    try:
        return float(value)

    except Exception:
        return None


def safe_int(value: Any) -> int | None:
    """
    Safely convert to int.
    """

    try:
        return int(value)

    except Exception:
        return None


def normalize_priority(priority: str | None) -> str:
    """
    Normalize recommendation priority.
    """

    if not priority:
        return "MEDIUM"

    priority = priority.upper()

    allowed = {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }

    if priority not in allowed:
        return "MEDIUM"

    return priority


def clean_response(text: str) -> str:
    """
    Clean whitespace.
    """

    return "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )