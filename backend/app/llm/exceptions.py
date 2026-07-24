"""
Custom Exceptions for LLM Module
"""


class LLMError(Exception):
    """
    Base exception for all LLM related errors.
    """

    pass


class LLMConnectionError(LLMError):
    """
    Raised when OpenAI/OpenRouter cannot be reached.
    """

    pass


class LLMResponseError(LLMError):
    """
    Raised when LLM returns invalid response.
    """

    pass


class PromptBuildError(LLMError):
    """
    Raised when prompt construction fails.
    """

    pass


class ContextBuildError(LLMError):
    """
    Raised when context creation fails.
    """

    pass