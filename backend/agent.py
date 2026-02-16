"""
Agent logic — separated from the HTTP layer.

Handles:
1. LightRAG knowledge graph queries
2. Context-injected Groq fallback
3. Prompt loading from pipeline/prompts/
"""

from functools import partial

from backend.config import (
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


# ── LightRAG Instance ────────────────────────────────────────

def create_rag():
    """Create a LightRAG instance using shared pipeline config."""
    import numpy as np
    from lightrag import LightRAG
    from lightrag.llm.openai import openai_complete
    from lightrag.utils import EmbeddingFunc

    # Import embedding from pipeline (shared with indexer)
    from pipeline.embeddings import get_embedding_func

    groq_complete = partial(
        openai_complete,
        api_key=GROQ_API_KEY,
        base_url=LLM_BASE_URL,
    )

    return LightRAG(
        working_dir=str(RAG_STORAGE_DIR),
        llm_model_func=groq_complete,
        llm_model_name=LLM_MODEL,
        embedding_func=EmbeddingFunc(
            embedding_dim=EMBEDDING_DIM,
            max_token_size=EMBEDDING_MAX_TOKENS,
            func=get_embedding_func(),
        ),
    )


# ── Portfolio Context ─────────────────────────────────────────

def load_portfolio_context() -> str:
    """Read all .md files from content/ for context injection."""
    texts = []
    if CONTENT_DIR.exists():
        for md_file in sorted(CONTENT_DIR.rglob("*.md")):
            text = md_file.read_text(encoding="utf-8").strip()
            if text:
                texts.append(text)
    return "\n\n---\n\n".join(texts)


# ── Query Strategies ──────────────────────────────────────────

async def query_rag(rag_instance, query: str) -> str | None:
    """
    Strategy A: Query the LightRAG knowledge graph.
    Returns the answer string or None if no useful result.
    """
    from lightrag import QueryParam

    try:
        result = await rag_instance.aquery(
            query,
            param=QueryParam(mode=RAG_QUERY_MODE),
        )
        if (result
                and isinstance(result, str)
                and len(result.strip()) > 20
                and "no-context" not in result.lower()
                and "no context" not in result.lower()
                and "not able to provide" not in result.lower()):
            return result.strip()
    except Exception as e:
        print(f"LightRAG query failed: {e}")
    return None


async def query_groq_with_context(query: str, portfolio_context: str) -> str:
    """
    Strategy B (fallback): Direct Groq call with portfolio content as context.
    Uses the system prompt from pipeline/prompts/system.md.
    """
    from groq import Groq

    system_prompt = load_prompt("system")
    ctx = portfolio_context[:CONTEXT_MAX_CHARS] if portfolio_context else ""

    if ctx:
        system_prompt += f"\n\n--- PORTFOLIO CONTEXT ---\n{ctx}\n--- END CONTEXT ---"

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        max_tokens=LLM_MAX_TOKENS,
        temperature=LLM_TEMPERATURE,
    )
    return response.choices[0].message.content or "I couldn't generate a response."


async def answer_query(rag_instance, query: str, portfolio_context: str) -> str:
    """
    Main entrypoint: try RAG first, fall back to context-injected Groq.
    """
    # Strategy A: LightRAG
    if rag_instance is not None:
        answer = await query_rag(rag_instance, query)
        if answer:
            return answer

    # Strategy B: Direct Groq with context
    return await query_groq_with_context(query, portfolio_context)
