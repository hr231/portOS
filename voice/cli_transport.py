"""
CLI voice transport — mic/speaker for terminal use.

Uses sounddevice for cross-platform audio capture and playback.
Runs locally, no server needed.

Usage:
    from voice.cli_transport import VoiceCLI
    voice = VoiceCLI()
    await voice.start()  # starts listening loop
"""

# TODO: Phase 2 — implement with sounddevice + numpy
#
# import sounddevice as sd
# import numpy as np
# from voice.stt import create_stt
# from voice.tts import create_tts
# from voice.vad import VADProcessor
# from agents.orchestrator import orchestrator
#
# class VoiceCLI:
#     async def start(self):
#         """Start voice interaction loop."""
#         stt = create_stt()
#         tts = create_tts()
#         vad = VADProcessor()
#         print("🎙️  Listening... (Ctrl+C to stop)")
#         # Record audio → VAD → STT → orchestrator → TTS → play


class VoiceCLI:
    """Terminal voice interface. Placeholder."""

    async def start(self):
        print("[voice/cli_transport] Not yet implemented — Phase 2")
        print("  Install: pip install sounddevice numpy")
        print("  Then implement mic capture + playback loop.")
