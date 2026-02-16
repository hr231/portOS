"""
FastAPI backend for the HarshitOS portfolio agent.
Loads a pre-built LightRAG knowledge graph and serves queries via Groq.

Run locally:
    cd portfolio
    export GROQ_API_KEY=gsk_...
    uvicorn backend.main:app --reload --port 8000

Deploy on Render:
    Build command:  pip install -r backend/requirements.txt
    Start command:  uvicorn backend.main:app --host 0.0.0.0 --port $PORT
"""

import os
from pathlib import Path
from functools import partial
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env.local")
load_dotenv(PROJECT_ROOT / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
RAG_STORAGE_DIR = PROJECT_ROOT / "rag_storage"
CONTENT_DIR = PROJECT_ROOT / "content"

# ------------------------------------------------------------------
# Global state
# ------------------------------------------------------------------
rag_instance = None
portfolio_context = ""  # loaded from content/ at startup


def load_portfolio_context() -> str:
    """Read all .md files from content/ to use as context for the LLM."""
    texts = []
    if CONTENT_DIR.exists():
        for md_file in sorted(CONTENT_DIR.rglob("*.md")):
            text = md_file.read_text(encoding="utf-8").strip()
            if text:
                texts.append(text)
    return "\n\n---\n\n".join(texts)


def create_rag():
    """Create and return a LightRAG instance pointing at the pre-built graph."""
    import numpy as np
    from lightrag import LightRAG
    from lightrag.llm.openai import openai_complete
    from lightrag.utils import EmbeddingFunc

    groq_complete = partial(
        openai_complete,
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )

    async def local_embedding(texts: list[str]) -> np.ndarray:
        """Deterministic hash-based embedding (matches the indexer)."""
        from lightrag.utils import compute_mdhash_id
        dim = 256
        embeddings = []
        for text in texts:
            h = compute_mdhash_id(text, prefix="")
            seed = int(h[:8], 16)
            rng = np.random.RandomState(seed)
            vec = rng.randn(dim).astype(np.float32)
            vec = vec / (np.linalg.norm(vec) + 1e-9)
            embeddings.append(vec)
        return np.array(embeddings)

    return LightRAG(
        working_dir=str(RAG_STORAGE_DIR),
        llm_model_func=groq_complete,
        llm_model_name="llama-3.3-70b-versatile",
        embedding_func=EmbeddingFunc(
            embedding_dim=256,
            max_token_size=8192,
            func=local_embedding,
        ),
    )


# ------------------------------------------------------------------
# App lifecycle
# ------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load portfolio context and LightRAG graph on startup."""
    global rag_instance, portfolio_context

    # Always load raw content for context-injection fallback
    portfolio_context = load_portfolio_context()
    if portfolio_context:
        print(f"Portfolio context loaded ({len(portfolio_context)} chars)")
    else:
        print("WARNING: No .md files found in content/")

    if not GROQ_API_KEY:
        print("WARNING: GROQ_API_KEY not set — /api/chat will return errors")

    if RAG_STORAGE_DIR.exists():
        print(f"Loading knowledge graph from {RAG_STORAGE_DIR} ...")
        try:
            rag_instance = create_rag()
            await rag_instance.initialize_storages()
            print("Knowledge graph loaded ✓")
        except Exception as e:
            print(f"WARNING: Failed to load knowledge graph: {e}")
            rag_instance = None
    else:
        print(f"WARNING: {RAG_STORAGE_DIR} not found — run scripts/index.py first")

    yield
    rag_instance = None


# ------------------------------------------------------------------
# FastAPI app
# ------------------------------------------------------------------
app = FastAPI(
    title="HarshitOS Agent API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow the Vercel frontend (and localhost for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",                          # Vite dev
        "http://localhost:3000",                          # fallback
        "https://portoai.vercel.app",                     # Vercel production
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",        # all Vercel preview deploys
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------
# Request / Response models
# ------------------------------------------------------------------
class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str


# ------------------------------------------------------------------
# Context-aware Groq chat (primary method)
# ------------------------------------------------------------------
SYSTEM_PROMPT_TEMPLATE = """You are Harshit B.'s portfolio AI assistant on his retro OS-themed website called HarshitOS.
Answer questions about Harshit based on the provided context. Be concise, friendly, and technical.
If you don't know something, say so honestly. Keep answers under 150 words.
Use the context below to provide accurate, specific answers.

--- PORTFOLIO CONTEXT ---
{context}
--- END CONTEXT ---"""


async def context_groq_chat(query: str) -> str:
    """Groq API call with portfolio content injected as context."""
    from groq import Groq

    # Truncate context to ~6000 chars to stay within token limits
    ctx = portfolio_context[:6000] if portfolio_context else "No portfolio content available."
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=ctx)

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content or "I couldn't generate a response."


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------
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

    # Strategy:
    # 1. Try LightRAG naive mode (no structured output needed)
    # 2. If that fails or returns empty, use context-injected Groq chat
    answer = None

    if rag_instance is not None:
        try:
            from lightrag import QueryParam
            result = await rag_instance.aquery(
                query,
                param=QueryParam(mode="naive"),
            )
            # Only accept meaningful responses (reject empty, no-context, or very short)
            if (result
                    and isinstance(result, str)
                    and len(result.strip()) > 20
                    and "no-context" not in result.lower()
                    and "no context" not in result.lower()
                    and "not able to provide" not in result.lower()):
                answer = result.strip()
        except Exception as e:
            print(f"LightRAG query failed (falling back to context chat): {e}")

    # Fallback: direct Groq with portfolio context
    if not answer:
        try:
            answer = await context_groq_chat(query)
        except Exception as e:
            print(f"Context chat error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to generate response: {e}")

    return ChatResponse(answer=answer)
