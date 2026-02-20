"""
Voice Activity Detection (VAD) — detects speech segments in audio.

Uses silero-vad (best open-source VAD).
Handles:
- Speech start/end detection
- Interruption detection (user speaks mid-response)
- Silence-based turn-ending

Usage:
    from voice.vad import VADProcessor
    vad = VADProcessor()
    for chunk in audio_stream:
        event = vad.process(chunk)
        if event == "speech_start": ...
        elif event == "speech_end": ...
"""

from voice.config import VAD_THRESHOLD, VAD_SILENCE_MS, VAD_MIN_SPEECH_MS


class VADProcessor:
    """Silero-VAD based voice activity detector."""

    def __init__(
        self,
        threshold: float = VAD_THRESHOLD,
        silence_ms: int = VAD_SILENCE_MS,
        min_speech_ms: int = VAD_MIN_SPEECH_MS,
    ):
        self.threshold = threshold
        self.silence_ms = silence_ms
        self.min_speech_ms = min_speech_ms
        self._model = None
        self._is_speaking = False

    def load_model(self) -> None:
        """Load silero-vad model."""
        # TODO: Phase 2 — load silero-vad via torch.hub or livekit-plugins-silero
        raise NotImplementedError("Phase 2: implement VAD model loading")

    def process(self, audio_chunk: bytes) -> str | None:
        """
        Process an audio chunk. Returns event or None.
        Events: "speech_start", "speech_end", "interruption"
        """
        # TODO: Phase 2
        raise NotImplementedError("Phase 2: implement VAD processing")

    def reset(self) -> None:
        """Reset VAD state (e.g., after handling an interruption)."""
        self._is_speaking = False
