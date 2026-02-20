"""
Base Agent Protocol.

Every agent inherits from BaseAgent and implements execute() + optionally stream().
The orchestrator uses `name` and `description` to route queries.

To create a new agent:
    1. Create agents/myagent/agent.py
    2. Subclass BaseAgent
    3. Implement execute()
    4. The registry auto-discovers it — no registration needed.

Example:
    class MyAgent(BaseAgent):
        name = "my_agent"
        description = "Handles XYZ tasks"
        tools = [my_tool_1, my_tool_2]

        async def execute(self, query, context):
            return "response"
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import AsyncIterator, Callable, Any


@dataclass
class Tool:
    """A callable tool that an agent can use."""
    name: str
    description: str
    parameters: dict = field(default_factory=dict)  # JSON Schema
    func: Callable[..., Any] = None

    def __repr__(self):
        return f"Tool({self.name})"


class BaseAgent(ABC):
    """Abstract base for all agents."""

    name: str = "unnamed"
    description: str = "No description"
    tools: list[Tool] = []

    @abstractmethod
    async def execute(self, query: str, context: dict | None = None) -> str:
        """
        Handle a routed query. Returns full response text.
        
        Args:
            query: The user's question or command
            context: Dict with session info, memory, auth tokens, etc.
        
        Returns:
            Response text
        """
        ...

    async def stream(self, query: str, context: dict | None = None) -> AsyncIterator[str]:
        """
        Streaming response for voice mode. Yields text chunks.
        Default: calls execute() and yields the full result.
        Override for true streaming.
        """
        result = await self.execute(query, context)
        yield result

    def get_tool_schemas(self) -> list[dict]:
        """Return tool definitions as JSON Schema for function calling."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
            }
            for t in self.tools
        ]

    async def initialize(self) -> None:
        """Optional setup called once when the agent is loaded."""
        pass

    async def shutdown(self) -> None:
        """Optional cleanup called when the agent is unloaded."""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"
