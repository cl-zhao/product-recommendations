# -*- coding: utf-8 -*-
from __future__ import annotations

import glob
import os
from typing import List

from .chunker import chunk_markdown
from .embedder import BGEEmbedder
from .markdown_loader import load_markdown
from .metadata_store import MetadataStore
from .vector_index import VectorIndex


class Indexer:
    def __init__(
        self,
        embedder: BGEEmbedder,
        meta_store: MetadataStore,
        vector_index: VectorIndex,
        chunk_size: int = 400,
        chunk_overlap: int = 80,
        batch_size: int = 16,
    ) -> None:
        self.embedder = embedder
        self.meta_store = meta_store
        self.vector_index = vector_index
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.batch_size = batch_size

    def _embed_texts(self, texts: List[str]):
        vectors = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            arr = self.embedder.embed_batch(batch)
            vectors.append(arr)
        if not vectors:
            import numpy as np
            return np.empty((0, self.vector_index.dim), dtype='float32')
        import numpy as np
        return np.vstack(vectors)

    def index_file(self, path: str) -> int:
        path = os.path.abspath(path)
        stat = os.stat(path)
        mtime = stat.st_mtime
        size = stat.st_size
        sha1 = MetadataStore.file_sha1(path)

        existing = self.meta_store.get_document(path)
        if existing and existing["sha1"] == sha1:
            return 0

        doc = load_markdown(path)
        chunks = chunk_markdown(doc, self.chunk_size, self.chunk_overlap)
        if not chunks:
            return 0

        if existing:
            self.meta_store.delete_chunks_for_doc(int(existing["doc_id"]))
        doc_id = self.meta_store.upsert_document(path, mtime, size, sha1)

        texts = [c["text"] for c in chunks]
        vectors = self._embed_texts(texts)
        chunk_ids = self.vector_index.add_vectors(vectors)

        for chunk_id, chunk in zip(chunk_ids, chunks):
            self.meta_store.insert_chunk(
                chunk_id=chunk_id,
                doc_id=doc_id,
                start_line=int(chunk["start_line"]),
                end_line=int(chunk["end_line"]),
                text=chunk["text"],
            )
        return len(chunks)

    def index_directory(self, root: str, pattern: str = "*.md") -> int:
        files = sorted(glob.glob(os.path.join(root, "**", pattern), recursive=True))
        total = 0
        for f in files:
            try:
                total += self.index_file(f)
            except Exception as e:
                print(f"Failed to index {f}: {e}")
        return total
