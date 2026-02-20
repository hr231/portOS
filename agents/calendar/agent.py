"""
Calendar Agent — manages Google Calendar and Outlook Calendar.

Tools: check_availability, create_event, list_events, find_free_slots
Reuses OAuth from email agent (same Google/MS Graph credentials).
"""

from agents.base import BaseAgent, Tool


class CalendarAgent(BaseAgent):
    name = "calendar"
    description = (
        "Manages calendar across Google Calendar and Outlook. Can check availability, "
        "create events, list upcoming events, and find free time slots."
    )
    tools = [
        Tool(name="check_availability", description="Check if a time slot is free"),
        Tool(name="create_event", description="Create a calendar event"),
        Tool(name="list_events", description="List upcoming events"),
        Tool(name="find_free_slots", description="Find available time slots"),
    ]

    async def execute(self, query: str, context: dict | None = None) -> str:
        # TODO: Phase 4
        return "[Calendar Agent] Not yet implemented. Coming in Phase 4."
