"""
Tests for voice/ module.

- test_stt_factory: create_stt returns correct provider
- test_tts_factory: create_tts returns correct provider
- test_vad: VAD processor initialization
- test_web_transport: WebSocket handler accepts and closes
- test_cli_transport: CLI voice placeholder
"""

import pytest
from voice.stt import create_stt, DeepgramSTT, GroqSTT, LocalSTT
from voice.tts import create_tts, ElevenLabsTTS, OpenAITTS, LocalTTS


class TestSTTFactory:
    def test_create_deepgram(self):
        stt = create_stt("deepgram")
        assert isinstance(stt, DeepgramSTT)

    def test_create_groq(self):
        stt = create_stt("groq")
        assert isinstance(stt, GroqSTT)

    def test_create_local(self):
        stt = create_stt("local")
        assert isinstance(stt, LocalSTT)

    def test_unknown_provider(self):
        with pytest.raises(ValueError):
            create_stt("nonexistent")


class TestTTSFactory:
    def test_create_elevenlabs(self):
        tts = create_tts("elevenlabs")
        assert isinstance(tts, ElevenLabsTTS)

    def test_create_openai(self):
        tts = create_tts("openai")
        assert isinstance(tts, OpenAITTS)

    def test_create_local(self):
        tts = create_tts("local")
        assert isinstance(tts, LocalTTS)

    def test_unknown_provider(self):
        with pytest.raises(ValueError):
            create_tts("nonexistent")


class TestVAD:
    def test_init(self):
        from voice.vad import VADProcessor
        vad = VADProcessor()
        assert vad.threshold == 0.5
        assert vad._is_speaking is False

    def test_reset(self):
        from voice.vad import VADProcessor
        vad = VADProcessor()
        vad._is_speaking = True
        vad.reset()
        assert vad._is_speaking is False


class TestSTTPlaceholders:
    @pytest.mark.asyncio
    async def test_deepgram_transcribe_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await DeepgramSTT().transcribe(b"audio")

    @pytest.mark.asyncio
    async def test_groq_transcribe_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await GroqSTT().transcribe(b"audio")


class TestTTSPlaceholders:
    @pytest.mark.asyncio
    async def test_elevenlabs_synthesize_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await ElevenLabsTTS().synthesize("hello")

    @pytest.mark.asyncio
    async def test_openai_synthesize_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await OpenAITTS().synthesize("hello")
