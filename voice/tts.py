"""
Text-to-Speech providers.

Supported:
- ElevenLabs (streaming, best quality)
- OpenAI TTS (good quality, simple API)
- Local Coqui XTTS (offline, free)

Usage:
    from voice.tts import create_tts
    tts = create_tts("elevenlabs")
    audio = await tts.synthesize("Hello!")
    async for chunk in tts.stream("Long response..."):
        play(chunk)
"""

from typing import AsyncIterator
from core.config import cfg


class BaseTTS:
    """Base class for TTS providers."""

    async def synthesize(self, text: str) -> bytes:
        """Batch: full text in, audio bytes out."""
        raise NotImplementedError

    async def stream(self, text: str) -> AsyncIterator[bytes]:
        """Streaming: yields audio chunks as they're generated."""
        raise NotImplementedError
        yield


class ElevenLabsTTS(BaseTTS):
    """ElevenLabs streaming TTS."""

    def __init__(self):
        self.api_key = cfg.voice.tts.api_key
        self.voice_id = cfg.voice.tts.voice_id

    async def synthesize(self, text: str) -> bytes:
        # TODO: Phase 2
        raise NotImplementedError("Phase 2: implement ElevenLabs batch TTS")

    async def stream(self, text: str) -> AsyncIterator[bytes]:
        # TODO: Phase 2 — use ElevenLabs streaming API
        raise NotImplementedError("Phase 2: implement ElevenLabs streaming TTS")
        yield


class OpenAITTS(BaseTTS):
    """OpenAI TTS-1 / TTS-1-HD."""

    async def synthesize(self, text: str) -> bytes:
        # TODO: Phase 2
        raise NotImplementedError("Phase 2: implement OpenAI TTS")

    async def stream(self, text: str) -> AsyncIterator[bytes]:
        # TODO: Phase 2
        raise NotImplementedError("Phase 2: implement OpenAI streaming TTS")
        yield


class LocalTTS(BaseTTS):
    """Local Coqui XTTS v2 (offline)."""

    async def synthesize(self, text: str) -> bytes:
        # TODO: Phase 2
        raise NotImplementedError("Phase 2: implement local Coqui TTS")


def create_tts(provider: str | None = None) -> BaseTTS:
    """Factory: create TTS instance based on provider name."""
    provider = provider or cfg.voice.tts.provider
    providers = {
        "elevenlabs": ElevenLabsTTS,
        "openai": OpenAITTS,
        "local": LocalTTS,
    }
    cls = providers.get(provider)
    if not cls:
        raise ValueError(f"Unknown TTS provider: {provider}. Options: {list(providers)}")
    return cls()
