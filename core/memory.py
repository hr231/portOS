"""
Conversation memory — per-session message history.

Stores messages in memory (dict) with optional SQLite persistence.
Each session gets a unique ID. Memory is used by the orchestrator
to maintain context across turns.

Usage:
    from core.memory import MemoryStore
    mem = MemoryStore()
    session = mem.create_session()
    mem.add(session, role="user", content="Hello")
    mem.add(session, role="assistant", content="Hi!")
    history = mem.get(session)
"""

import uuid
from dataclasses import dataclass, field


@dataclass
class Message:
    role: str       # "user" | "assistant" | "system"
    content: str
    agent: str = ""  # which agent handled this message
    timestamp: float = 0.0


class MemoryStore:
    """In-memory conversation store. SQLite persistence added later."""

    def __init__(self):
        self._sessions: dict[str, list[Message]] = {}

    def create_session(self) -> str:
        """Create a new conversation session. Returns session ID."""
        session_id = str(uuid.uuid4())[:8]
        self._sessions[session_id] = []
        return session_id

    def add(self, session_id: str, role: str, content: str, agent: str = "") -> None:
        """Add a message to a session."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append(Message(role=role, content=content, agent=agent))

    def get(self, session_id: str, limit: int = 20) -> list[Message]:
        """Get recent messages from a session."""
        return self._sessions.get(session_id, [])[-limit:]

    def clear(self, session_id: str) -> None:
        """Clear a session's history."""
        self._sessions[session_id] = []

    async def persist(self, session_id: str) -> None:
        """Save session to SQLite. TODO: Phase 1."""
        raise NotImplementedError("Phase 1: implement SQLite persistence")

    async def load(self, session_id: str) -> None:
        """Load session from SQLite. TODO: Phase 1."""
        raise NotImplementedError("Phase 1: implement SQLite loading")
