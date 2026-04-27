# 轻量向量检索服务实现清单（适配 OpenClaw）

> 目标：替代 qmd 的中文检索能力  
> 方案：**bge-small-zh-v1.5（ONNX 量化） + hnswlib + sqlite**  
> 特点：**轻依赖、低内存、纯 CPU、可 CLI 调用、可选本地 HTTP**

---

## 1. 环境准备

### Python 版本要求

**推荐：Python 3.10 ~ 3.11**

当前环境已确认：**Python 3.11.6** ✅

---

### 推荐安装方式

**推荐：`python3 -m venv` 虚拟环境**

```bash
cd /root/.openclaw/workspace
python3 -m venv light-rag-venv
source light-rag-venv/bin/activate
```

---

### requirements.txt

```txt
numpy==1.26.4
hnswlib==0.8.0
onnxruntime==1.18.1
tokenizers==0.19.1
transformers==4.44.2
PyYAML==6.0.2
Flask==3.0.3  # 可选，仅用于 HTTP API
```

---

## 2. 目录结构

```text
light-rag/
├── README.md
├── requirements.txt
├── config/
│   └── config.yaml
├── models/
│   └── bge-small-zh-v1.5/
│       ├── model.onnx
│       ├── tokenizer.json
│       ├── config.json
│       └── ...
├── data/
│   ├── docs/                 # 待索引 markdown 文档根目录
│   ├── index/
│   │   ├── vectors.hnsw      # HNSW 索引文件
│   │   ├── meta.db           # sqlite 元数据
│   │   └── state.json        # 索引版本/维度/统计信息
│   └── cache/
├── logs/
│   └── app.log
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── embedder.py           # Embedding 模块
│   ├── markdown_loader.py    # Markdown 解析
│   ├── chunker.py            # Chunk 策略
│   ├── metadata_store.py     # SQLite 元数据
│   ├── vector_index.py       # HNSW 索引
│   ├── indexer.py            # 索引构建
│   ├── searcher.py           # 检索
│   ├── api.py                # HTTP API（可选）
│   └── cli.py                # CLI 入口
└── scripts/
    ├── bootstrap.sh
    ├── build_index.sh
    └── search.sh
```

---

## 3. 核心模块代码

### A. Embedding 模块 (`src/embedder.py`)

```python
# src/embedder.py
from __future__ import annotations

import os
from typing import List

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


class EmbeddingError(Exception):
    pass


class BGEEmbedder:
    def __init__(
        self,
        model_path: str,
        tokenizer_path: str,
        max_length: int = 512,
        normalize: bool = True,
        intra_threads: int = 2,
        inter_threads: int = 1,
    ) -> None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ONNX model not found: {model_path}")
        if not os.path.exists(tokenizer_path):
            raise FileNotFoundError(f"Tokenizer not found: {tokenizer_path}")

        self.tokenizer = Tokenizer.from_file(tokenizer_path)
        self.max_length = max_length
        self.normalize = normalize

        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = intra_threads
        sess_options.inter_op_num_threads = inter_threads
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        self.session = ort.InferenceSession(
            model_path,
            sess_options=sess_options,
            providers=["CPUExecutionProvider"],
        )

        self.input_names = [x.name for x in self.session.get_inputs()]
        self.output_name = self.session.get_outputs()[0].name

    def _tokenize(self, texts: List[str]) -> dict:
        input_ids = []
        attention_mask = []

        for text in texts:
            if not isinstance(text, str):
                raise EmbeddingError("Input text must be str")

            text = text.strip()
            if not text:
                text = " "

            enc = self.tokenizer.encode(text)
            ids = enc.ids[: self.max_length]
            mask = [1] * len(ids)

            pad_len = self.max_length - len(ids)
            if pad_len > 0:
                ids += [0] * pad_len
                mask += [0] * pad_len

            input_ids.append(ids)
            attention_mask.append(mask)

        return {
            "input_ids": np.array(input_ids, dtype=np.int64),
            "attention_mask": np.array(attention_mask, dtype=np.int64),
        }

    def _mean_pooling(self, last_hidden_state: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        mask = attention_mask[..., None].astype(np.float32)
        masked = last_hidden_state * mask
        summed = masked.sum(axis=1)
        counts = np.clip(mask.sum(axis=1), a_min=1e-9, a_max=None)
        emb = summed / counts
        return emb

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 512), dtype=np.float32)

        try:
            inputs = self._tokenize(texts)
            outputs = self.session.run([self.output_name], inputs)[0]
            emb = self._mean_pooling(outputs, inputs["attention_mask"]).astype(np.float32)

            if self.normalize:
                norms = np.linalg.norm(emb, axis=1, keepdims=True)
                emb = emb / np.clip(norms, 1e-12, None)

            return emb
        except Exception as e:
            raise EmbeddingError(f"embed_batch failed: {e}") from e

    def embed_one(self, text: str) -> np.ndarray:
        vectors = self.embed_batch([text])
        if vectors.shape[0] == 0:
            raise EmbeddingError("empty embedding result")
        return vectors[0]
```

---

### B. Markdown 解析 (`src/markdown_loader.py`)

```python
# src/markdown_loader.py
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

        # 去图片
        line = re.sub(r"!\[.*?\]\(.*?\)", " ", line)
        # 链接转文字
        line = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", line)
        # markdown 标记简化
        line = re.sub(r"^[>#\-\*\+\s]+", "", line)
        line = re.sub(r"`([^`]*)`", r"\1", line)
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            cleaned_lines.append(line)
            line_map.append(idx)

    return {
        "path": os.path.abspath(path),
        "lines": cleaned_lines,
        "line_map": line_map,
    }
```

---

### C. Chunk 策略 (`src/chunker.py`)

```python
# src/chunker.py
from __future__ import annotations

from typing import Dict, List


def chunk_markdown(doc: Dict, chunk_size: int = 400, overlap: int = 80) -> List[Dict]:
    """按字符长度切分，适合中文场景"""
    lines = doc["lines"]
    line_map = doc["line_map"]
    path = doc["path"]

    chunks: List[Dict] = []
    buffer = []
    buffer_len = 0
    start_line = None

    def flush():
        nonlocal buffer, buffer_len, start_line
        if not buffer:
            return

        text = "".join(buffer).strip()
        if text:
            chunks.append({
                "path": path,
                "start_line": start_line,
                "end_line": current_end_line,
                "text": text,
            })

        if overlap > 0 and text:
            keep = text[-overlap:]
            buffer = [keep]
            buffer_len = len(keep)
            start_line = current_end_line
        else:
            buffer = []
            buffer_len = 0
            start_line = None

    current_end_line = 0

    for i, line in enumerate(lines):
        ln = line_map[i]
        current_end_line = ln

        if start_line is None:
            start_line = ln

        piece = line + "\n"
        if buffer_len + len(piece) > chunk_size and buffer:
            flush()
            if start_line is None:
                start_line = ln

        buffer.append(piece)
        buffer_len += len(piece)

    if buffer:
        flush()

    return chunks
```

---

### D. SQLite 元数据存储 (`src/metadata_store.py`)

```python
# src/metadata_store.py
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
        self.conn.executescript("""
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
        """)
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
            return row["doc_id"]

        cur = self.conn.execute(
            "INSERT INTO documents(path, mtime, size, sha1) VALUES (?, ?, ?, ?)",
            (path, mtime, size, sha1),
        )
        self.conn.commit()
        return cur.lastrowid

    def delete_chunks_for_doc(self, doc_id: int) -> None:
        self.conn.execute("DELETE FROM chunks WHERE doc_id = ?", (doc_id,))
        self.conn.commit()

    def insert_chunk(self, doc_id: int, start_line: int, end_line: int, text: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO chunks(doc_id, start_line, end_line, text) VALUES (?, ?, ?, ?)",
            (doc_id, start_line, end_line, text),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_chunks_by_ids(self, chunk_ids: List[int]) -> List[dict]:
        if not chunk_ids:
            return []
        placeholders = ",".join("?" * len(chunk_ids))
        cur = self.conn.execute(
            f"SELECT c.*, d.path FROM chunks c JOIN documents d ON c.doc_id = d.doc_id WHERE c.chunk_id IN ({placeholders})",
            chunk_ids,
        )
        return [dict(row) for row in cur.fetchall()]

    def close(self) -> None:
        self.conn.close()
```

---

### E. HNSW 向量索引 (`src/vector_index.py`)

```python
# src/vector_index.py
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
    ) -> None:
        self.index_path = index_path
        self.dim = dim
        self.max_elements = max_elements
        self.ef_construction = ef_construction
        self.M = M
        self.index = None
        self._next_id = 0

        os.makedirs(os.path.dirname(index_path), exist_ok=True)

    def init_index(self) -> None:
        self.index = hnswlib.Index(space="cosine", dim=self.dim)
        self.index.init_index(max_elements=self.max_elements, ef_construction=self.ef_construction, M=self.M)
        self._next_id = 0

    def load(self) -> bool:
        if not os.path.exists(self.index_path):
            return False
        try:
            self.index = hnswlib.Index(space="cosine", dim=self.dim)
            self.index.load_index(self.index_path)
            self._next_id = self.index.get_current_count()
            return True
        except Exception:
            return False

    def save(self) -> None:
        if self.index:
            self.index.save_index(self.index_path)

    def add_vectors(self, vectors: np.ndarray) -> List[int]:
        if self.index is None:
            raise RuntimeError("Index not initialized")

        n = vectors.shape[0]
        ids = list(range(self._next_id, self._next_id + n))
        self.index.add_items(vectors, ids)
        self._next_id += n
        return ids

    def search(self, query: np.ndarray, k: int = 5) -> Tuple[List[int], List[float]]:
        if self.index is None:
            raise RuntimeError("Index not initialized")

        if query.ndim == 1:
            query = query.reshape(1, -1)

        labels, distances = self.index.knn_query(query, k=k)
        return labels[0].tolist(), distances[0].tolist()

    def get_current_count(self) -> int:
        return self._next_id if self.index else 0
```

---

### F. 索引构建 (`src/indexer.py`)

```python
# src/indexer.py
from __future__ import annotations

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
    ) -> None:
        self.embedder = embedder
        self.meta_store = meta_store
        self.vector_index = vector_index
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def index_file(self, path: str) -> int:
        """索引单个文件，返回 chunk 数量"""
        path = os.path.abspath(path)
        
        # 检查是否需要更新
        stat = os.stat(path)
        mtime = stat.st_mtime
        size = stat.st_size
        sha1 = MetadataStore.file_sha1(path)
        
        existing = self.meta_store.get_document(path)
        if existing and existing["sha1"] == sha1:
            return 0  # 无变化

        # 解析 markdown
        doc = load_markdown(path)
        chunks = chunk_markdown(doc, self.chunk_size, self.chunk_overlap)

        if not chunks:
            return 0

        # 删除旧的 chunks
        if existing:
            self.meta_store.delete_chunks_for_doc(existing["doc_id"])

        # 更新文档记录
        doc_id = self.meta_store.upsert_document(path, mtime, size, sha1)

        # Embedding
        texts = [c["text"] for c in chunks]
        vectors = self.embedder.embed_batch(texts)

        # 添加到向量索引
        chunk_ids = self.vector_index.add_vectors(vectors)

        # 存储元数据
        for chunk_id, chunk in zip(chunk_ids, chunks):
            self.meta_store.insert_chunk(
                doc_id, chunk["start_line"], chunk["end_line"], chunk["text"]
            )

        return len(chunks)

    def index_directory(self, root: str, pattern: str = "*.md") -> int:
        """索引目录下所有 markdown 文件"""
        import glob
        files = glob.glob(os.path.join(root, "**", pattern), recursive=True)
        total = 0
        for f in files:
            try:
                total += self.index_file(f)
            except Exception as e:
                print(f"Failed to index {f}: {e}")
        return total
```

---

### G. 检索 (`src/searcher.py`)

```python
# src/searcher.py
from __future__ import annotations

from typing import List

import numpy as np

from .embedder import BGEEmbedder
from .metadata_store import MetadataStore
from .vector_index import VectorIndex


class SearchResult:
    def __init__(self, path: str, start_line: int, end_line: int, text: str, score: float):
        self.path = path
        self.start_line = start_line
        self.end_line = end_line
        self.text = text
        self.score = score

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

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        # Query embedding
        query_vec = self.embedder.embed_one(query)

        # 向量检索
        chunk_ids, scores = self.vector_index.search(query_vec, k=top_k)

        if not chunk_ids:
            return []

        # 获取元数据
        chunks = self.meta_store.get_chunks_by_ids(chunk_ids)
        
        # 组装结果
        results = []
        for chunk, score in zip(chunks, scores):
            results.append(SearchResult(
                path=chunk["path"],
                start_line=chunk["start_line"],
                end_line=chunk["end_line"],
                text=chunk["text"],
                score=score,
            ))

        return results
```

---

### H. CLI 入口 (`src/cli.py`)

```python
# src/cli.py
#!/usr/bin/env python3
import argparse
import json
import sys

from .config import Config
from .embedder import BGEEmbedder
from .indexer import Indexer
from .metadata_store import MetadataStore
from .searcher import Searcher
from .vector_index import VectorIndex


def cmd_index(args):
    config = Config.load(args.config)
    
    embedder = BGEEmbedder(
        model_path=config.model_path,
        tokenizer_path=config.tokenizer_path,
    )
    
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
    )
    
    if args.file:
        count = indexer.index_file(args.file)
    elif args.dir:
        count = indexer.index_directory(args.dir)
    else:
        count = indexer.index_directory(config.docs_dir)
    
    vector_index.save()
    
    print(json.dumps({"ok": True, "chunks_indexed": count}))


def cmd_search(args):
    config = Config.load(args.config)
    
    embedder = BGEEmbedder(
        model_path=config.model_path,
        tokenizer_path=config.tokenizer_path,
    )
    
    meta_store = MetadataStore(config.meta_db_path)
    
    vector_index = VectorIndex(config.index_path, dim=config.vector_dim)
    if not vector_index.load():
        print(json.dumps({"ok": False, "error": "Index not found. Run 'index' first."}))
        sys.exit(1)
    
    searcher = Searcher(embedder, meta_store, vector_index)
    results = searcher.search(args.query, top_k=args.top_k)
    
    output = {
        "ok": True,
        "query": args.query,
        "results": [r.to_dict() for r in results],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Light RAG CLI")
    parser.add_argument("--config", "-c", default="config/config.yaml", help="Config file path")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # index 命令
    index_parser = subparsers.add_parser("index", help="Build or update index")
    index_parser.add_argument("--file", "-f", help="Index a single file")
    index_parser.add_argument("--dir", "-d", help="Index a directory")
    index_parser.set_defaults(func=cmd_index)
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="Search the index")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of results")
    search_parser.set_defaults(func=cmd_search)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
```

---

### I. 配置管理 (`src/config.py`)

```python
# src/config.py
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

    @classmethod
    def load(cls, path: str) -> "Config":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        base_dir = os.path.dirname(os.path.dirname(path))
        
        return cls(
            model_path=os.path.join(base_dir, data.get("model_path", "models/bge-small-zh-v1.5/model.onnx")),
            tokenizer_path=os.path.join(base_dir, data.get("tokenizer_path", "models/bge-small-zh-v1.5/tokenizer.json")),
            index_path=os.path.join(base_dir, data.get("index_path", "data/index/vectors.hnsw")),
            meta_db_path=os.path.join(base_dir, data.get("meta_db_path", "data/index/meta.db")),
            docs_dir=os.path.join(base_dir, data.get("docs_dir", "data/docs")),
            vector_dim=data.get("vector_dim", 512),
            chunk_size=data.get("chunk_size", 400),
            chunk_overlap=data.get("chunk_overlap", 80),
            default_top_k=data.get("default_top_k", 5),
        )
```

---

## 4. 配置文件 (`config/config.yaml`)

```yaml
# 模型配置
model_path: models/bge-small-zh-v1.5/model.onnx
tokenizer_path: models/bge-small-zh-v1.5/tokenizer.json

# 索引配置
index_path: data/index/vectors.hnsw
meta_db_path: data/index/meta.db
docs_dir: data/docs

# 向量维度（bge-small-zh-v1.5 是 512）
vector_dim: 512

# Chunk 策略
chunk_size: 400      # 中文字符数
chunk_overlap: 80    # overlap 字符数

# 检索配置
default_top_k: 5
```

---

## 5. 部署步骤

### Step 1: 创建项目目录

```bash
cd /root/.openclaw/workspace
mkdir -p light-rag/{config,models/bge-small-zh-v1.5,data/{docs,index,cache},logs,src,scripts}
touch light-rag/src/__init__.py
```

### Step 2: 创建虚拟环境

```bash
cd /root/.openclaw/workspace/light-rag
python3 -m venv venv
source venv/bin/activate
```

### Step 3: 安装依赖

```bash
pip install -r requirements.txt
```

### Step 4: 下载模型

从 HuggingFace 下载 bge-small-zh-v1.5 并转换为 ONNX：

```bash
# 下载原始模型
pip install optimum[onnx]
python -c "
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

model_id = 'BAAI/bge-small-zh-v1.5'
save_path = 'models/bge-small-zh-v1.5'

model = ORTModelForFeatureExtraction.from_pretrained(model_id, export=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)

model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
print('Model saved to', save_path)
"
```

### Step 5: 准备文档

```bash
# 链接或复制你的 markdown 文档
ln -s /root/.openclaw/workspace/memory data/docs/memory
```

### Step 6: 构建索引

```bash
python -m src.cli index
```

### Step 7: 测试检索

```bash
python -m src.cli search "模型使用策略" -k 5
```

---

## 6. 与 OpenClaw 集成

### 推荐方案：CLI + JSON 输出

OpenClaw 通过 `exec` 调用检索脚本，输出 JSON 格式。

#### 示例调用

```bash
/root/.openclaw/workspace/light-rag/venv/bin/python \
  -m src.cli search "模型使用策略 GLM MiniMax" -k 5 \
  --config /root/.openclaw/workspace/light-rag/config/config.yaml
```

#### 输出格式

```json
{
  "ok": true,
  "query": "模型使用策略 GLM MiniMax",
  "results": [
    {
      "path": "/root/.openclaw/workspace/memory/model-policy.md",
      "start_line": 1,
      "end_line": 25,
      "text": "# 模型使用策略\n\n...",
      "score": 0.85
    }
  ]
}
```

---

### 可选：本地 HTTP API

如果需要常驻服务，可以启动 Flask API：

```python
# src/api.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# ... 初始化 embedder, meta_store, vector_index, searcher ...

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "")
    top_k = data.get("top_k", 5)
    
    results = searcher.search(query, top_k)
    return jsonify({
        "ok": True,
        "query": query,
        "results": [r.to_dict() for r in results],
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5100)
```

启动：
```bash
python -m src.api
```

---

## 7. 运维建议

### 索引更新策略

- **定时更新**：cron 每小时/每天检查文件变化
- **触发式更新**：文件变更时触发索引更新

```bash
# cron 示例
0 * * * * /root/.openclaw/workspace/light-rag/venv/bin/python -m src.cli index
```

### 日志

在 `config.yaml` 中配置日志级别，日志输出到 `logs/app.log`。

### 备份

定期备份 `data/index/` 目录。

### 性能调优

1. **减少 chunk 大小** 可以提高精度但增加索引数量
2. **增加 ef_construction** 可以提高索引质量但增加构建时间
3. **调整 intra_threads** 根据 CPU 核心数

---

## 8. 文件清单

```
light-rag/
├── config/config.yaml           # 配置文件
├── requirements.txt             # Python 依赖
├── src/
│   ├── __init__.py
│   ├── config.py                # 配置加载
│   ├── embedder.py              # Embedding 模块
│   ├── markdown_loader.py       # Markdown 解析
│   ├── chunker.py               # Chunk 策略
│   ├── metadata_store.py        # SQLite 元数据
│   ├── vector_index.py          # HNSW 索引
│   ├── indexer.py               # 索引构建
│   ├── searcher.py              # 检索
│   ├── cli.py                   # CLI 入口
│   └── api.py                   # HTTP API（可选）
├── models/bge-small-zh-v1.5/    # 模型文件
├── data/
│   ├── docs/                    # 待索引文档
│   └── index/                   # 索引数据
└── logs/                        # 日志
```

---

## 资源预估

| 项目 | 占用 |
|------|------|
| 模型内存 | ~150-350MB |
| 索引（1万 chunk） | ~50MB |
| 索引（10万 chunk） | ~250MB |
| 查询延迟 | 80-250ms |
| 首次加载 | 2-8s |

**与 OpenClaw 共存：可行** ✅
