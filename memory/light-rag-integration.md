# Light-RAG Memory 集成文档

## 现状（2026-03-13）

### 索引情况
- 已索引 memory 目录所有 `.md` 文件（45 个文档，309 chunks）
- 使用 BGE-small-zh-v1.5 本地 ONNX 模型，无需外部 API
- 索引路径：`light-rag/data/memory-index/`
- 配置文件：`light-rag/config/config.memory.yaml`

### 检索命令
```bash
# 直接用 wrapper 脚本（推荐）
/root/.openclaw/workspace/bin/light-rag-search "查询文本" --top-k 5

# 原始 CLI
cd /root/.openclaw/workspace/light-rag
source venv/bin/activate
PYTHONPATH=. python -m src.cli --config config/config.memory.yaml search "查询文本"

# 重建索引（有新文件时）
PYTHONPATH=. python -m src.cli --config config/config.memory.yaml index
```

### 检索效果评测（5条查询）

| 查询 | Top-1 文件 | 评分 |
|---|---|---|
| 用户喜欢什么沟通风格 | user-preferences.md（第2名） | 一般 |
| 模型使用策略 GLM MiniMax | model-policy.md（第5名） | 一般 |
| GitHub 权限 配置 | github-access.md（第1名）| **好** |
| AI 智能体开发 C# Python | agentscope-review.md | **好** |
| qmd 中文分词 问题 | 2026-03-13.md | **好** |

**结论：3/5 好，2/5 一般，无差。比 qmd 稳定（无中文分词 bug）**

### 集成方案

#### 当前：方案 B（Wrapper 脚本）
OpenClaw 无原生接口让外部 CLI 替换 qmd。  
目前采用的方案：**我（Agent 小亮）主动调用 wrapper 脚本做语义检索**。

**何时用 light-rag-search：**
- 需要在 memory 目录查找相关上下文时
- qmd 返回结果不准、或 memory_search fallback 到 Gemini 时
- 需要更精确的中文语义检索时

#### 未来：方案 A（OpenClaw 原生 local provider）
OpenClaw 支持 `agents.defaults.memorySearch.provider = "local"` + 本地 ONNX 模型。  
light-rag 使用的 `bge-small-zh-v1.5` 和 OpenClaw 的 local provider 格式兼容，  
可以考虑直接配置 OpenClaw 使用该模型，绕开 qmd 整个链路。  
但 OpenClaw 的 local provider 不读 HNSW 索引，每次查询需要暴力扫描，内存不友好。  
**暂不迁移，先用 wrapper 方案。**

## 定期维护
- 新增 memory 文件后，重新跑 `index` 命令更新索引
- 索引增量更新，不会重复处理已有文件
