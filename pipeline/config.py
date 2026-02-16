"""
Central configuration for the RAG pipeline.

Edit this file to change models, embedding dimensions, paths, etc.
No code changes needed elsewhere — everything reads from here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Paths ─────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env.local")
load_dotenv(PROJECT_ROOT / ".env")

CONTENT_DIR = PROJECT_ROOT / "content"
RAG_STORAGE_DIR = PROJECT_ROOT / "rag_storage"
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
INDEX_STATE_FILE = RAG_STORAGE_DIR / ".index_state.json"

# ── API Keys ──────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ── LLM Settings ─────────────────────────────────────────────
LLM_PROVIDER = "groq"                          # groq | openai | ollama
LLM_MODEL = "llama-3.3-70b-versatile"          # model name
LLM_BASE_URL = "https://api.groq.com/openai/v1"
LLM_MAX_TOKENS = 300
LLM_TEMPERATURE = 0.7

# ── Embedding Settings ────────────────────────────────────────
EMBEDDING_TYPE = "hash"       # "hash" (local, free) or "api" (needs key)
EMBEDDING_DIM = 256
EMBEDDING_MAX_TOKENS = 8192

# ── RAG Query Settings ────────────────────────────────────────
RAG_QUERY_MODE = "naive"      # naive | local | global | hybrid
CONTEXT_MAX_CHARS = 6000      # max chars of raw content injected as context

# ── Content Settings ──────────────────────────────────────────
SUPPORTED_EXTENSIONS = [".md", ".txt"]  # file types to ingest


def load_prompt(name: str) -> str:
    """Load a prompt template from pipeline/prompts/<name>.md"""
    prompt_file = PROMPTS_DIR / f"{name}.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8").strip()
    return ""
