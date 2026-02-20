"""
Speech-to-Text providers.

Supported:
- Deepgram (streaming, lowest latency ~300ms)
- Groq Whisper (batch, free tier)
- Local faster-whisper (offline, private)

Usage:
    from voice.stt import create_stt
    stt = create_stt("deepgram")  # or "groq" or "local"
    text = await stt.transcribe(audio_bytes)
"""

from typing import AsyncIterator
from core.config import cfg


class BaseSTT:
    """Base class for STT providers."""

    async def transcribe(self, audio: bytes) -> str:
        """Batch: full audio in, text out."""
        raise NotImplementedError

    async def stream(self, audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[str]:
        """Streaming: yields partial transcripts as audio arrives."""
        raise NotImplementedError
        yield


class DeepgramSTT(BaseSTT):
    """Deepgram Nova-2 streaming STT."""

    def __init__(self):
        self.api_key = cfg.voice.stt.api_key
        self.model = cfg.voice.stt.model

    async def transcribe(self, audio: bytes) -> str:
        # TODO: Phase 2
        raise NotImplementedError("Phase 2: implement Deepgram batch STT")

    async def stream(self, audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[str]:
        # TODO: Phase 2 — use Deepgram live streaming API
        raise NotImplementedError("Phase 2: implement Deepgram streaming STT")
        yield


class GroqSTT(BaseSTT):
    """Groq Whisper batch STT (free)."""

    async def transcribe(self, audio: bytes) -> str:
        # TODO: Phase 2
        raise NotImplementedError("Phase 2: implement Groq Whisper STT")


class LocalSTT(BaseSTT):
    """Local faster-whisper STT (offline, private)."""

    async def transcribe(self, audio: bytes) -> str:
        # TODO: Phase 2
        raise NotImplementedError("Phase 2: implement local Whisper STT")


def create_stt(provider: str | None = None) -> BaseSTT:
    """Factory: create STT instance based on provider name."""
    provider = provider or cfg.voice.stt.provider
    providers = {
        "deepgram": DeepgramSTT,
        "groq": GroqSTT,
        "local": LocalSTT,
    }
    cls = providers.get(provider)
    if not cls:
        raise ValueError(f"Unknown STT provider: {provider}. Options: {list(providers)}")
    return cls()
