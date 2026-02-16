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

# ------------------------------------------------------------------
# Global LightRAG instance (loaded on startup)
# ------------------------------------------------------------------
rag_instance = None


def create_rag():
    """Create and return a LightRAG instance pointing at the pre-built graph."""
    import numpy as np
    from lightrag import LightRAG
    from lightrag.llm.groq import groq_complete
    from lightrag.utils import EmbeddingFunc

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
        llm_model_kwargs={"api_key": GROQ_API_KEY},
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
    """Load LightRAG graph on startup."""
    global rag_instance
    if not GROQ_API_KEY:
        print("WARNING: GROQ_API_KEY not set — /api/chat will return errors")
    if RAG_STORAGE_DIR.exists():
        print(f"Loading knowledge graph from {RAG_STORAGE_DIR} ...")
        rag_instance = create_rag()
        print("Knowledge graph loaded ✓")
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
        "http://localhost:5173",       # Vite dev
        "http://localhost:3000",       # fallback
        "https://*.vercel.app",        # Vercel preview URLs
        # Add your custom domain here if you have one:
        # "https://harshit.dev",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
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
# Fallback: direct Groq call when knowledge graph is not available
# ------------------------------------------------------------------
FALLBACK_SYSTEM_PROMPT = """You are Harshit B.'s portfolio AI assistant on his retro OS-themed website.
Answer questions about Harshit based on what you know. Be concise, friendly, and technical.
If you don't know something, say so honestly. Keep answers under 150 words.
Harshit is an AI Engineer Intern at Staples Inc., previously ML Engineer at Pixeltechnologies
and Data Analyst at GROWITUP. He's pursuing MS Data Analytics at Northeastern (3.9 GPA).
He builds production ML systems with LangGraph, FastAPI, vLLM, Kubernetes, and RAG pipelines."""


async def fallback_groq_chat(query: str) -> str:
    """Direct Groq API call when LightRAG graph is unavailable."""
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": FALLBACK_SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "graph_loaded": rag_instance is not None,
        "storage_exists": RAG_STORAGE_DIR.exists(),
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        if rag_instance is not None:
            # Use LightRAG knowledge graph (hybrid mode = graph + vector)
            from lightrag import QueryParam
            answer = await rag_instance.aquery(
                query,
                param=QueryParam(mode="hybrid"),
            )
        else:
            # Fallback to direct Groq when graph not available
            answer = await fallback_groq_chat(query)

        return ChatResponse(answer=answer)

    except Exception as e:
        print(f"Chat error: {e}")
        # Try fallback on any LightRAG error
        try:
            answer = await fallback_groq_chat(query)
            return ChatResponse(answer=answer)
        except Exception as fallback_err:
            raise HTTPException(status_code=500, detail=str(fallback_err))
