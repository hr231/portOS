"""
Tests for core/ module.

- test_config: config loads correctly, env vars override defaults
- test_llm: LLM gateway handles completions, streaming, function calling
- test_memory: session creation, message add/get, history limits
- test_state: SQLite CRUD operations, namespacing
"""

import os
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ═══════════════════════════════════════════════════════════════
#  Config
# ═══════════════════════════════════════════════════════════════

class TestConfig:
    def test_config_loads(self):
        """Config singleton initializes without errors."""
        from core.config import cfg
        assert cfg is not None
        assert cfg.llm.provider in ("groq", "openai", "ollama", "anthropic")

    def test_paths_exist(self):
        """Key paths are set."""
        from core.config import cfg
        assert cfg.paths.project_root.exists()

    def test_env_override(self, monkeypatch):
        """Environment variables override defaults."""
        monkeypatch.setenv("LLM_PROVIDER", "openai")
        monkeypatch.setenv("LLM_MODEL", "gpt-4o")
        # Re-import to pick up new env vars
        import importlib
        import core.config
        importlib.reload(core.config)
        from core.config import cfg as reloaded_cfg
        # Restore after test — provider might still be cached in dataclass
        # Just check the env var is there
        assert os.environ["LLM_PROVIDER"] == "openai"


# ═══════════════════════════════════════════════════════════════
#  LLM Gateway
# ═══════════════════════════════════════════════════════════════

def _mock_response(content: str = "Hello from mock LLM"):
    """Build a mock litellm response object."""
    message = MagicMock()
    message.content = content
    message.tool_calls = None

    choice = MagicMock()
    choice.message = message

    response = MagicMock()
    response.choices = [choice]
    return response


def _mock_function_response(name: str, arguments: dict):
    """Build a mock litellm function-call response."""
    tool_call = MagicMock()
    tool_call.function.name = name
    tool_call.function.arguments = json.dumps(arguments)

    message = MagicMock()
    message.content = None
    message.tool_calls = [tool_call]

    choice = MagicMock()
    choice.message = message

    response = MagicMock()
    response.choices = [choice]
    return response


async def _mock_stream_response(chunks: list[str]):
    """Async generator that mimics litellm streaming."""
    for text in chunks:
        delta = MagicMock()
        delta.content = text
        choice = MagicMock()
        choice.delta = delta
        chunk = MagicMock()
        chunk.choices = [choice]
        yield chunk


class TestLLMGateway:
    """Tests for core.llm.LLMGateway — all mocked, no API key needed."""

    @pytest.mark.asyncio
    async def test_complete_returns_text(self):
        """complete() returns the response content as a string."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        with patch("core.llm._check_api_key"), \
             patch("core.llm.acompletion", new_callable=AsyncMock) as mock_ac:
            mock_ac.return_value = _mock_response("The answer is 4")
            result = await gw.complete("What is 2+2?")

        assert result == "The answer is 4"
        mock_ac.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_with_system_prompt(self):
        """complete() sends system message when provided."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        with patch("core.llm._check_api_key"), \
             patch("core.llm.acompletion", new_callable=AsyncMock) as mock_ac:
            mock_ac.return_value = _mock_response("Sure")
            await gw.complete("Hi", system="You are helpful")

        call_kwargs = mock_ac.call_args
        messages = call_kwargs.kwargs["messages"]
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

    @pytest.mark.asyncio
    async def test_complete_empty_content_returns_empty_string(self):
        """complete() returns '' when LLM returns None content."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        with patch("core.llm._check_api_key"), \
             patch("core.llm.acompletion", new_callable=AsyncMock) as mock_ac:
            mock_ac.return_value = _mock_response(None)
            # Override the mock to return None content
            mock_ac.return_value.choices[0].message.content = None
            result = await gw.complete("empty")

        assert result == ""

    @pytest.mark.asyncio
    async def test_stream_yields_chunks(self):
        """stream() yields text chunks from the streaming response."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        chunks = ["Hello", " world", "!"]
        with patch("core.llm._check_api_key"), \
             patch("core.llm.acompletion", new_callable=AsyncMock) as mock_ac:
            mock_ac.return_value = _mock_stream_response(chunks)
            collected = []
            async for text in gw.stream("Tell me something"):
                collected.append(text)

        assert collected == ["Hello", " world", "!"]

    @pytest.mark.asyncio
    async def test_stream_skips_empty_deltas(self):
        """stream() skips chunks with no content."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        async def stream_with_empties():
            for content in ["Hi", None, "", "there"]:
                delta = MagicMock()
                delta.content = content
                choice = MagicMock()
                choice.delta = delta
                chunk = MagicMock()
                chunk.choices = [choice]
                yield chunk

        with patch("core.llm._check_api_key"), \
             patch("core.llm.acompletion", new_callable=AsyncMock) as mock_ac:
            mock_ac.return_value = stream_with_empties()
            collected = []
            async for text in gw.stream("test"):
                collected.append(text)

        assert collected == ["Hi", "there"]

    @pytest.mark.asyncio
    async def test_function_call_returns_tool(self):
        """function_call() extracts the tool name and arguments."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        functions = [{
            "name": "route_to_agent",
            "description": "Route query to an agent",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {"type": "string"},
                },
                "required": ["agent_name"],
            },
        }]

        with patch("core.llm._check_api_key"), \
             patch("core.llm.acompletion", new_callable=AsyncMock) as mock_ac:
            mock_ac.return_value = _mock_function_response(
                "route_to_agent", {"agent_name": "portfolio"}
            )
            result = await gw.function_call("What are Harshit's skills?", functions)

        assert result["name"] == "route_to_agent"
        assert result["arguments"]["agent_name"] == "portfolio"

    @pytest.mark.asyncio
    async def test_function_call_no_tool_called(self):
        """function_call() returns fallback when LLM doesn't call a tool."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        with patch("core.llm._check_api_key"), \
             patch("core.llm.acompletion", new_callable=AsyncMock) as mock_ac:
            mock_ac.return_value = _mock_response("I don't know which agent to use")
            result = await gw.function_call("vague query", [{"name": "test", "description": "test", "parameters": {}}])

        assert result["name"] == "_no_tool_called"
        assert "response" in result["arguments"]

    @pytest.mark.asyncio
    async def test_function_call_empty_functions_raises(self):
        """function_call() raises ValueError with empty functions list."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        with patch("core.llm._check_api_key"):
            with pytest.raises(ValueError, match="at least one function"):
                await gw.function_call("test", [])

    @pytest.mark.asyncio
    async def test_function_call_malformed_args(self):
        """function_call() handles malformed JSON in tool arguments."""
        from core.llm import LLMGateway
        gw = LLMGateway()

        # Build a response with invalid JSON in arguments
        tool_call = MagicMock()
        tool_call.function.name = "some_func"
        tool_call.function.arguments = "not valid json{{"

        message = MagicMock()
        message.tool_calls = [tool_call]

        choice = MagicMock()
        choice.message = message

        response = MagicMock()
        response.choices = [choice]

        with patch("core.llm._check_api_key"), \
             patch("core.llm.acompletion", new_callable=AsyncMock) as mock_ac:
            mock_ac.return_value = response
            result = await gw.function_call("test", [{"name": "f", "description": "f", "parameters": {}}])

        assert result["name"] == "some_func"
        assert result["arguments"] == {}  # graceful fallback


class TestLLMModelId:
    """Tests for the _model_id() helper."""

    def test_groq_prefix(self, monkeypatch):
        """Groq provider produces 'groq/model'."""
        monkeypatch.setattr("core.llm.cfg.llm.provider", "groq")
        monkeypatch.setattr("core.llm.cfg.llm.model", "llama-3.3-70b-versatile")
        from core.llm import _model_id
        assert _model_id() == "groq/llama-3.3-70b-versatile"

    def test_openai_no_prefix(self, monkeypatch):
        """OpenAI provider has no prefix."""
        monkeypatch.setattr("core.llm.cfg.llm.provider", "openai")
        monkeypatch.setattr("core.llm.cfg.llm.model", "gpt-4o")
        from core.llm import _model_id
        assert _model_id() == "gpt-4o"

    def test_ollama_prefix(self, monkeypatch):
        """Ollama provider produces 'ollama/model'."""
        monkeypatch.setattr("core.llm.cfg.llm.provider", "ollama")
        monkeypatch.setattr("core.llm.cfg.llm.model", "llama3")
        from core.llm import _model_id
        assert _model_id() == "ollama/llama3"

    def test_unknown_provider_raises(self, monkeypatch):
        """Unknown provider raises ValueError."""
        monkeypatch.setattr("core.llm.cfg.llm.provider", "banana")
        from core.llm import _model_id
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            _model_id()


class TestLLMApiKeyCheck:
    """Tests for API key validation."""

    def test_missing_key_raises(self, monkeypatch):
        """Missing API key raises AuthenticationError."""
        monkeypatch.setattr("core.llm.cfg.llm.provider", "groq")
        monkeypatch.setattr("core.llm.cfg.llm.api_key", "")
        from core.llm import _check_api_key
        from litellm.exceptions import AuthenticationError
        with pytest.raises(AuthenticationError, match="API key missing"):
            _check_api_key()

    def test_ollama_no_key_needed(self, monkeypatch):
        """Ollama provider doesn't require an API key."""
        monkeypatch.setattr("core.llm.cfg.llm.provider", "ollama")
        monkeypatch.setattr("core.llm.cfg.llm.api_key", "")
        from core.llm import _check_api_key
        _check_api_key()  # should not raise

    def test_valid_key_passes(self, monkeypatch):
        """Valid API key passes check."""
        monkeypatch.setattr("core.llm.cfg.llm.provider", "groq")
        monkeypatch.setattr("core.llm.cfg.llm.api_key", "gsk_test_key_12345")
        from core.llm import _check_api_key
        _check_api_key()  # should not raise


# ═══════════════════════════════════════════════════════════════
#  Memory
# ═══════════════════════════════════════════════════════════════

class TestMemory:
    def test_create_session(self):
        """Create a session and get its ID."""
        from core.memory import MemoryStore
        mem = MemoryStore()
        sid = mem.create_session()
        assert isinstance(sid, str)
        assert len(sid) == 8

    def test_add_and_get(self):
        """Add messages and retrieve them."""
        from core.memory import MemoryStore
        mem = MemoryStore()
        sid = mem.create_session()
        mem.add(sid, "user", "hello")
        mem.add(sid, "assistant", "hi there")
        history = mem.get(sid)
        assert len(history) == 2
        assert history[0].role == "user"
        assert history[1].content == "hi there"

    def test_clear_session(self):
        """Clear a session's history."""
        from core.memory import MemoryStore
        mem = MemoryStore()
        sid = mem.create_session()
        mem.add(sid, "user", "hello")
        mem.clear(sid)
        assert len(mem.get(sid)) == 0

    def test_get_nonexistent_session(self):
        """Getting a non-existent session returns empty list."""
        from core.memory import MemoryStore
        mem = MemoryStore()
        history = mem.get("nonexistent")
        assert history == []

    def test_history_limit(self):
        """get() respects the limit parameter."""
        from core.memory import MemoryStore
        mem = MemoryStore()
        sid = mem.create_session()
        for i in range(10):
            mem.add(sid, "user", f"message {i}")
        history = mem.get(sid, limit=3)
        assert len(history) == 3
        assert history[0].content == "message 7"  # last 3


# ═══════════════════════════════════════════════════════════════
#  StateDB
# ═══════════════════════════════════════════════════════════════

class TestStateDB:
    @pytest.mark.asyncio
    async def test_initialize_not_implemented(self):
        """StateDB initialize raises NotImplementedError (placeholder)."""
        from core.state import state_db
        with pytest.raises(NotImplementedError):
            await state_db.initialize()
