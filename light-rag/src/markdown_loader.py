# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re
from typing import Dict, List


def load_markdown(path: str) -> Dict:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    cleaned_lines: List[str] = []
    line_map: List[int] = []
    code_block = False

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if line.strip().startswith("```"):
            code_block = not code_block
            continue
        if code_block:
            continue

        line = re.sub(r"!\[.*?\]\(.*?\)", " ", line)
        line = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", line)
        line = re.sub(r"^[>#\-\*\+\s]+", "", line)
        line = re.sub(r"`([^`]*)`", r"\1", line)
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            cleaned_lines.append(line)
            line_map.append(idx)

    return {"path": os.path.abspath(path), "lines": cleaned_lines, "line_map": line_map}
