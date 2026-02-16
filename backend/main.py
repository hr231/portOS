"""
FastAPI backend — slim HTTP layer.

All logic lives in backend/agent.py.
All config lives in pipeline/config.py + backend/config.py.

Run locally:   make backend
Deploy:        make deploy
"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import (  # noqa: E402
    GROQ_API_KEY,
    RAG_STORAGE_DIR,
    CORS_ORIGINS,
    CORS_ORIGIN_REGEX,
)
from backend.agent import (  # noqa: E402
    create_rag,
    load_portfolio_context,
    answer_query,
)


# ── Global state ──────────────────────────────────────────────
rag_instance = None
portfolio_context = ""


# ── Lifecycle ─────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_instance, portfolio_context

    # Load raw content for context-injection fallback
    portfolio_context = load_portfolio_context()
    print(f"Portfolio context: {len(portfolio_context)} chars" if portfolio_context else "WARNING: No content found")

    if not GROQ_API_KEY:
        print("WARNING: GROQ_API_KEY not set — /api/chat will fail")

    # Load knowledge graph
    if RAG_STORAGE_DIR.exists():
        try:
            rag_instance = create_rag()
            await rag_instance.initialize_storages()
            print("Knowledge graph loaded ✓")
        except Exception as e:
            print(f"WARNING: Knowledge graph failed to load: {e}")
            rag_instance = None
    else:
        print(f"WARNING: {RAG_STORAGE_DIR} not found — run 'make ingest' first")

    yield
    rag_instance = None


# ── App ───────────────────────────────────────────────────────
app = FastAPI(title="HarshitOS Agent API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str


# ── Endpoints ─────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "graph_loaded": rag_instance is not None,
        "storage_exists": RAG_STORAGE_DIR.exists(),
        "context_loaded": bool(portfolio_context),
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        answer = await answer_query(rag_instance, query, portfolio_context)
    except Exception as e:
        print(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {e}")

    return ChatResponse(answer=answer)
