"""
Voice-specific configuration.

Separate from core/config.py for voice-only settings like
audio format, sample rates, buffer sizes, etc.
"""

# Audio format defaults
SAMPLE_RATE = 16000          # 16kHz for STT
OUTPUT_SAMPLE_RATE = 24000   # 24kHz for TTS playback
CHANNELS = 1                 # mono
CHUNK_SIZE = 4096            # audio buffer size in bytes
FORMAT = "pcm_s16le"         # 16-bit PCM

# VAD defaults
VAD_THRESHOLD = 0.5          # speech probability threshold
VAD_MIN_SPEECH_MS = 250      # minimum speech duration to trigger
VAD_SILENCE_MS = 500         # silence duration to end turn
VAD_PREFIX_PADDING_MS = 300  # audio to keep before speech start

# Streaming
STT_INTERIM_RESULTS = True   # send partial transcripts
TTS_CHUNK_SIZE = 4096        # TTS audio chunk size for streaming
