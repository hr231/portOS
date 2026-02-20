"""
LLM Gateway — provider-agnostic interface via litellm.

Supports: Groq, OpenAI, Ollama, Anthropic, Azure, etc.
Swap providers by changing LLM_PROVIDER + LLM_MODEL in .env.local.

Usage:
    from core.llm import llm
    response = await llm.complete("What is 2+2?")
    async for chunk in llm.stream("Tell me about RAG"):
        print(chunk, end="")
    result = await llm.function_call("route this", functions=[...])
"""

import json
import logging
from typing import AsyncIterator

import litellm
from litellm import acompletion
from litellm.exceptions import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    RateLimitError,
    Timeout,
)

from core.config import cfg

logger = logging.getLogger(__name__)

# ── litellm configuration ────────────────────────────────────
litellm.drop_params = True        # silently ignore unsupported params per provider
litellm.set_verbose = False       # flip to True for debugging


def _model_id() -> str:
    """Build the litellm model string: 'provider/model'."""
    provider = cfg.llm.provider.lower()
    model = cfg.llm.model

    # litellm prefixes for common providers
    prefix_map = {
        "groq": "groq/",
        "openai": "",            # openai is the default, no prefix
        "ollama": "ollama/",
        "anthropic": "anthropic/",
        "azure": "azure/",
    }
    prefix = prefix_map.get(provider)
    if prefix is None:
        raise ValueError(
            f"Unknown LLM provider '{provider}'. "
            f"Supported: {list(prefix_map.keys())}"
        )
    return f"{prefix}{model}"


def _check_api_key() -> None:
    """Raise early if the API key is missing (skip for local providers)."""
    provider = cfg.llm.provider.lower()
    if provider in ("ollama",):
        return  # local providers don't need a key
    if not cfg.llm.api_key:
        raise AuthenticationError(
            message=f"API key missing for provider '{provider}'. Set GROQ_API_KEY (or the relevant key) in .env.local",
            llm_provider=provider,
            model=cfg.llm.model,
        )


class LLMGateway:
    """Provider-agnostic LLM interface powered by litellm."""

    # ── retry / timeout config ────────────────────────────────
    MAX_RETRIES = 3
    TIMEOUT_SECONDS = 30

    def __init__(self):
        self._config = cfg.llm

    # ── core methods ──────────────────────────────────────────

    async def complete(
        self,
        prompt: str,
        system: str = "",
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Single-shot completion. Returns full response text."""
        _check_api_key()

        messages = self._build_messages(prompt, system)
        response = await acompletion(
            model=_model_id(),
            messages=messages,
            temperature=temperature or self._config.temperature,
            max_tokens=max_tokens or self._config.max_tokens,
            api_key=self._config.api_key,
            num_retries=self.MAX_RETRIES,
            timeout=self.TIMEOUT_SECONDS,
        )
        content = response.choices[0].message.content
        return content or ""

    async def stream(
        self,
        prompt: str,
        system: str = "",
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """Streaming completion. Yields text chunks (needed for voice TTS)."""
        _check_api_key()

        messages = self._build_messages(prompt, system)
        response = await acompletion(
            model=_model_id(),
            messages=messages,
            temperature=temperature or self._config.temperature,
            max_tokens=max_tokens or self._config.max_tokens,
            api_key=self._config.api_key,
            stream=True,
            num_retries=self.MAX_RETRIES,
            timeout=self.TIMEOUT_SECONDS,
        )
        async for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content

    async def function_call(
        self,
        prompt: str,
        functions: list[dict],
        system: str = "",
    ) -> dict:
        """
        Function-calling for orchestrator routing.

        Returns:
            {"name": "function_name", "arguments": {"arg1": "val1", ...}}
        """
        _check_api_key()

        if not functions:
            raise ValueError("function_call() requires at least one function definition")

        messages = self._build_messages(prompt, system)

        # litellm uses OpenAI-compatible tools format
        tools = [
            {"type": "function", "function": fn}
            for fn in functions
        ]

        response = await acompletion(
            model=_model_id(),
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.1,  # low temperature for deterministic routing
            max_tokens=self._config.max_tokens,
            api_key=self._config.api_key,
            num_retries=self.MAX_RETRIES,
            timeout=self.TIMEOUT_SECONDS,
        )

        msg = response.choices[0].message

        # Extract tool call if present
        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            try:
                arguments = json.loads(tool_call.function.arguments)
            except (json.JSONDecodeError, TypeError):
                arguments = {}
            return {
                "name": tool_call.function.name,
                "arguments": arguments,
            }

        # Fallback: no tool was called — return content as fallback
        return {
            "name": "_no_tool_called",
            "arguments": {"response": msg.content or ""},
        }

    # ── helpers ───────────────────────────────────────────────

    @staticmethod
    def _build_messages(
        prompt: str,
        system: str = "",
    ) -> list[dict]:
        """Build the messages list for the LLM call."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return messages


# ── Singleton ─────────────────────────────────────────────────
llm = LLMGateway()
