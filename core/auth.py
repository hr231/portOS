"""
Auth & Credential Management.

Handles:
- OAuth2 PKCE flows for Gmail and Outlook
- Token storage via keyring (encrypted, OS-native)
- Token refresh

Usage:
    from core.auth import auth_manager
    await auth_manager.authenticate("gmail")
    token = auth_manager.get_token("gmail")
"""

from core.config import cfg


class AuthManager:
    """Manages OAuth2 credentials for external services."""

    def __init__(self):
        self._config = cfg.auth
        self._tokens: dict[str, str] = {}  # in-memory cache

    async def authenticate(self, service: str) -> bool:
        """
        Run OAuth2 flow for a service.
        Supported: "gmail", "outlook"
        Stores token in keyring.
        """
        # TODO: Phase 3 — implement OAuth2 PKCE per service
        raise NotImplementedError(f"Phase 3: implement OAuth2 for {service}")

    def get_token(self, service: str) -> str | None:
        """Get a valid access token for a service. Auto-refreshes if expired."""
        # TODO: Phase 3 — implement token retrieval + refresh
        raise NotImplementedError(f"Phase 3: implement token retrieval for {service}")

    def is_authenticated(self, service: str) -> bool:
        """Check if we have valid credentials for a service."""
        # TODO: Phase 3
        return False

    async def revoke(self, service: str) -> None:
        """Revoke and delete credentials for a service."""
        # TODO: Phase 3
        raise NotImplementedError(f"Phase 3: implement revocation for {service}")


# ── Singleton ─────────────────────────────────────────────────
auth_manager = AuthManager()
