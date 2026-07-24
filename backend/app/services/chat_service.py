"""
AI Chat Service
"""

from __future__ import annotations

import logging

from app.llm.client import llm_client
from app.llm.context_builder import context_builder
from app.llm.parser import parser
from app.llm.prompts import (
    SYSTEM_PROMPT,
    build_chat_prompt,
)
from app.llm.schemas import ChatResponse

logger = logging.getLogger(__name__)


class ChatService:
    """
    Cluster Doctor AI Chat Service.
    """

    async def chat(
        self,
        *,
        question: str,
        history: list[dict] | None = None,
        cluster: dict | None = None,
        node: dict | None = None,
        telemetry: dict | None = None,
        prediction: dict | None = None,
    ) -> ChatResponse:

        context = context_builder.chat_context(
            cluster=cluster,
            node=node,
            telemetry=telemetry,
            prediction=prediction,
            history=history,
        )

        history_text = ""

        if history:
            history_text = "\n".join(
                f'{item.get("role","user")}: {item.get("content","")}'
                for item in history
            )

        prompt = build_chat_prompt(
            history=history_text,
            question=question,
            context=context,
        )

        raw_response = await llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            prompt=prompt,
            temperature=0.3,
            max_tokens=1200,
        )

        return parser.chat(raw_response)


chat_service = ChatService()