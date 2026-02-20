"""
Outlook / Microsoft Graph email client.

Wraps msgraph-sdk for:
- Reading inbox
- Searching emails
- Sending replies
- Drafting emails

Auth: OAuth2 via core.auth (MSAL + keyring)
"""


class OutlookClient:
    """Microsoft Graph Mail API wrapper."""

    def __init__(self, credentials=None):
        self._creds = credentials
        self._client = None

    async def connect(self) -> None:
        """Build MS Graph client from credentials."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement Outlook connection")

    async def get_inbox(self, limit: int = 10) -> list[dict]:
        """Fetch recent inbox messages."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement inbox fetch")

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        """Search emails."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement email search")

    async def send_reply(self, message_id: str, body: str) -> dict:
        """Reply to an email."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement send reply")

    async def draft(self, to: str, subject: str, body: str) -> dict:
        """Create a draft email."""
        # TODO: Phase 3
        raise NotImplementedError("Phase 3: implement draft creation")
