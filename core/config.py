"""
Global configuration for the entire agent system.

Single source of truth for:
- LLM provider settings
- Voice provider settings (STT, TTS)
- Auth / credential paths
- Database paths
- Content / RAG paths

Usage:
    from core.config import cfg
    model = cfg.llm.model
    stt = cfg.voice.stt_provider
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv

# ── Paths ─────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env.local")
load_dotenv(PROJECT_ROOT / ".env")


@dataclass
class LLMConfig:
    provider: str = os.getenv("LLM_PROVIDER", "groq")
    model: str = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    base_url: str = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    api_key: str = os.getenv("GROQ_API_KEY", "")
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "512"))
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    streaming: bool = True  # needed for voice


@dataclass
class STTConfig:
    provider: str = os.getenv("STT_PROVIDER", "deepgram")  # deepgram | groq | local
    api_key: str = os.getenv("DEEPGRAM_API_KEY", "")
    model: str = os.getenv("STT_MODEL", "nova-2")
    language: str = "en"


@dataclass
class TTSConfig:
    provider: str = os.getenv("TTS_PROVIDER", "elevenlabs")  # elevenlabs | openai | local
    api_key: str = os.getenv("ELEVENLABS_API_KEY", "")
    voice_id: str = os.getenv("TTS_VOICE_ID", "")
    speed: float = float(os.getenv("TTS_SPEED", "1.0"))


@dataclass
class VoiceConfig:
    stt: STTConfig = field(default_factory=STTConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)
    livekit_url: str = os.getenv("LIVEKIT_URL", "")
    livekit_api_key: str = os.getenv("LIVEKIT_API_KEY", "")
    livekit_api_secret: str = os.getenv("LIVEKIT_API_SECRET", "")
    vad_threshold: float = float(os.getenv("VAD_THRESHOLD", "0.5"))
    vad_silence_ms: int = int(os.getenv("VAD_SILENCE_MS", "500"))


@dataclass
class AuthConfig:
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    azure_client_id: str = os.getenv("AZURE_CLIENT_ID", "")
    azure_tenant_id: str = os.getenv("AZURE_TENANT_ID", "")
    credentials_dir: Path = PROJECT_ROOT / "data" / "credentials"


@dataclass
class PathsConfig:
    project_root: Path = PROJECT_ROOT
    content_dir: Path = PROJECT_ROOT / "content"
    rag_storage_dir: Path = PROJECT_ROOT / "rag_storage"
    prompts_dir: Path = PROJECT_ROOT / "pipeline" / "prompts"
    data_dir: Path = PROJECT_ROOT / "data"
    db_path: Path = PROJECT_ROOT / "data" / "state.db"


@dataclass
class AppConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    voice: VoiceConfig = field(default_factory=VoiceConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)


# ── Singleton ─────────────────────────────────────────────────
cfg = AppConfig()
