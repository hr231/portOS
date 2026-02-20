"""
LiveKit Agents worker — the main real-time voice loop.

Connects to a LiveKit room and handles:
- Audio input via VAD + STT
- Query routing through the orchestrator
- Streaming response via TTS
- Interruption handling

This is the bridge between voice transport (WebRTC/SIP) and the agent system.

Run with: make voice-server
"""

# TODO: Phase 2 — implement with livekit-agents SDK
#
# Simplified target implementation:
#
# from livekit.agents import Agent, AgentSession
# from livekit.plugins import deepgram, elevenlabs, silero
# from agents.orchestrator import orchestrator
#
# class HarshitAgent(Agent):
#     def __init__(self):
#         super().__init__(
#             instructions="You are Harshit's personal AI assistant...",
#             stt=deepgram.STT(),
#             tts=elevenlabs.TTS(voice_id="..."),
#             vad=silero.VAD.load(),
#         )
#
#     async def on_user_turn_completed(self, turn_ctx, new_message):
#         transcript = new_message.text_content
#         response = await orchestrator.handle(transcript, session_context)
#         await turn_ctx.generate_reply(instructions=response)
#
# if __name__ == "__main__":
#     from livekit.agents import WorkerOptions, cli
#     cli.run_app(WorkerOptions(agent_cls=HarshitAgent))


def main():
    """Entry point for the LiveKit agent worker."""
    print("[voice/livekit_agent] Not yet implemented — Phase 2")
    print("  Install: pip install livekit-agents livekit-plugins-deepgram livekit-plugins-silero")
    print("  Then implement the HarshitAgent class above.")


if __name__ == "__main__":
    main()
