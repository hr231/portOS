"""
Orchestrator — routes user queries to the correct agent.

Uses LLM function-calling to classify intent and pick an agent.
Falls back to the portfolio agent if unsure.

Usage:
    from agents.orchestrator import orchestrator
    response = await orchestrator.handle("Check my email", session_context)
    async for chunk in orchestrator.handle_stream("Tell me about Harshit", ctx):
        print(chunk, end="")
"""

from typing import AsyncIterator

from agents.registry import registry


class Orchestrator:
    """Routes queries to the appropriate agent via LLM intent classification."""

    def __init__(self):
        self._default_agent = "portfolio"

    async def handle(self, query: str, context: dict | None = None) -> str:
        """
        Route a text query to the right agent and return the response.
        
        Steps:
            1. Get list of available agents + descriptions
            2. Ask LLM to classify intent (function-calling)
            3. Delegate to chosen agent's execute()
            4. Return response
        """
        # TODO: Phase 1 — implement LLM-based routing
        # Placeholder: route everything to portfolio agent
        agent = registry.get(self._default_agent)
        if agent:
            return await agent.execute(query, context)
        return "No agents available."

    async def handle_stream(self, query: str, context: dict | None = None) -> AsyncIterator[str]:
        """
        Streaming version for voice mode.
        Routes to agent's stream() method.
        """
        # TODO: Phase 1 — implement with streaming
        agent = registry.get(self._default_agent)
        if agent:
            async for chunk in agent.stream(query, context):
                yield chunk
        else:
            yield "No agents available."

    async def _classify_intent(self, query: str) -> str:
        """
        Use LLM function-calling to determine which agent handles this query.
        Returns agent name.
        """
        # TODO: Phase 1 — implement with core.llm.function_call()
        raise NotImplementedError("Phase 1: implement intent classification")


# ── Singleton ─────────────────────────────────────────────────
orchestrator = Orchestrator()
