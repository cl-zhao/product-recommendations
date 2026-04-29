# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    model_path: str
    tokenizer_path: str
    index_path: str
    meta_db_path: str
    docs_dir: str
    vector_dim: int = 512
    chunk_size: int = 400
    chunk_overlap: int = 80
    default_top_k: int = 5
    model_max_length: int = 512
    intra_threads: int = 2
    inter_threads: int = 1
    batch_size: int = 16

    @classmethod
    def load(cls, path: str) -> "Config":
        abs_path = os.path.abspath(path)
        with open(abs_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        base_dir = os.path.dirname(os.path.dirname(abs_path))

        def r(key: str, default: str) -> str:
            value = data.get(key, default)
            return value if os.path.isabs(value) else os.path.join(base_dir, value)

        return cls(
            model_path=r("model_path", "models/bge-small-zh-v1.5/model.onnx"),
            tokenizer_path=r("tokenizer_path", "models/bge-small-zh-v1.5/tokenizer.json"),
            index_path=r("index_path", "data/index/vectors.hnsw"),
            meta_db_path=r("meta_db_path", "data/index/meta.db"),
            docs_dir=r("docs_dir", "data/docs"),
            vector_dim=int(data.get("vector_dim", 512)),
            chunk_size=int(data.get("chunk_size", 400)),
            chunk_overlap=int(data.get("chunk_overlap", 80)),
            default_top_k=int(data.get("default_top_k", 5)),
            model_max_length=int(data.get("model_max_length", 512)),
            intra_threads=int(data.get("intra_threads", 2)),
            inter_threads=int(data.get("inter_threads", 1)),
            batch_size=int(data.get("batch_size", 16)),
        )
