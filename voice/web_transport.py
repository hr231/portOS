"""
WebSocket transport for browser-based voice.

Provides a WebSocket endpoint that the frontend connects to for real-time audio.
Audio flows: browser mic → WebSocket → STT → orchestrator → TTS → WebSocket → browser speaker.

Alternative to LiveKit JS SDK for simpler deployments.

Usage (backend):
    from voice.web_transport import voice_websocket
    # Mount as FastAPI WebSocket route

Usage (frontend):
    const ws = new WebSocket("ws://localhost:8000/api/voice");
    ws.send(audioChunk);  // send mic audio
    ws.onmessage = (e) => playAudio(e.data);  // receive TTS audio
"""

# TODO: Phase 2 — implement WebSocket voice handler
#
# async def voice_websocket(websocket):
#     """Handle a browser voice session over WebSocket."""
#     stt = create_stt()
#     tts = create_tts()
#     vad = VADProcessor()
#
#     async for message in websocket.iter_bytes():
#         event = vad.process(message)
#         if event == "speech_end":
#             transcript = await stt.transcribe(accumulated_audio)
#             response = await orchestrator.handle(transcript)
#             async for audio_chunk in tts.stream(response):
#                 await websocket.send_bytes(audio_chunk)


async def voice_websocket(websocket):
    """Placeholder WebSocket handler."""
    await websocket.accept()
    await websocket.send_text("[voice] Not yet implemented — Phase 2")
    await websocket.close()
