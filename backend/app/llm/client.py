"""
LLM Client

Responsible for communicating with OpenAI/OpenRouter.
"""

from __future__ import annotations

import logging
from typing import Optional

from openai import AsyncOpenAI

from app.core.config import settings
from app.llm.exceptions import (
    LLMConnectionError,
    LLMResponseError,
)

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Singleton async LLM client.
    """

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=getattr(
                settings,
                "OPENAI_BASE_URL",
                "https://api.openai.com/v1",
            ),
        )

        self.default_model = settings.OPENAI_MODEL

    async def generate(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 600,
    ) -> str:
        """
        Generate LLM response.
        """

        try:

            messages = []

            if system_prompt:
                messages.append(
                    {
                        "role": "system",
                        "content": system_prompt,
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            response = await self.client.chat.completions.create(
                model=self.default_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            if not response.choices:
                raise LLMResponseError(
                    "LLM returned empty response."
                )

            answer = response.choices[0].message.content

            if answer is None:
                raise LLMResponseError(
                    "LLM response content is empty."
                )

            return answer.strip()

        except Exception as e:

            logger.exception("LLM Request Failed")

            raise LLMConnectionError(
                str(e)
            ) from e


llm_client = LLMClient()
print("API KEY:", settings.OPENAI_API_KEY[:20] + "...")
print("BASE URL:", settings.OPENAI_BASE_URL)
print("MODEL:", settings.OPENAI_MODEL)