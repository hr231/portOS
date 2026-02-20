"""
Agent Registry — auto-discovers and registers agents.

Scans agents/*/agent.py for BaseAgent subclasses.
No manual registration needed — drop a new agent module and it's live.

Usage:
    from agents.registry import registry
    await registry.discover()
    agent = registry.get("email")
    all_agents = registry.list()
"""

import importlib
import pkgutil
from pathlib import Path

from agents.base import BaseAgent


class AgentRegistry:
    """Discovers and manages agent instances."""

    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    async def discover(self) -> None:
        """
        Scan agents/ subdirectories for BaseAgent subclasses.
        Imports each agents/<name>/agent.py and registers instances.
        """
        # TODO: Phase 1 — implement auto-discovery
        # For now, manual registration works:
        #   registry.register(MyAgent())
        raise NotImplementedError("Phase 1: implement auto-discovery")

    def register(self, agent: BaseAgent) -> None:
        """Manually register an agent instance."""
        self._agents[agent.name] = agent

    def get(self, name: str) -> BaseAgent | None:
        """Get an agent by name."""
        return self._agents.get(name)

    def list(self) -> list[BaseAgent]:
        """List all registered agents."""
        return list(self._agents.values())

    def list_descriptions(self) -> list[dict]:
        """Return agent names + descriptions (used by orchestrator for routing)."""
        return [
            {"name": a.name, "description": a.description}
            for a in self._agents.values()
        ]

    async def initialize_all(self) -> None:
        """Call initialize() on all registered agents."""
        for agent in self._agents.values():
            await agent.initialize()

    async def shutdown_all(self) -> None:
        """Call shutdown() on all registered agents."""
        for agent in self._agents.values():
            await agent.shutdown()


# ── Singleton ─────────────────────────────────────────────────
registry = AgentRegistry()
