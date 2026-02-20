"""
Social Agent — LinkedIn and content generation.

Can draft LinkedIn posts, generate content based on portfolio context,
and (with API access) post directly.
"""

from agents.base import BaseAgent, Tool


class SocialAgent(BaseAgent):
    name = "social"
    description = (
        "Manages social media presence. Can draft LinkedIn posts, generate "
        "professional content, and schedule posts."
    )
    tools = [
        Tool(name="draft_linkedin_post", description="Draft a LinkedIn post"),
        Tool(name="post_to_linkedin", description="Post to LinkedIn"),
        Tool(name="draft_content", description="Generate professional content"),
    ]

    async def execute(self, query: str, context: dict | None = None) -> str:
        # TODO: Phase 5
        return "[Social Agent] Not yet implemented. Coming in Phase 5."
