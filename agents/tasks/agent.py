"""
Tasks Agent — local task / to-do management.

SQLite-backed via core.state. No external dependencies.
Optional future sync with Notion or Todoist.
"""

from agents.base import BaseAgent, Tool


class TasksAgent(BaseAgent):
    name = "tasks"
    description = (
        "Manages personal tasks and to-dos. Can add tasks, list them, "
        "mark as complete, and prioritize. All stored locally."
    )
    tools = [
        Tool(name="add_task", description="Add a new task"),
        Tool(name="list_tasks", description="List all tasks"),
        Tool(name="complete_task", description="Mark a task as done"),
        Tool(name="prioritize", description="Reorder tasks by priority"),
    ]

    async def execute(self, query: str, context: dict | None = None) -> str:
        # TODO: Phase 4
        return "[Tasks Agent] Not yet implemented. Coming in Phase 4."
