"""
Backend configuration — reads from pipeline.config + adds backend-specific settings.
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path so pipeline/ is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.config import (  # noqa: E402
    GROQ_API_KEY,
    RAG_STORAGE_DIR,
    CONTENT_DIR,
    LLM_MODEL,
    LLM_BASE_URL,
    LLM_MAX_TOKENS,
    LLM_TEMPERATURE,
    EMBEDDING_DIM,
    EMBEDDING_MAX_TOKENS,
    RAG_QUERY_MODE,
    CONTEXT_MAX_CHARS,
    load_prompt,
)

# ── CORS origins ──────────────────────────────────────────────
CORS_ORIGINS = [
    "http://localhost:5173",                  # Vite dev
    "http://localhost:3000",                  # fallback
    "https://portoai.vercel.app",             # Vercel production
]
CORS_ORIGIN_REGEX = r"https://.*\.vercel\.app"  # all Vercel preview deploys
