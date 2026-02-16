"""
Swappable embedding functions for LightRAG.

Currently uses a deterministic hash-based embedding (free, no API key).
To switch to a real embedding model, change EMBEDDING_TYPE in config.py
and implement the corresponding function here.
"""

import numpy as np
from pipeline.config import EMBEDDING_DIM, EMBEDDING_TYPE


async def hash_embedding(texts: list[str]) -> np.ndarray:
    """
    Deterministic hash-based embedding.
    Free, fast, no API key needed. Good enough for small knowledge graphs.
    """
    from lightrag.utils import compute_mdhash_id

    embeddings = []
    for text in texts:
        h = compute_mdhash_id(text, prefix="")
        seed = int(h[:8], 16)
        rng = np.random.RandomState(seed)
        vec = rng.randn(EMBEDDING_DIM).astype(np.float32)
        vec = vec / (np.linalg.norm(vec) + 1e-9)
        embeddings.append(vec)
    return np.array(embeddings)


# ── Add new embedding functions here ──────────────────────────
# async def openai_embedding(texts: list[str]) -> np.ndarray:
#     """Use OpenAI's text-embedding-3-small for better semantic search."""
#     import openai
#     client = openai.AsyncOpenAI()
#     response = await client.embeddings.create(model="text-embedding-3-small", input=texts)
#     return np.array([e.embedding for e in response.data], dtype=np.float32)


def get_embedding_func():
    """Return the active embedding function based on config."""
    if EMBEDDING_TYPE == "hash":
        return hash_embedding
    # elif EMBEDDING_TYPE == "openai":
    #     return openai_embedding
    else:
        raise ValueError(f"Unknown EMBEDDING_TYPE: {EMBEDDING_TYPE}")
