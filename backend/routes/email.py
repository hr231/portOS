"""
Email routes — /api/email/*

REST endpoints for the email agent (used by web UI).
"""

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/email")


@router.get("/inbox")
async def get_inbox(provider: str = "gmail", limit: int = 10):
    """Get recent inbox emails."""
    # TODO: Phase 3
    raise HTTPException(status_code=501, detail="Email agent not yet implemented")


@router.get("/search")
async def search_email(q: str, provider: str = "gmail"):
    """Search emails."""
    # TODO: Phase 3
    raise HTTPException(status_code=501, detail="Email agent not yet implemented")


@router.post("/reply")
async def reply_email(thread_id: str, body: str, provider: str = "gmail"):
    """Reply to an email thread."""
    # TODO: Phase 3
    raise HTTPException(status_code=501, detail="Email agent not yet implemented")


@router.post("/draft")
async def draft_email(to: str, subject: str, body: str, provider: str = "gmail"):
    """Create a draft email."""
    # TODO: Phase 3
    raise HTTPException(status_code=501, detail="Email agent not yet implemented")
