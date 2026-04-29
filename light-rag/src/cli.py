# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

from .config import Config
from .embedder import BGEEmbedder
from .indexer import Indexer
from .metadata_store import MetadataStore
from .searcher import Searcher
from .vector_index import VectorIndex


def build_embedder(config: Config) -> BGEEmbedder:
    return BGEEmbedder(
        model_path=config.model_path,
        tokenizer_path=config.tokenizer_path,
        max_length=config.model_max_length,
        intra_threads=config.intra_threads,
        inter_threads=config.inter_threads,
    )


def cmd_index(args):
    config = Config.load(args.config)
    embedder = build_embedder(config)
    meta_store = MetadataStore(config.meta_db_path)
    vector_index = VectorIndex(config.index_path, dim=config.vector_dim)
    if not vector_index.load():
        vector_index.init_index()
    indexer = Indexer(
        embedder=embedder,
        meta_store=meta_store,
        vector_index=vector_index,
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        batch_size=config.batch_size,
    )

    if args.file:
        count = indexer.index_file(args.file)
    elif args.dir:
        count = indexer.index_directory(args.dir)
    else:
        count = indexer.index_directory(config.docs_dir)

    vector_index.save()
    output = {
        "ok": True,
        "chunks_indexed": count,
        "index_size": vector_index.get_current_count(),
        "meta_chunks": meta_store.count_chunks(),
    }
    print(json.dumps(output, ensure_ascii=False))


def cmd_search(args):
    config = Config.load(args.config)
    embedder = build_embedder(config)
    meta_store = MetadataStore(config.meta_db_path)
    vector_index = VectorIndex(config.index_path, dim=config.vector_dim)
    if not vector_index.load():
        print(json.dumps({"ok": False, "error": "Index not found. Run 'index' first."}, ensure_ascii=False))
        sys.exit(1)
    searcher = Searcher(embedder, meta_store, vector_index)
    results = searcher.search(args.query, top_k=args.top_k or config.default_top_k)
    print(json.dumps({"ok": True, "query": args.query, "results": [r.to_dict() for r in results]}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Light RAG CLI")
    parser.add_argument("--config", "-c", default="config/config.yaml", help="Config file path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="Build or update index")
    index_parser.add_argument("--file", "-f", help="Index a single file")
    index_parser.add_argument("--dir", "-d", help="Index a directory")
    index_parser.set_defaults(func=cmd_index)

    search_parser = subparsers.add_parser("search", help="Search the index")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--top-k", "-k", type=int, default=None, help="Number of results")
    search_parser.set_defaults(func=cmd_search)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
