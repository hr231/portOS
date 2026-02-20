"""
Email agent tools — function implementations for the agent's tool list.

Each tool is a standalone async function that the agent calls.
Tools use the Gmail/Outlook clients internally.
"""


async def read_inbox(provider: str = "gmail", limit: int = 10) -> str:
    """Read recent emails from inbox. Returns formatted summary."""
    # TODO: Phase 3
    return "[read_inbox] Not yet implemented"


async def search_email(query: str, provider: str = "gmail") -> str:
    """Search emails by query string."""
    # TODO: Phase 3
    return "[search_email] Not yet implemented"


async def send_reply(thread_id: str, body: str, provider: str = "gmail") -> str:
    """Reply to an email thread."""
    # TODO: Phase 3
    return "[send_reply] Not yet implemented"


async def draft_email(to: str, subject: str, body: str, provider: str = "gmail") -> str:
    """Draft a new email."""
    # TODO: Phase 3
    return "[draft_email] Not yet implemented"


async def summarize_thread(thread_id: str, provider: str = "gmail") -> str:
    """Summarize an email thread using LLM."""
    # TODO: Phase 3
    return "[summarize_thread] Not yet implemented"
