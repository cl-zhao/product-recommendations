# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .embedder import BGEEmbedder
from .metadata_store import MetadataStore
from .vector_index import VectorIndex


@dataclass
class SearchResult:
    path: str
    start_line: int
    end_line: int
    text: str
    score: float

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "text": self.text,
            "score": self.score,
        }


class Searcher:
    def __init__(self, embedder: BGEEmbedder, meta_store: MetadataStore, vector_index: VectorIndex):
        self.embedder = embedder
        self.meta_store = meta_store
        self.vector_index = vector_index
        self.query_instruction = "为这个句子生成表示以用于检索相关文章："

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        query_text = f"{self.query_instruction}{query.strip()}"
        query_vec = self.embedder.embed_one(query_text)
        chunk_ids, distances = self.vector_index.search(query_vec, k=top_k)
        if not chunk_ids:
            return []
        chunks = self.meta_store.get_chunks_by_ids(chunk_ids)
        results: List[SearchResult] = []
        for chunk, distance in zip(chunks, distances):
            score = max(0.0, 1.0 - float(distance))
            results.append(
                SearchResult(
                    path=chunk["path"],
                    start_line=int(chunk["start_line"]),
                    end_line=int(chunk["end_line"]),
                    text=chunk["text"],
                    score=score,
                )
            )
        return results
