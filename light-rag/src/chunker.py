# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Dict, List


def chunk_markdown(doc: Dict, chunk_size: int = 400, overlap: int = 80) -> List[Dict]:
    lines = doc["lines"]
    line_map = doc["line_map"]
    path = doc["path"]

    chunks: List[Dict] = []
    buffer: List[str] = []
    buffer_len = 0
    start_line = None
    current_end_line = 0

    def flush() -> None:
        nonlocal buffer, buffer_len, start_line
        if not buffer:
            return
        text = "".join(buffer).strip()
        if text:
            chunks.append(
                {
                    "path": path,
                    "start_line": start_line,
                    "end_line": current_end_line,
                    "text": text,
                }
            )
        if overlap > 0 and text:
            keep = text[-overlap:]
            buffer = [keep]
            buffer_len = len(keep)
            start_line = current_end_line
        else:
            buffer = []
            buffer_len = 0
            start_line = None

    for i, line in enumerate(lines):
        ln = line_map[i]
        current_end_line = ln
        if start_line is None:
            start_line = ln
        piece = line + "\n"
        if buffer and buffer_len + len(piece) > chunk_size:
            flush()
            if start_line is None:
                start_line = ln
        buffer.append(piece)
        buffer_len += len(piece)

    if buffer:
        flush()
    return chunks
