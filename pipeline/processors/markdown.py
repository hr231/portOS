"""
Markdown document processor.

Handles scanning, hashing, and preparing .md/.txt files for ingestion.
Extend this or add new processors for other formats (PDF, HTML, etc.)
"""

import hashlib
import json
from pathlib import Path

from pipeline.config import CONTENT_DIR, INDEX_STATE_FILE, SUPPORTED_EXTENSIONS


class MarkdownProcessor:
    """Scans content directory, detects changes, yields docs ready for indexing."""

    def __init__(self, content_dir: Path = CONTENT_DIR):
        self.content_dir = content_dir
        self._prev_state = self._load_state()
        self._new_state = {}

    # ── Public API ────────────────────────────────────────────

    def scan(self) -> list[dict]:
        """
        Scan content directory and return list of docs.
        Each doc: { path, hash, text, changed }
        """
        docs = []
        for ext in SUPPORTED_EXTENSIONS:
            for filepath in sorted(self.content_dir.rglob(f"*{ext}")):
                text = filepath.read_text(encoding="utf-8").strip()
                if not text:
                    continue

                relative = str(filepath.relative_to(self.content_dir))
                file_hash = self._hash(filepath)
                changed = self._prev_state.get(relative) != file_hash

                self._new_state[relative] = file_hash
                docs.append({
                    "path": relative,
                    "hash": file_hash,
                    "text": text,
                    "changed": changed,
                })
        return docs

    def get_changed(self) -> list[dict]:
        """Return only new or modified documents."""
        return [d for d in self.scan() if d["changed"]]

    def get_all(self) -> list[dict]:
        """Return all documents (for force reindex)."""
        return self.scan()

    def save_state(self):
        """Persist the current index state (call after successful indexing)."""
        INDEX_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        INDEX_STATE_FILE.write_text(json.dumps(self._new_state, indent=2))

    def clear_state(self):
        """Delete saved state (forces full reindex next run)."""
        if INDEX_STATE_FILE.exists():
            INDEX_STATE_FILE.unlink()
            print("Index state cleared — next run will reindex everything.")

    # ── Internal ──────────────────────────────────────────────

    @staticmethod
    def _hash(filepath: Path) -> str:
        return hashlib.sha256(filepath.read_bytes()).hexdigest()

    @staticmethod
    def _load_state() -> dict:
        if INDEX_STATE_FILE.exists():
            return json.loads(INDEX_STATE_FILE.read_text())
        return {}
