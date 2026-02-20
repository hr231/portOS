"""
Email Agent — manages Gmail and Outlook email.

Tools: read_inbox, search_email, send_reply, draft_email, summarize_thread
Supports instruction-based auto-reply via rules.yaml.

Voice example:
    "Check my email" → reads inbox summary
    "Reply to the one from Professor Smith" → drafts and confirms reply
"""

from agents.base import BaseAgent, Tool


class EmailAgent(BaseAgent):
    name = "email"
    description = (
        "Manages email across Gmail and Outlook. Can read inbox, search emails, "
        "draft replies, send messages, and summarize threads. Use for any email-related tasks."
    )
    tools = [
        Tool(name="read_inbox", description="Read recent emails from inbox"),
        Tool(name="search_email", description="Search emails by query"),
        Tool(name="send_reply", description="Reply to an email"),
        Tool(name="draft_email", description="Draft a new email"),
        Tool(name="summarize_thread", description="Summarize an email thread"),
    ]

    async def execute(self, query: str, context: dict | None = None) -> str:
        # TODO: Phase 3
        return "[Email Agent] Not yet implemented. Coming in Phase 3."

    async def initialize(self) -> None:
        # TODO: Phase 3 — check auth, load rules
        pass
