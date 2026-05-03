# -*- coding: utf-8 -*-
from __future__ import annotations

import hashlib
import os
import sqlite3
from typing import List, Optional


class MetadataStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            PRAGMA journal_mode=WAL;

            CREATE TABLE IF NOT EXISTS documents (
                doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL UNIQUE,
                mtime REAL NOT NULL,
                size INTEGER NOT NULL,
                sha1 TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id INTEGER PRIMARY KEY,
                doc_id INTEGER NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(doc_id) REFERENCES documents(doc_id)
            );

            CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON chunks(doc_id);
            CREATE INDEX IF NOT EXISTS idx_documents_path ON documents(path);
            """
        )
        self.conn.commit()

    @staticmethod
    def file_sha1(path: str) -> str:
        h = hashlib.sha1()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def get_document(self, path: str) -> Optional[sqlite3.Row]:
        cur = self.conn.execute("SELECT * FROM documents WHERE path = ?", (path,))
        return cur.fetchone()

    def upsert_document(self, path: str, mtime: float, size: int, sha1: str) -> int:
        row = self.get_document(path)
        if row:
            self.conn.execute(
                "UPDATE documents SET mtime=?, size=?, sha1=? WHERE path=?",
                (mtime, size, sha1, path),
            )
            self.conn.commit()
            return int(row["doc_id"])
        cur = self.conn.execute(
            "INSERT INTO documents(path, mtime, size, sha1) VALUES (?, ?, ?, ?)",
            (path, mtime, size, sha1),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def delete_chunks_for_doc(self, doc_id: int) -> None:
        self.conn.execute("DELETE FROM chunks WHERE doc_id = ?", (doc_id,))
        self.conn.commit()

    def insert_chunk(self, chunk_id: int, doc_id: int, start_line: int, end_line: int, text: str) -> int:
        self.conn.execute(
            "INSERT OR REPLACE INTO chunks(chunk_id, doc_id, start_line, end_line, text) VALUES (?, ?, ?, ?, ?)",
            (chunk_id, doc_id, start_line, end_line, text),
        )
        self.conn.commit()
        return chunk_id

    def get_chunks_by_ids(self, chunk_ids: List[int]) -> List[dict]:
        if not chunk_ids:
            return []
        placeholders = ",".join("?" * len(chunk_ids))
        cur = self.conn.execute(
            f"SELECT c.*, d.path FROM chunks c JOIN documents d ON c.doc_id = d.doc_id WHERE c.chunk_id IN ({placeholders})",
            chunk_ids,
        )
        rows = {int(row["chunk_id"]): dict(row) for row in cur.fetchall()}
        return [rows[cid] for cid in chunk_ids if cid in rows]

    def count_chunks(self) -> int:
        cur = self.conn.execute("SELECT COUNT(*) FROM chunks")
        return int(cur.fetchone()[0])

    def close(self) -> None:
        self.conn.close()
