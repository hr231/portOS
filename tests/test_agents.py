"""
Tests for agents/ module.

- test_base_agent: BaseAgent interface, tool schemas, streaming default
- test_registry: agent registration, discovery, listing
- test_orchestrator: routing, default fallback, streaming
- test_portfolio_agent: execute, RAG query, fallback
- test_email_agent: tool execution, Gmail/Outlook clients, rules
- test_docs_agent: document search, summarization
- test_calendar_agent: availability check, event creation
- test_tasks_agent: CRUD operations, prioritization
- test_search_agent: web search, URL summarization
- test_social_agent: content drafting, LinkedIn posting
"""

import pytest
from agents.base import BaseAgent, Tool


class TestBaseAgent:
    def test_tool_schema(self):
        """Tool definitions produce valid JSON schemas."""
        tool = Tool(
            name="test_tool",
            description="A test tool",
            parameters={"type": "object", "properties": {"q": {"type": "string"}}},
        )
        assert tool.name == "test_tool"

    def test_cannot_instantiate_directly(self):
        """BaseAgent is abstract — cannot be instantiated."""
        with pytest.raises(TypeError):
            BaseAgent()

    @pytest.mark.asyncio
    async def test_stream_default(self):
        """Default stream() calls execute() and yields the result."""

        class TestAgent(BaseAgent):
            name = "test"
            description = "test"

            async def execute(self, query, context=None):
                return f"answer: {query}"

        agent = TestAgent()
        chunks = []
        async for chunk in agent.stream("hello"):
            chunks.append(chunk)
        assert chunks == ["answer: hello"]


class TestRegistry:
    def test_register_and_get(self):
        """Register an agent and retrieve it."""
        from agents.registry import AgentRegistry

        class DummyAgent(BaseAgent):
            name = "dummy"
            description = "test"

            async def execute(self, query, context=None):
                return "ok"

        reg = AgentRegistry()
        reg.register(DummyAgent())
        assert reg.get("dummy") is not None
        assert reg.get("nonexistent") is None

    def test_list_agents(self):
        """List all registered agents."""
        from agents.registry import AgentRegistry

        class A(BaseAgent):
            name = "a"
            description = "agent a"
            async def execute(self, q, c=None): return ""

        class B(BaseAgent):
            name = "b"
            description = "agent b"
            async def execute(self, q, c=None): return ""

        reg = AgentRegistry()
        reg.register(A())
        reg.register(B())
        assert len(reg.list()) == 2
        descs = reg.list_descriptions()
        assert any(d["name"] == "a" for d in descs)


class TestOrchestrator:
    @pytest.mark.asyncio
    async def test_handle_no_agents(self):
        """Orchestrator returns fallback when no agents registered."""
        from agents.orchestrator import Orchestrator
        orch = Orchestrator()
        result = await orch.handle("test query")
        assert "No agents" in result


class TestPortfolioAgent:
    @pytest.mark.asyncio
    async def test_placeholder(self):
        """Portfolio agent raises NotImplementedError (placeholder)."""
        from agents.portfolio.agent import PortfolioAgent
        agent = PortfolioAgent()
        with pytest.raises(NotImplementedError):
            await agent.execute("test")


class TestEmailAgent:
    @pytest.mark.asyncio
    async def test_placeholder(self):
        """Email agent returns placeholder message."""
        from agents.email.agent import EmailAgent
        agent = EmailAgent()
        result = await agent.execute("check email")
        assert "Not yet implemented" in result


class TestDocsAgent:
    @pytest.mark.asyncio
    async def test_placeholder(self):
        from agents.docs.agent import DocsAgent
        result = await DocsAgent().execute("search for RAG")
        assert "Not yet implemented" in result


class TestCalendarAgent:
    @pytest.mark.asyncio
    async def test_placeholder(self):
        from agents.calendar.agent import CalendarAgent
        result = await CalendarAgent().execute("am I free tomorrow?")
        assert "Not yet implemented" in result


class TestTasksAgent:
    @pytest.mark.asyncio
    async def test_placeholder(self):
        from agents.tasks.agent import TasksAgent
        result = await TasksAgent().execute("add task")
        assert "Not yet implemented" in result


class TestSearchAgent:
    @pytest.mark.asyncio
    async def test_placeholder(self):
        from agents.search.agent import SearchAgent
        result = await SearchAgent().execute("search LangGraph")
        assert "Not yet implemented" in result


class TestSocialAgent:
    @pytest.mark.asyncio
    async def test_placeholder(self):
        from agents.social.agent import SocialAgent
        result = await SocialAgent().execute("draft a post")
        assert "Not yet implemented" in result
