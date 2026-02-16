"""
Data ingestion pipeline.

Usage:
    python -m pipeline.ingest              # incremental (only new/changed files)
    python -m pipeline.ingest --force      # reindex everything
    python -m pipeline.ingest --clear      # clear state (next run reindexes all)
    python -m pipeline.ingest --status     # show what would be indexed
"""

import sys
import asyncio
from functools import partial

from pipeline.config import (
    GROQ_API_KEY,
    RAG_STORAGE_DIR,
    LLM_MODEL,
    LLM_BASE_URL,
    EMBEDDING_DIM,
    EMBEDDING_MAX_TOKENS,
)
from pipeline.embeddings import get_embedding_func
from pipeline.processors import MarkdownProcessor


def check_api_key():
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not set.")
        print("  → Export it:  export GROQ_API_KEY=gsk_...")
        print("  → Or add to .env.local")
        sys.exit(1)


async def build_rag():
    """Create and initialize a LightRAG instance using pipeline config."""
    from lightrag import LightRAG
    from lightrag.llm.openai import openai_complete
    from lightrag.utils import EmbeddingFunc

    groq_complete = partial(
        openai_complete,
        api_key=GROQ_API_KEY,
        base_url=LLM_BASE_URL,
    )

    RAG_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    rag = LightRAG(
        working_dir=str(RAG_STORAGE_DIR),
        llm_model_func=groq_complete,
        llm_model_name=LLM_MODEL,
        embedding_func=EmbeddingFunc(
            embedding_dim=EMBEDDING_DIM,
            max_token_size=EMBEDDING_MAX_TOKENS,
            func=get_embedding_func(),
        ),
    )
    await rag.initialize_storages()
    return rag


async def run_ingest(force: bool = False):
    """Main ingestion: scan content, index changed docs into LightRAG."""
    check_api_key()

    processor = MarkdownProcessor()
    docs = processor.get_all() if force else processor.get_changed()

    if not docs and not force:
        all_docs = processor.get_all()
        if not all_docs:
            print("No documents found in content/. Nothing to index.")
            return
        print(f"All {len(all_docs)} document(s) unchanged. Nothing to index.")
        print("  → Use --force to reindex everything.")
        return

    print(f"{'Force reindexing' if force else 'Indexing'} {len(docs)} document(s)...")
    rag = await build_rag()

    indexed = 0
    for doc in docs:
        print(f"  {'REINDEX' if force else 'INDEX'}: {doc['path']} ...")
        try:
            await rag.ainsert(doc["text"])
            indexed += 1
            print(f"    ✓ Done")
        except Exception as e:
            print(f"    ✗ Error: {e}")

    processor.save_state()
    print(f"\n✓ Indexed {indexed}/{len(docs)} documents")
    print(f"  Knowledge graph: {RAG_STORAGE_DIR}")


def run_status():
    """Show what would be indexed without actually indexing."""
    processor = MarkdownProcessor()
    all_docs = processor.scan()

    if not all_docs:
        print("No documents found in content/.")
        return

    changed = [d for d in all_docs if d["changed"]]
    unchanged = [d for d in all_docs if not d["changed"]]

    print(f"Content scan: {len(all_docs)} document(s)\n")
    if changed:
        print(f"  NEW/CHANGED ({len(changed)}):")
        for d in changed:
            print(f"    + {d['path']} ({len(d['text'])} chars)")
    if unchanged:
        print(f"  UNCHANGED ({len(unchanged)}):")
        for d in unchanged:
            print(f"    · {d['path']}")
    print(f"\n  Run 'make ingest' to index {len(changed)} new/changed file(s).")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--status" in args:
        run_status()
    elif "--clear" in args:
        MarkdownProcessor().clear_state()
    elif "--force" in args:
        asyncio.run(run_ingest(force=True))
    else:
        asyncio.run(run_ingest(force=False))
