"""
Voice route — WebSocket /api/voice

Real-time bidirectional audio for browser-based voice.
Browser sends mic audio, receives TTS audio.
"""

from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/api/voice")
async def voice_ws(websocket: WebSocket):
    """Handle real-time voice session over WebSocket."""
    # TODO: Phase 2 — implement with voice/web_transport.py
    from voice.web_transport import voice_websocket
    await voice_websocket(websocket)
