# OpenClaw 记忆检索优化方案

## 📋 背景回顾

OpenClaw 当前使用 qmd 作为记忆检索后端，存在以下问题：
1. qmd 中文分词 bug 导致 fallback 到 Gemini
2. CPU 模式下 qmd embed 速度慢（~1.5分钟）
3. 需要手动创建 collection，配置复杂

**硬件约束**: 2核 CPU / 4GB 内存 / 60GB 磁盘 / 无 GPU / Linux OpenCloudOS

---

## 📦 方案列表

### 1. LightRAG (推荐)

**GitHub**: https://github.com/HKUDS/LightRAG  
**Stars**: ⭐ 5.2k+  
**最新更新**: 2025.11 (活跃)

#### 核心特性
- 轻量级 RAG 框架，支持本地部署
- 异构图索引 + 知识图谱增强检索
- 支持向量检索 + 关键词检索混合
- 支持多种存储后端：PostgreSQL / Neo4j / MongoDB
- 内置 Web UI 和 API 服务
- 支持 Ollama 模型调用
- 中文支持好

#### 硬件需求
- **CPU**: ✅ 2核完全够用
- **内存**: ✅ 4GB 足够（官方支持边缘设备）
- **存储**: ✅ 轻量级设计

#### 中文支持
- ✅ 原生支持中文分词和检索
- ✅ 有中文文档和社区

#### OpenClaw 集成难度
- ⭐ 低 - 提供 Python SDK (`pip install lightrag-hku`)
- 有 LangChain / LlamaIndex 集成
- 预计工作量：1-2 天

#### 优缺点
| ✅ 优点 | ❌ 缺点 |
|---------|---------|
| 维护活跃（每月更新） | 依赖 LLM 进行知识图谱提取 |
| 功能完整（RAG + KG） | 首次索引需要 LLM 调用 |
| 支持多种数据库后端 | 图谱构建需要一定时间 |
| 性能优秀（EMNLP 2025） | |

---

### 2. MiniRAG (轻量首选)

**GitHub**: https://github.com/HKUDS/MiniRAG  
**Stars**: ⭐ 1.3k+  
**最新更新**: 2025.02 (活跃)

#### 核心特性
- 专为小模型设计的极简 RAG 框架
- 异构图索引（不依赖复杂语义理解）
- 支持 10+ 异构图数据库（Neo4j, PostgreSQL, TiDB 等）
- 存储空间仅需传统 RAG 的 25%
- 支持 API & Docker 部署
- 中文优化

#### 硬件需求
- **CPU**: ✅ 极低功耗，2核绰绰有余
- **内存**: ✅ 4GB 轻松运行
- **存储**: ✅ 极轻量

#### 中文支持
- ✅ 专门针对中文优化
- ✅ 有中文 README

#### OpenClaw 集成难度
- ⭐ 很低 - `pip install minirag-hku`
- 基于 LightRAG，API 兼容
- 预计工作量：0.5-1 天

#### 优缺点
| ✅ 优点 | ❌ 缺点 |
|---------|---------|
| 极简设计，资源消耗低 | 较新，社区相对较小 |
| 适合边缘设备部署 | 功能比 LightRAG 少 |
| 性能优秀（小模型测试领先） | 需要小模型配合使用 |
| 支持 Docker 一键部署 | |

---

### 3. pgvector (传统数据库方案)

**GitHub**: https://github.com/pgvector/pgvector  
**Stars**: ⭐ 12k+  
**最新更新**: 2025.03 (持续维护)

#### 核心特性
- PostgreSQL 向量搜索扩展
- 支持精确和近似最近邻搜索
- 支持 L2 / 内积 / cosine / L1 距离
- 支持 HNSW 和 IVFFlat 索引
- ACID 兼容，可 JOIN 传统数据
- 任何语言都能通过 Postgres 客户端使用

#### 硬件需求
- **CPU**: ✅ 2核可用
- **内存**: ✅ 4GB 可运行（需调优）
- **存储**: ✅ 依赖 PostgreSQL

#### 中文支持
- ⚠️ 向量存储无语言限制
- ⚠️ 分词需配合其他工具（jieba）

#### OpenClaw 集成难度
- ⭐ 中等 - 需要安装 PostgreSQL 扩展
- Python SDK: `pip install pgvector`
- 预计工作量：1-2 天

#### 优缺点
| ✅ 优点 | ❌ 缺点 |
|---------|---------|
| 极其成熟，稳定可靠 | 需要额外安装 PostgreSQL |
| 与现有数据库集成 | 近似搜索精度调优复杂 |
| 社区庞大，文档丰富 | 无内置中文分词 |
| 免费开源 | 需要手动管理索引 |

---

### 4. ChromaDB (原型首选)

**GitHub**: https://github.com/chroma-core/chroma  
**Stars**: ⭐ 13k+  
**最新更新**: 2025 有重大更新（Rust 重写）

#### 核心特性
- 开源向量数据库
- Python-first 设计，API 极简（仅 4 个函数）
- 支持 LangChain / LlamaIndex 集成
- 内存模式 + 持久化模式
- 2025 年发布 Rust 重写版，性能提升 4x

#### 硬件需求
- **CPU**: ✅ 2核可用
- **内存**: ✅ 4GB 可运行
- **存储**: ✅ 本地文件存储

#### 中文支持
- ⚠️ 支持多语言 embedding
- ⚠️ 需配合 embedding 模型使用

#### OpenClaw 集成难度
- ⭐ 很低 - `pip install chromadb`
- LangChain 集成成熟
- 预计工作量：0.5 天

#### 优缺点
| ✅ 优点 | ❌ 缺点 |
|---------|---------|
| 极易上手，API 简洁 | 生产环境需额外配置 |
| 适合原型开发 | 分布式能力较弱 |
| LangChain/LlamaIndex 集成 | Rust 版本较新 |
| 支持 Docker 部署 | |

---

### 5. Qdrant (高性能方案)

**GitHub**: https://github.com/qdrant/qdrant  
**Stars**: ⭐ 16k+  
**最新更新**: 持续活跃

#### 核心特性
- Rust 编写的向量搜索引擎
- 高性能，低延迟
- 支持 Docker 一键部署
- 支持过滤查询
- 有云端版本（免费 tier）
- Python / Go / JS / Java / .NET 客户端

#### 硬件需求
- **CPU**: ✅ 2核可用
- **内存**: ✅ 4GB 可运行（推荐 8GB 优化）
- **存储**: ✅ 磁盘存储

#### 中文支持
- ⚠️ 向量存储无语言限制
- ⚠️ 需配合 embedding 模型

#### OpenClaw 集成难度
- ⭐ 中低 - Docker 部署 + Python SDK
- 预计工作量：1 天

#### 优缺点
| ✅ 优点 | ❌ 缺点 |
|---------|---------|
| 性能极高 | 资源需求相对较高 |
| 生产级稳定性 | 2核4G 需调优 |
| 过滤查询功能强 | 复杂度较高 |
| 文档完善 | |

---

## 🏆 推荐方案

### 首选：LightRAG + BGE-M3

| 维度 | 评分 |
|------|------|
| 中文支持 | ⭐⭐⭐⭐⭐ |
| 资源占用 | ⭐⭐⭐⭐ |
| 集成难度 | ⭐⭐⭐⭐⭐ |
| 维护活跃 | ⭐⭐⭐⭐⭐ |
| 文档质量 | ⭐⭐⭐⭐⭐ |

**推荐理由**：
1. **功能完整**：向量检索 + 知识图谱，语义理解更强
2. **中文优化**：异构图索引降低对中文分词的依赖
3. **后端灵活**：支持 PostgreSQL，无需额外数据库
4. **性能优秀**：EMNLP 2025 研究成果
5. **维护活跃**：月更，响应快

### 备选：MiniRAG + Jina-v2-zh

| 维度 | 评分 |
|------|------|
| 中文支持 | ⭐⭐⭐⭐⭐ |
| 资源占用 | ⭐⭐⭐⭐⭐ |
| 集成难度 | ⭐⭐⭐⭐⭐ |
| 维护活跃 | ⭐⭐⭐⭐ |
| 文档质量 | ⭐⭐⭐⭐ |

**备选理由**：
- 如果资源极度受限（< 2GB 内存）
- 如果追求极致简单
- 边缘设备部署场景

---

## 🔧 集成建议

### 方案一：LightRAG + BGE-M3（推荐）

```bash
# 1. 安装 LightRAG
pip install "lightrag-hku[api]"

# 2. 安装中文 embedding 模型
pip install flagembedding  # BGE-M3
# 或
pip install sentence-transformers  # Jina v2

# 3. 配置 .env 文件
# 参考 env.example 配置 LLM 和 embedding
```

**集成到 OpenClaw**:
```python
# 创建 memory 模块封装
from lightrag import LightRAG
from flagembedding import FlagModel

# 使用 BGE-M3 作为 embedding
model = FlagModel("BAAI/bge-m3", use_fp16=True)

# 初始化 LightRAG
rag = LightRAG(
    working_dir="./openclaw_memory",
    embedding_func=model.encode,
    # 使用 PostgreSQL 作为存储
)
```

**预计工作量**：1-2 天

---

### 方案二：pgvector + jieba

如果现有系统已有 PostgreSQL，这是最简单方案：

```bash
# 1. 安装 pgvector
# PostgreSQL 扩展安装略

# 2. Python 依赖
pip install pgvector psycopg2-binary jieba

# 3. 创建向量表
CREATE TABLE IF NOT EXISTS memory (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1024),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON memory USING hnsw (embedding vector_cosine_ops);
```

**预计工作量**：0.5-1 天

---

### Embedding 模型推荐

| 模型 | 向量维度 | 中文效果 | 资源需求 | 速度 |
|------|----------|----------|----------|------|
| **BGE-M3** | 1024 | ⭐⭐⭐⭐⭐ | 中等 | 中等 |
| Jina-v2-base-zh | 768 | ⭐⭐⭐⭐ | 较低 | 快 |
| BGE-base-zh-v1.5 | 768 | ⭐⭐⭐⭐ | 低 | 快 |
| mteb-zh-retrieval | 1024 | ⭐⭐⭐⭐⭐ | 中等 | 中等 |

**推荐 BGE-M3**：多语言 + 多功能 + 中文最优

---

## 📊 综合对比

| 方案 | 中文 | 2C4G | 维护 | 集成 | 推荐度 |
|------|------|------|------|------|--------|
| **LightRAG** | ✅✅✅✅✅ | ✅✅✅✅ | ✅✅✅✅✅ | ✅✅✅✅✅ | 🥇 |
| **MiniRAG** | ✅✅✅✅✅ | ✅✅✅✅✅ | ✅✅✅✅ | ✅✅✅✅✅ | 🥈 |
| pgvector | ✅✅ | ✅✅✅ | ✅✅✅✅✅ | ✅✅✅ | 🥉 |
| ChromaDB | ✅✅ | ✅✅✅ | ✅✅✅✅ | ✅✅✅✅ | - |
| Qdrant | ✅✅ | ✅✅✅ | ✅✅✅✅✅ | ✅✅✅✅ | - |

---

## 🚀 下一步行动

1. **测试 LightRAG**（推荐先用 Docker 快速体验）
2. **选择 embedding 模型**（BGE-M3 或 Jina-v2-zh）
3. **设计 OpenClaw 封装层**
4. **性能基准测试**

---

*Last updated: 2026-03-13*