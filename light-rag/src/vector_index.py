# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from typing import List, Tuple

import hnswlib
import numpy as np


class VectorIndex:
    def __init__(
        self,
        index_path: str,
        dim: int = 512,
        max_elements: int = 100000,
        ef_construction: int = 200,
        M: int = 16,
        ef_search: int = 50,
    ) -> None:
        self.index_path = index_path
        self.dim = dim
        self.max_elements = max_elements
        self.ef_construction = ef_construction
        self.M = M
        self.ef_search = ef_search
        self.index: hnswlib.Index | None = None
        self._next_id = 0
        os.makedirs(os.path.dirname(index_path), exist_ok=True)

    def init_index(self) -> None:
        self.index = hnswlib.Index(space="cosine", dim=self.dim)
        self.index.init_index(max_elements=self.max_elements, ef_construction=self.ef_construction, M=self.M)
        self.index.set_ef(self.ef_search)
        self._next_id = 0

    def load(self) -> bool:
        if not os.path.exists(self.index_path):
            return False
        try:
            self.index = hnswlib.Index(space="cosine", dim=self.dim)
            self.index.load_index(self.index_path, max_elements=self.max_elements)
            self.index.set_ef(self.ef_search)
            self._next_id = int(self.index.get_current_count())
            return True
        except Exception:
            self.index = None
            return False

    def save(self) -> None:
        if self.index is not None:
            self.index.save_index(self.index_path)

    def add_vectors(self, vectors: np.ndarray) -> List[int]:
        if self.index is None:
            raise RuntimeError("Index not initialized")
        n = int(vectors.shape[0])
        if n == 0:
            return []
        ids = list(range(self._next_id, self._next_id + n))
        self.index.add_items(vectors.astype(np.float32), ids)
        self._next_id += n
        return ids

    def search(self, query: np.ndarray, k: int = 5) -> Tuple[List[int], List[float]]:
        if self.index is None:
            raise RuntimeError("Index not initialized")
        if query.ndim == 1:
            query = query.reshape(1, -1)
        current = int(self.index.get_current_count())
        if current == 0:
            return [], []
        k = min(k, current)
        labels, distances = self.index.knn_query(query.astype(np.float32), k=k)
        return labels[0].tolist(), distances[0].tolist()

    def get_current_count(self) -> int:
        return self._next_id if self.index is not None else 0
