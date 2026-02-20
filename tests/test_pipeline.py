"""
Tests for pipeline/ module.

- test_processor: markdown scanning, hash detection, state management
- test_config: pipeline config values
- test_embeddings: hash embedding produces correct dimensions
"""

import pytest
from pathlib import Path


class TestMarkdownProcessor:
    def test_scan_empty_dir(self, tmp_path):
        """Scanning an empty directory returns no docs."""
        from pipeline.processors.markdown import MarkdownProcessor
        proc = MarkdownProcessor(content_dir=tmp_path)
        assert proc.scan() == []

    def test_scan_finds_md_files(self, tmp_path):
        """Scanning finds .md files."""
        (tmp_path / "test.md").write_text("# Hello\nWorld")
        from pipeline.processors.markdown import MarkdownProcessor
        proc = MarkdownProcessor(content_dir=tmp_path)
        docs = proc.scan()
        assert len(docs) == 1
        assert docs[0]["path"] == "test.md"
        assert docs[0]["changed"] is True

    def test_unchanged_detection(self, tmp_path):
        """Second scan detects unchanged files."""
        (tmp_path / "test.md").write_text("# Hello")
        from pipeline.processors.markdown import MarkdownProcessor

        proc1 = MarkdownProcessor(content_dir=tmp_path)
        proc1.scan()
        proc1.save_state()

        proc2 = MarkdownProcessor(content_dir=tmp_path)
        docs = proc2.scan()
        assert docs[0]["changed"] is False


class TestEmbeddings:
    @pytest.mark.asyncio
    async def test_hash_embedding_shape(self):
        """Hash embedding produces correct dimensions."""
        from pipeline.embeddings import hash_embedding
        result = await hash_embedding(["hello world"])
        assert result.shape == (1, 256)

    @pytest.mark.asyncio
    async def test_hash_embedding_deterministic(self):
        """Same input produces same embedding."""
        from pipeline.embeddings import hash_embedding
        import numpy as np
        r1 = await hash_embedding(["test"])
        r2 = await hash_embedding(["test"])
        assert np.allclose(r1, r2)
