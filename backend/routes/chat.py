"""
Chat route — POST /api/chat

Routes text queries through the orchestrator.
This replaces the current inline chat endpoint in main.py.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    agent: str = ""  # which agent handled it
    session_id: str = ""


@router.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Handle a text chat query via the orchestrator."""
    # TODO: Phase 1 — route through orchestrator instead of direct agent call
    # For now, this is a placeholder. The existing main.py endpoint still works.
    raise HTTPException(status_code=501, detail="Route not yet migrated to orchestrator")
