"""
Health route — GET /api/health

System health and status endpoint.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/health")
async def health():
    """Return system health and agent status."""
    # TODO: Phase 1 — query registry for agent statuses
    return {
        "status": "ok",
        "agents": [],  # TODO: list registered agents
        "voice": False,  # TODO: check voice pipeline status
    }
