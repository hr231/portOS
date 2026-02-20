"""
Persistent State Store — SQLite-backed.

Used by agents to persist data across sessions:
- Tasks (tasks agent)
- Email cache (email agent)
- Preferences (all agents)
- Conversation history (memory)

Usage:
    from core.state import state_db
    await state_db.initialize()
    await state_db.set("tasks", "task-1", {"title": "...", "done": False})
    task = await state_db.get("tasks", "task-1")
"""

from pathlib import Path
from core.config import cfg


class StateDB:
    """SQLite-backed key-value + relational store."""

    def __init__(self, db_path: Path | None = None):
        self._db_path = db_path or cfg.paths.db_path
        self._conn = None

    async def initialize(self) -> None:
        """Create tables if they don't exist."""
        # TODO: Phase 1 — implement with aiosqlite
        raise NotImplementedError("Phase 1: implement SQLite initialization")

    async def set(self, namespace: str, key: str, value: dict) -> None:
        """Store a value in a namespace."""
        # TODO: Phase 1
        raise NotImplementedError("Phase 1: implement set()")

    async def get(self, namespace: str, key: str) -> dict | None:
        """Retrieve a value from a namespace."""
        # TODO: Phase 1
        raise NotImplementedError("Phase 1: implement get()")

    async def list(self, namespace: str, limit: int = 100) -> list[dict]:
        """List all values in a namespace."""
        # TODO: Phase 1
        raise NotImplementedError("Phase 1: implement list()")

    async def delete(self, namespace: str, key: str) -> None:
        """Delete a value."""
        # TODO: Phase 1
        raise NotImplementedError("Phase 1: implement delete()")

    async def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            await self._conn.close()


# ── Singleton ─────────────────────────────────────────────────
state_db = StateDB()
