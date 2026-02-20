"""
Document Agent — Q&A over ingested documents via LightRAG.

Evolves the existing pipeline/ RAG into a proper agent.
Supports: search, summarize, cite, list documents.
"""

from agents.base import BaseAgent, Tool


class DocsAgent(BaseAgent):
    name = "docs"
    description = (
        "Searches and answers questions from ingested documents (markdown, PDF, etc.). "
        "Use for document Q&A, summarization, and citation."
    )
    tools = [
        Tool(name="search_docs", description="Search documents by query"),
        Tool(name="summarize_doc", description="Summarize a specific document"),
        Tool(name="list_docs", description="List all ingested documents"),
    ]

    async def execute(self, query: str, context: dict | None = None) -> str:
        # TODO: Phase 4 — wrap existing LightRAG logic
        return "[Docs Agent] Not yet implemented. Coming in Phase 4."
