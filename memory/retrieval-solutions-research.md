# 记忆检索方案调研报告

> 调研时间：2026-03-13
> 目标：寻找类似 qmd 的开源检索方案，重点关注轻量级、本地部署、CPU 友好、支持混合检索

---

## 一、本地混合检索引擎（BM25 + 向量）

### 1. Meilisearch

**项目信息**
- GitHub: https://github.com/meilisearch/meilisearch
- 官网: https://www.meilisearch.com
- 语言: Rust
- Star: 48k+

**核心功能**
- ✅ 混合检索（BM25 + 向量搜索）
- ✅ 内置 embedding 支持（支持本地或第三方）
- ✅ 自动查询扩展
- ✅ 拼写纠正和容错
- ✅ 多语言支持
- ✅ 实时索引

**硬件需求**
- CPU: 良好支持，无需 GPU
- 内存: 最低 2GB，推荐 4GB+
- 存储: SSD 推荐

**与 qmd 对比**
- ✅ 更成熟稳定，生产级方案
- ✅ 内置全文搜索（qmd 需要自己实现）
- ✅ 更好的文档和社区支持
- ❌ 不支持本地 GGUF 模型（需要外部 embedding 服务）
- ❌ 不是专门为 AI Agent 设计

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐ (4/5)
- 适合作为 Agent 的知识库检索后端
- 需要自己实现记忆管理层

---

### 2. Typesense

**项目信息**
- GitHub: https://github.com/typesense/typesense
- 官网: https://typesense.org
- 语言: C++
- Star: 22k+

**核心功能**
- ✅ 混合检索（BM25 + 向量）
- ✅ RRF (Reciprocal Rank Fusion) 融合算法
- ✅ 支持远程 embedding 模型
- ✅ 拼写纠正
- ✅ 地理位置搜索
- ✅ 分面搜索

**硬件需求**
- CPU: 优秀支持，无需 GPU
- 内存: 轻量级，1GB 即可运行
- 存储: 内存索引 + 磁盘持久化

**与 qmd 对比**
- ✅ 更轻量级
- ✅ 内存效率高
- ✅ 查询速度快（C++ 实现）
- ❌ embedding 支持不如 qmd 灵活
- ❌ 不支持本地 GGUF 模型

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐ (4/5)
- 适合资源受限环境
- 小规模 Agent 记忆检索

---

### 3. Quickwit

**项目信息**
- GitHub: https://github.com/quickwit-oss/quickwit
- 官网: https://quickwit.io
- 语言: Rust
- Star: 8k+

**核心功能**
- ✅ 基于 Tantivy（类似 Lucene）
- ✅ 云原生架构
- ✅ 对象存储友好
- ✅ 分布式搜索
- ✅ 日志和可观测性场景优化

**硬件需求**
- CPU: 支持良好
- 内存: 可配置，支持热缓存
- 存储: 对象存储优先

**与 qmd 对比**
- ✅ 更适合大规模数据
- ✅ 成本更低（对象存储）
- ❌ 不适合小规模本地使用
- ❌ 不是为 AI Agent 设计
- ❌ 缺少内置 embedding 支持

**适合 AI Agent 记忆检索**
- ⭐⭐ (2/5)
- 过于重量级
- 更适合日志分析场景

---

## 二、向量数据库/检索工具

### 4. Chroma

**项目信息**
- GitHub: https://github.com/chroma-core/chroma
- 官网: https://www.trychroma.com
- 语言: Python/Rust
- Star: 15k+

**核心功能**
- ✅ 纯向量数据库
- ✅ 支持全文搜索（BM25/SPLADE）
- ✅ 内存模式 + 持久化
- ✅ 自动 embedding
- ✅ 元数据过滤
- ✅ 与 LangChain/LlamaIndex 深度集成

**硬件需求**
- CPU: 完全支持，无需 GPU
- 内存: 轻量级，512MB 即可启动
- 存储: 支持磁盘持久化

**与 qmd 对比**
- ✅ 更简单的 API
- ✅ 开箱即用
- ✅ 社区活跃，生态丰富
- ❌ 性能不如专用搜索引擎
- ❌ 不支持混合检索的深度融合
- ❌ 缺少 query expansion

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐⭐ (5/5)
- **最推荐的向量数据库**
- 与 AI Agent 框架无缝集成
- Mem0 也使用 Chroma 作为后端

---

### 5. LanceDB

**项目信息**
- GitHub: https://github.com/lancedb/lancedb
- 官网: https://lancedb.com
- 语言: Rust
- Star: 5k+

**核心功能**
- ✅ 嵌入式向量数据库
- ✅ 无服务器架构
- ✅ 多模态支持（文本、图像、视频）
- ✅ Lance 列式格式
- ✅ 零拷贝读取
- ✅ 向量 + 全文混合搜索

**硬件需求**
- CPU: 完全支持
- 内存: 嵌入式，按需使用
- 存储: 磁盘优先，支持对象存储

**与 qmd 对比**
- ✅ 嵌入式设计，无服务器依赖
- ✅ 支持大规模多模态数据
- ✅ 成本低（磁盘存储）
- ❌ 功能相对新，生态不成熟
- ❌ 文档较少

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐ (4/5)
- 适合嵌入式场景
- 适合多模态 Agent

---

### 6. Qdrant

**项目信息**
- GitHub: https://github.com/qdrant/qdrant
- 官网: https://qdrant.io
- 语言: Rust
- Star: 21k+

**核心功能**
- ✅ 高性能向量数据库
- ✅ 混合检索（BM25 + 向量）
- ✅ FastEmbed 集成
- ✅ 丰富的过滤能力
- ✅ 分布式支持
- ✅ 混合 CPU/GPU 分区

**硬件需求**
- CPU: 优秀支持
- GPU: 可选加速（热数据 GPU，冷数据 CPU）
- 内存: 可配置缓存
- 存储: 磁盘 + 内存混合

**与 qmd 对比**
- ✅ 生产级稳定性
- ✅ 性能优异
- ✅ 混合检索支持好
- ❌ 部署相对复杂
- ❌ 资源消耗较大

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐ (4/5)
- 适合中大规模部署
- 需要高性能时首选

---

### 7. Milvus Lite

**项目信息**
- GitHub: https://github.com/milvus-io/milvus-lite
- 官网: https://milvus.io
- 语言: Go
- Star: 31k+ (Milvus 主项目)

**核心功能**
- ✅ Milvus 的轻量级版本
- ✅ 单机部署
- ✅ pip install 即可使用
- ✅ 向量 + 标量混合查询
- ✅ 与完整 Milvus API 兼容

**硬件需求**
- CPU: 完全支持
- 内存: 2GB+ 推荐
- 存储: 本地磁盘

**与 qmd 对比**
- ✅ 轻量级，易上手
- ✅ 可扩展到分布式
- ❌ 功能比完整版少
- ❌ 不支持混合检索（BM25）

**适合 AI Agent 记忆检索**
- ⭐⭐⭐ (3/5)
- 适合快速原型
- 不适合生产环境

---

## 三、AI Agent 记忆/检索方案

### 8. Mem0

**项目信息**
- GitHub: https://github.com/mem0ai/mem0
- 官网: https://mem0.ai
- 语言: Python
- Star: 25k+

**核心功能**
- ✅ **专为 AI Agent 设计的记忆层**
- ✅ 长期记忆 + 短期记忆
- ✅ 自动记忆提取和更新
- ✅ 用户/会话/Agent 级别隔离
- ✅ 支持多种向量数据库（Chroma, Qdrant, Pinecone 等）
- ✅ 与 LangChain/LlamaIndex/AutoGen 集成
- ✅ 自我改进能力

**硬件需求**
- CPU: 完全支持
- 内存: 取决于后端数据库
- 存储: 使用后端数据库

**与 qmd 对比**
- ✅ **专门为 Agent 设计**
- ✅ 记忆管理自动化
- ✅ 跨会话持久化
- ✅ 个性化支持
- ❌ 不是搜索引擎，是记忆层
- ❌ 依赖外部向量数据库

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐⭐ (5/5)
- **强烈推荐**
- 直接解决 Agent 记忆问题
- 可以与 qmd 或其他搜索引擎结合

---

### 9. Letta (原 MemGPT)

**项目信息**
- GitHub: https://github.com/letta-ai/letta
- 官网: https://www.letta.com
- 语言: Python
- Star: 12k+

**核心功能**
- ✅ **有状态的 AI Agent 框架**
- ✅ 自我改进记忆系统
- ✅ 多层记忆（核心 + 对话 + 归档）
- ✅ 自动记忆管理
- ✅ 跨模型可移植
- ✅ Letta Code（代码 Agent）

**硬件需求**
- CPU: 完全支持
- 内存: 依赖 LLM
- 存储: 本地数据库

**与 qmd 对比**
- ✅ 完整的 Agent 框架
- ✅ 自主记忆管理
- ✅ 学习和改进能力
- ❌ 不只是检索工具
- ❌ 学习曲线较陡

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐⭐ (5/5)
- **推荐用于构建 Agent**
- 提供完整的记忆解决方案
- 适合长期运行的 Agent

---

### 10. LangChain Memory

**项目信息**
- GitHub: https://github.com/langchain-ai/langchain
- 文档: https://python.langchain.com/docs/modules/memory/
- Star: 100k+

**核心功能**
- ✅ 多种记忆类型
  - ConversationBufferMemory
  - ConversationSummaryMemory
  - VectorStoreMemory
  - EntityMemory
- ✅ LangMem SDK（长期记忆）
- ✅ 与 LangChain 生态集成
- ✅ 灵活配置

**硬件需求**
- CPU: 完全支持
- 内存: 取决于实现
- 存储: 取决于后端

**与 qmd 对比**
- ✅ 生态最成熟
- ✅ 多种记忆策略
- ✅ 易于集成
- ❌ 需要自己组合
- ❌ 性能依赖实现

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐ (4/5)
- 适合使用 LangChain 的项目
- 需要额外配置

---

### 11. LlamaIndex Memory

**项目信息**
- GitHub: https://github.com/run-llama/llama_index
- 文档: https://docs.llamaindex.ai/
- Star: 37k+

**核心功能**
- ✅ Vector Memory（向量记忆）
- ✅ Chat Memory Buffer
- ✅ 与 RAG 深度集成
- ✅ 多种索引类型
- ✅ Agentic RAG

**硬件需求**
- CPU: 完全支持
- 内存: 取决于索引
- 存储: 取决于后端

**与 qmd 对比**
- ✅ RAG 优化好
- ✅ 记忆与检索结合
- ✅ 灵活的索引策略
- ❌ 需要 LLM 依赖

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐ (4/5)
- 适合 RAG 为主的 Agent
- 与 LlamaIndex 生态配合好

---

## 四、RAG 优化工具

### 12. BGE Reranker (BAAI)

**项目信息**
- GitHub: https://github.com/FlagOpen/FlagEmbedding
- HuggingFace: https://huggingface.co/BAAI/bge-reranker-base
- 开发者: 北京智源人工智能研究院

**核心功能**
- ✅ 多种模型大小
  - bge-reranker-base (小)
  - bge-reranker-large (中)
  - bge-reranker-v2-m3 (多语言，推荐)
- ✅ CPU 友好
- ✅ 多语言支持
- ✅ 高精度重排序

**硬件需求**
- **bge-reranker-base**
  - CPU: ✅ 完全支持，速度快
  - 内存: ~500MB
- **bge-reranker-v2-m3**
  - CPU: ✅ 支持，较慢
  - 内存: ~1.5GB
  - GPU: 可选加速

**与 qmd 对比**
- ✅ 专业 reranker，性能更好
- ✅ CPU 下可用
- ✅ 开源免费
- ❌ 需要额外集成
- ❌ qmd 已内置

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐⭐ (5/5)
- **强烈推荐**
- 提升检索精度明显
- CPU 下可用

---

### 13. Cohere Rerank

**项目信息**
- 官网: https://cohere.com/rerank
- API 文档: https://docs.cohere.com/docs/rerank

**核心功能**
- ✅ 云端 API
- ✅ 高质量重排序
- ✅ 多语言支持
- ✅ 易于使用

**硬件需求**
- 无本地需求（云端 API）
- 需要网络连接

**与 qmd 对比**
- ✅ 质量高
- ✅ 无需本地资源
- ❌ 需要付费 API
- ❌ 数据隐私问题
- ❌ 网络依赖

**适合 AI Agent 记忆检索**
- ⭐⭐⭐ (3/5)
- 适合对隐私要求不高的场景
- 快速原型

---

### 14. Query Expansion 工具

**方案 1: 使用本地 LLM**
- 工具: LocalAI, llama.cpp, Ollama
- 模型: Llama-3.2-1B-Instruct, Qwen2.5-3B
- 优点: 本地运行，隐私安全
- 缺点: CPU 下较慢（qmd 当前问题）

**方案 2: 使用小模型**
- 推荐: Flan-T5-small, Qwen2.5-0.5B
- 优点: 速度快，资源少
- 缺点: 扩展质量一般

**方案 3: 规则扩展**
- 同义词库
- WordNet
- 快速但效果有限

**适合 AI Agent 记忆检索**
- ⭐⭐⭐⭐ (4/5)
- 推荐：小模型 + 规则混合
- 平衡速度和质量

---

## 五、推荐方案组合

### 🥇 方案 1: Mem0 + Chroma + BGE Reranker

**适用场景**
- AI Agent 记忆管理
- 中小规模部署
- CPU 环境

**优势**
- ✅ 专门为 Agent 设计
- ✅ 轻量级，易部署
- ✅ 完全本地化
- ✅ 成本低

**架构**
```
User Query
  ↓
Mem0 (记忆管理)
  ↓
Chroma (向量检索)
  ↓
BGE Reranker (重排序)
  ↓
返回相关记忆
```

---

### 🥈 方案 2: Meilisearch + Mem0

**适用场景**
- 需要强大全文搜索
- 混合检索需求
- 知识库 + 记忆

**优势**
- ✅ 成熟的搜索引擎
- ✅ 混合检索性能好
- ✅ 文档完善
- ✅ 生产级稳定

**架构**
```
User Query
  ↓
Mem0 (Agent 记忆)
  ↓
Meilisearch (混合检索: BM25 + 向量)
  ↓
返回相关内容
```

---

### 🥉 方案 3: Letta + LanceDB

**适用场景**
- 构建有状态 Agent
- 长期记忆和自我改进
- 多模态数据

**优势**
- ✅ 完整的 Agent 框架
- ✅ 自主记忆管理
- ✅ 支持多模态
- ✅ 嵌入式，无服务器

**架构**
```
User Query
  ↓
Letta Agent (有状态)
  ↓
LanceDB (多模态存储)
  ↓
自我改进记忆系统
```

---

## 六、针对 qmd 的改进建议

### 当前问题
1. 只索引特定目录
2. CPU 下 query expansion 较慢
3. 需要更多检索方案选择

### 改进方案

**问题 1: 目录限制**
- 参考 Meilisearch 的多索引设计
- 支持动态添加数据源
- 参考 Mem0 的多租户隔离

**问题 2: Query Expansion 慢**
- 方案 A: 使用更小的模型（Qwen2.5-0.5B, Flan-T5-small）
- 方案 B: 缓存扩展结果
- 方案 C: 规则 + 模型混合
- 方案 D: 异步扩展

**问题 3: 检索方案单一**
- 集成 BGE Reranker（提升精度）
- 支持多种向量数据库后端（Chroma, Qdrant）
- 添加全文搜索支持（参考 Typesense）

---

## 七、快速开始建议

### 最小可行方案（MVP）

**如果只想快速尝试**
```python
# 使用 Chroma + BGE Reranker
import chromadb
from FlagEmbedding import FlagReranker

# 1. 初始化 Chroma
client = chromadb.Client()
collection = client.create_collection("memories")

# 2. 添加文档
collection.add(
    documents=["记忆内容1", "记忆内容2"],
    metadatas=[{"type": "fact"}, {"type": "event"}],
    ids=["id1", "id2"]
)

# 3. 检索
results = collection.query(
    query_texts=["查询内容"],
    n_results=10
)

# 4. 重排序
reranker = FlagReranker('BAAI/bge-reranker-base', use_fp16=False)
scores = reranker.compute_score([('查询内容', doc) for doc in results['documents'][0]])
```

### 生产级方案

**如果要构建生产系统**
1. 使用 **Meilisearch** 作为搜索引擎
2. 使用 **Mem0** 管理 Agent 记忆
3. 使用 **BGE Reranker** 提升精度
4. 使用 **Llama 3.2 1B** 做 query expansion（异步）

---

## 八、资源链接汇总

### 本地混合检索引擎
- Meilisearch: https://github.com/meilisearch/meilisearch
- Typesense: https://github.com/typesense/typesense
- Quickwit: https://github.com/quickwit-oss/quickwit

### 向量数据库
- Chroma: https://github.com/chroma-core/chroma
- LanceDB: https://github.com/lancedb/lancedb
- Qdrant: https://github.com/qdrant/qdrant
- Milvus Lite: https://github.com/milvus-io/milvus-lite

### AI Agent 记忆
- Mem0: https://github.com/mem0ai/mem0
- Letta: https://github.com/letta-ai/letta
- LangChain: https://github.com/langchain-ai/langchain
- LlamaIndex: https://github.com/run-llama/llama_index

### RAG 优化
- BGE Reranker: https://github.com/FlagOpen/FlagEmbedding
- Cohere Rerank: https://cohere.com/rerank

---

## 九、结论

### 最佳推荐

**如果目标是构建 AI Agent 记忆系统**
- 首选: **Mem0 + Chroma + BGE Reranker**
- 理由: 专为 Agent 设计，轻量级，CPU 友好

**如果目标是通用文档检索**
- 首选: **Meilisearch**
- 理由: 成熟稳定，混合检索强大，生产级

**如果目标是长期学习型 Agent**
- 首选: **Letta**
- 理由: 完整的有状态 Agent 框架，自我改进

### 与 qmd 的关系

**qmd 的独特优势**
- ✅ 本地 GGUF 模型支持
- ✅ 一体化方案
- ✅ 对开发者友好

**建议的进化方向**
1. 保持 GGUF 模型支持（这是差异化优势）
2. 集成 BGE Reranker（提升精度）
3. 支持多种后端（Chroma/Qdrant/Meilisearch）
4. 添加 Mem0 风格的记忆管理 API
5. 优化 query expansion（小模型 + 缓存）

---

**报告完成时间**: 2026-03-13 00:14
**调研项目总数**: 14 个
**推荐方案**: 3 个
