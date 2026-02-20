"""
Search Agent — web search and research via Tavily API.

Can search the web, summarize URLs, and do multi-step research.
Free tier: 1000 queries/month.
"""

from agents.base import BaseAgent, Tool


class SearchAgent(BaseAgent):
    name = "search"
    description = (
        "Searches the web for real-time information. Can search by query, "
        "summarize web pages, and do multi-step research on a topic."
    )
    tools = [
        Tool(name="web_search", description="Search the web for a query"),
        Tool(name="summarize_url", description="Summarize a web page"),
        Tool(name="research_topic", description="Multi-step research on a topic"),
    ]

    async def execute(self, query: str, context: dict | None = None) -> str:
        # TODO: Phase 5
        return "[Search Agent] Not yet implemented. Coming in Phase 5."
