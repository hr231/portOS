"""
Voice Gateway — provider-agnostic STT + TTS interface.

STT providers: Deepgram (streaming), Groq Whisper (batch), local faster-whisper
TTS providers: ElevenLabs (streaming), OpenAI TTS, local Coqui XTTS

Usage:
    from core.voice import stt, tts
    text = await stt.transcribe(audio_bytes)
    audio = await tts.synthesize("Hello there!")
    async for chunk in tts.stream("Long response text..."):
        play(chunk)
"""

from typing import AsyncIterator

from core.config import cfg


class STTGateway:
    """Speech-to-Text provider abstraction."""

    def __init__(self):
        self._config = cfg.voice.stt

    async def transcribe(self, audio: bytes, format: str = "wav") -> str:
        """Batch transcription — full audio in, text out."""
        # TODO: Phase 2 — implement per provider
        raise NotImplementedError("Phase 2: implement STT")

    async def stream_transcribe(self, audio_stream: AsyncIterator[bytes]) -> AsyncIterator[str]:
        """Streaming transcription — yields partial transcripts as audio arrives."""
        # TODO: Phase 2 — Deepgram streaming, or buffer + batch for others
        raise NotImplementedError("Phase 2: implement streaming STT")
        yield


class TTSGateway:
    """Text-to-Speech provider abstraction."""

    def __init__(self):
        self._config = cfg.voice.tts

    async def synthesize(self, text: str) -> bytes:
        """Batch synthesis — full text in, audio bytes out."""
        # TODO: Phase 2 — implement per provider
        raise NotImplementedError("Phase 2: implement TTS")

    async def stream(self, text: str) -> AsyncIterator[bytes]:
        """Streaming synthesis — yields audio chunks as they're generated."""
        # TODO: Phase 2 — ElevenLabs streaming, or batch + chunk for others
        raise NotImplementedError("Phase 2: implement streaming TTS")
        yield


# ── Singletons ────────────────────────────────────────────────
stt = STTGateway()
tts = TTSGateway()
