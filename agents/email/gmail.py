"""
Gmail API client.

Wraps google-api-python-client for:
- Reading inbox (with pagination)
- Searching emails
- Sending replies
- Managing labels
- Drafting emails

Auth: OAuth2 via core.auth (credentials stored in keyring)
"""


class GmailClient:
    """Gmail API wrapper."""

    def __init__(self, credentials=None):
        self._creds = credentials
        self._service = None

    async def connect(self) -> None:
        """Build Gmail API service from credentials."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement Gmail connection")

    async def get_inbox(self, limit: int = 10) -> list[dict]:
        """Fetch recent inbox messages."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement inbox fetch")

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        """Search emails by Gmail query syntax."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement email search")

    async def send_reply(self, thread_id: str, body: str) -> dict:
        """Reply to an email thread."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement send reply")

    async def draft(self, to: str, subject: str, body: str) -> dict:
        """Create a draft email."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement draft creation")

    async def get_thread(self, thread_id: str) -> dict:
        """Get full email thread."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement thread fetch")
