"""
Portfolio Agent — answers questions about Harshit's background, skills, projects.

Refactored from the original backend/agent.py.
Uses LightRAG knowledge graph + context-injected Groq fallback.

This is the existing working agent — Phase 1 wraps it in BaseAgent interface.
"""

from agents.base import BaseAgent, Tool


class PortfolioAgent(BaseAgent):
    name = "portfolio"
    description = (
        "Answers questions about Harshit's experience, skills, projects, education, "
        "and professional background. Use for any personal or career-related queries."
    )
    tools = []  # No external tools — uses RAG internally

    async def execute(self, query: str, context: dict | None = None) -> str:
        """Query the portfolio knowledge graph + fallback."""
        # TODO: Phase 1 — migrate logic from backend/agent.py
        # For now, delegate to the existing backend/agent.py
        raise NotImplementedError(
            "Phase 1: migrate backend/agent.py logic here"
        )

    async def initialize(self) -> None:
        """Load LightRAG knowledge graph + portfolio context."""
        # TODO: Phase 1 — load RAG on startup
        pass
