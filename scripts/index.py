#!/usr/bin/env python3
"""
LightRAG Indexing Pipeline
--------------------------
Scans all .md files in content/ and indexes them into the knowledge graph.

Usage:
    cd portfolio
    pip install -r scripts/requirements.txt
    export GROQ_API_KEY=gsk_...
    python scripts/index.py

The knowledge graph is stored in rag_storage/ and should be committed to git
so the backend can load it at startup without re-indexing.
"""

import os
import sys
import hashlib
import json
from pathlib import Path

from dotenv import load_dotenv

# Load .env.local or .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env.local")
load_dotenv(PROJECT_ROOT / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not set. Export it or add to .env.local")
    sys.exit(1)

CONTENT_DIR = PROJECT_ROOT / "content"
RAG_STORAGE_DIR = PROJECT_ROOT / "rag_storage"
INDEX_STATE_FILE = RAG_STORAGE_DIR / ".index_state.json"


def get_file_hash(filepath: Path) -> str:
    """SHA256 hash of a file for change detection."""
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def collect_documents(content_dir: Path) -> list[dict]:
    """Recursively collect all .md files from content/."""
    docs = []
    for md_file in sorted(content_dir.rglob("*.md")):
        relative = md_file.relative_to(content_dir)
        text = md_file.read_text(encoding="utf-8").strip()
        if not text:
            continue
        docs.append({
            "path": str(relative),
            "hash": get_file_hash(md_file),
            "text": text,
        })
    return docs


def load_index_state() -> dict:
    """Load the previous indexing state to support incremental indexing."""
    if INDEX_STATE_FILE.exists():
        return json.loads(INDEX_STATE_FILE.read_text())
    return {}


def save_index_state(state: dict):
    """Persist the indexing state."""
    INDEX_STATE_FILE.write_text(json.dumps(state, indent=2))


def main():
    from lightrag import LightRAG, QueryParam
    from lightrag.llm.groq import groq_complete
    from lightrag.utils import EmbeddingFunc
    import numpy as np

    print(f"Content directory: {CONTENT_DIR}")
    print(f"RAG storage: {RAG_STORAGE_DIR}")

    # Ensure storage dir exists
    RAG_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Embedding function using a simple TF-IDF-like approach via Groq
    # LightRAG needs an embedding func; we use a lightweight local one
    # to avoid needing a separate embedding API.
    # ------------------------------------------------------------------
    async def local_embedding(texts: list[str]) -> np.ndarray:
        """
        Simple hash-based embedding fallback.
        For production, swap this with an actual embedding model.
        LightRAG's graph extraction is what matters most — embeddings
        are secondary for the knowledge-graph-based retrieval.
        """
        from lightrag.utils import compute_mdhash_id
        dim = 256
        embeddings = []
        for text in texts:
            # Deterministic pseudo-embedding from text hash
            h = compute_mdhash_id(text, prefix="")
            seed = int(h[:8], 16)
            rng = np.random.RandomState(seed)
            vec = rng.randn(dim).astype(np.float32)
            vec = vec / (np.linalg.norm(vec) + 1e-9)
            embeddings.append(vec)
        return np.array(embeddings)

    # Initialize LightRAG with Groq LLM backend
    rag = LightRAG(
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

    # Collect all documents
    docs = collect_documents(CONTENT_DIR)
    if not docs:
        print("No .md files found in content/. Nothing to index.")
        return

    print(f"Found {len(docs)} document(s)")

    # Load previous state for incremental indexing
    prev_state = load_index_state()
    new_state = {}
    indexed_count = 0

    for doc in docs:
        path = doc["path"]
        file_hash = doc["hash"]
        new_state[path] = file_hash

        # Skip if unchanged since last index
        if prev_state.get(path) == file_hash:
            print(f"  SKIP (unchanged): {path}")
            continue

        print(f"  INDEXING: {path} ...")
        try:
            rag.insert(doc["text"])
            indexed_count += 1
            print(f"    ✓ Done")
        except Exception as e:
            print(f"    ✗ Error: {e}")

    # Save updated state
    save_index_state(new_state)

    print(f"\nIndexing complete: {indexed_count} new/updated, {len(docs) - indexed_count} unchanged")
    print(f"Knowledge graph stored in: {RAG_STORAGE_DIR}")
    print("Remember to commit rag_storage/ and push!")


if __name__ == "__main__":
    main()
