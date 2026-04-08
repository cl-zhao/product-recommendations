# MemPalace 开源项目深度调研报告

> 调研时间：2026-04-07
> 项目地址：https://github.com/milla-jovovich/mempalace
> スター数：210+ (上线1天内达成)

---

## 一、项目概述

MemPalace 是一个**本地运行的 AI 记忆系统**，号称"有史以来基准测试得分最高的 AI 记忆系统，而且免费"。它解决的核心问题是：**你和 AI 的每一段对话（决策、调试、设计辩论）在会话结束后就消失了**。六个月每天使用 AI = 1950万 token 的决策历史，全部丢失。

核心卖点：
- **LongMemEval R@5 得分 96.6%**，无需任何 API 调用
- **100% R@5**（配合 Haiku 重排）
- **零订阅、零云端、纯本地**，仅依赖 ChromaDB + PyYAML
- 支持 **MCP 协议**，可接入 Claude Code、Cursor 等 AI 工具

---

## 二、核心创新

### 2.1 The Palace（记忆宫殿）

MemPalace 将**古希腊修辞学中的"记忆宫殿"方法**应用于 AI 记忆管理。其灵感来源：古希腊雄辩家通过在想象中的建筑里"放置"思想来记忆整篇演讲——走进建筑，找到思想。

结构层次（类比古希腊宫殿）：

```
┌─────────────────────────────────────────────────────────────┐
│  WING（侧厅）：Person / Project                              │
│    │                                                        │
│    ├── Room A ──hall── Room B（同一侧厅内的走廊）             │
│    │                                                        │
│    │    Closet（压缩摘要）→ Drawer（原始文件）                │
└────┼────────────────────────────────────────────────────────┘
     │
   tunnel（隧道：跨侧厅连接同一主题）
     │
┌────┼────────────────────────────────────────────────────────┐
│  WING：Project                                              │
└─────────────────────────────────────────────────────────────┘
```

| 层级 | 说明 |
|------|------|
| **Wing（侧厅）** | 一个人物或项目，可以有任意多个 |
| **Room（房间）** | 侧厅内的具体主题，如 auth-migration、graphql-switch |
| **Hall（走廊）** | 记忆类型走廊，每个侧厅都有：hall_facts（决策）、hall_events（事件）、hall_discoveries（发现）、hall_preferences（偏好）、hall_advice（建议）|
| **Tunnel（隧道）** | 跨侧厅的主题连接——当不同侧厅都有"auth"房间时，隧道自动建立跨域关联 |
| **Closet（储藏室）** | 压缩摘要，AI 快速读取 |
| **Drawer（抽屉）** | 原始逐字文件，永不摘要 |

**关键洞察**：结构本身就能带来 **+34% 的检索提升**。测试数据：

| 搜索范围 | R@10 得分 |
|---------|-----------|
| 搜索所有 closet | 60.9% |
| 限定 wing 内搜索 | 73.1%（+12%）|
| 限定 wing + hall | 84.8%（+24%）|
| 限定 wing + room | **94.8%（+34%）**|

> 📌 宫殿结构不是装饰——它是产品本身。

### 2.2 AAAK 方言（无损压缩）

AAAK（A Lossless Asymmetric Abstraction Keyboard 的缩写，具体含义官方未完全公开解释）是一种**无损符号记忆语言**，设计目标是让任何 LLM 都能快速读取，零解码器、零微调。

**设计理念**：不追求人类可读，而是追求"AI 可快速理解"。30倍压缩率。

**示例**：

英文原文（约1000 token）：
```
Priya manages the Driftwood team: Kai (backend, 3 years),
Soren (frontend), Maya (infrastructure), and Leo (junior, started last month).
They're building a SaaS analytics platform. Current sprint: auth migration to Clerk.
Kai recommended Clerk over Auth0 based on pricing and DX.
```

AAAK 版本（约120 token）：
```
TEAM: PRI(lead) | KAI(backend,3yr) SOR(frontend) MAY(infra) LEO(junior,new)
PROJ: DRIFTWOOD(saas.analytics) | SPRINT: auth.migration→clerk
DECISION: KAI.rec:clerk>auth0(pricing+dx) | ★★★★
```

**兼容任意模型**：Claude、GPT、Gemini、Llama、Mistral——任何能读文本的模型都能读 AAAK。在本地 Llama 模型上运行，整个记忆栈完全离线。

**格式特点**：
- 实体用3位大写字母代码（KAI=Priya，ALC=Alice）
- 情感用星标表示重要性（★~★★★★★）
- 管道符分隔字段，结构紧凑

### 2.3 知识图谱（Temporal Entity-Relationship Graph）

MemPalace 维护一个**时序实体关系三元组图谱**，存储在 SQLite 本地文件中，类似于 Zep 的 Graphiti，但完全免费且自托管。

```python
from mempalace.knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()
kg.add_triple("Kai", "works_on", "Orion", valid_from="2025-06-01")
kg.add_triple("Maya", "assigned_to", "auth-migration", valid_from="2026-01-15")

# 查询2026年1月时 Maya 的状态
kg.query_entity("Maya", as_of="2026-01-20")
# → [Maya → assigned_to → auth-migration (active)]
```

**特点**：
- 时序有效性窗口（valid_from → valid_to）
- 实体关系可失效（invalidate）
- 历史查询 vs 当前查询
- 自动计算年龄、日期、工龄（动态而非硬编码）

| 对比项 | MemPalace | Zep (Graphiti) |
|--------|-----------|----------------|
| 存储 | SQLite（本地）| Neo4j（云端）|
| 费用 | 免费 | $25/月+ |
| 时序有效性 | ✅ | ✅ |
| 自托管 | ✅ 始终 | ❌ 仅企业版 |
| 隐私 | 全部本地 | SOC 2, HIPAA |

### 2.4 矛盾检测

MemPalace 会对输入内容与已有知识图谱进行对比，自动标记矛盾：

```
输入: "Soren finished the auth migration"
输出: 🔴 AUTH-MIGRATION: attribution conflict — Maya was assigned, not Soren

输入: "Kai has been here 2 years"
输出: 🟡 KAI: wrong_tenure — records show 3 years (started 2023-04)

输入: "The sprint ends Friday"
输出: 🟡 SPRINT: stale_date — current sprint ends Thursday (updated 2 days ago)
```

---

## 三、技术架构

### 3.1 四层记忆栈

| 层级 | 内容 | 大小 | 加载时机 |
|------|------|------|---------|
| **L0** | 身份——这个 AI 是谁 | ~50 token | 始终 |
| **L1** | 关键事实——团队、项目、偏好 | ~120 token（AAAK）| 始终 |
| **L2** | 房间回忆——近期会话、当前项目 | 按需 | 话题出现时 |
| **L3** | 深度搜索——跨所有 closet 的语义查询 | 按需 | 显式询问时 |

AI 启动时只需 ~170 token 就能"认识你的世界"，搜索只在需要时触发。

### 3.2 数据流

```
用户 → CLI
       │
   ┌───▼────────┐
   │   miner    │  ← 项目文件摄取（代码、文档、笔记）
   │ convo_miner│  ← 对话摄取（按 Q+A 对分块）
   └─────┬──────┘
         ▼
   ┌───────────┐
   │  ChromaDB  │  ← Palace（宫殿存储，逐字原文）
   └─────┬─────┘
         │
   ┌─────▼────────┐
   │ knowledge_    │  ← SQLite（时序实体关系图谱）
   │ graph         │
   └─────┬─────────┘
         │
   ┌─────▼────────┐
   │ mcp_server    │  ← 19个 MCP 工具
   └───────────────┘
```

### 3.3 支持的输入格式

`normalize.py` 支持5种聊天格式标准化：
- Claude Code JSONL
- Claude.ai JSON
- ChatGPT JSON
- Slack JSON
- 纯文本

### 3.4 MCP Server（19个工具）

**Palace 读取工具**：

| 工具 | 功能 |
|------|------|
| `mempalace_status` | 宫殿概览 + AAAK 规范 + 记忆协议 |
| `mempalace_list_wings` | 所有侧厅及抽屉计数 |
| `mempalace_list_rooms` | 侧厅内的房间列表 |
| `mempalace_get_taxonomy` | 完整 wing→room→count 树 |
| `mempalace_search` | 语义搜索，支持 wing/room 过滤 |
| `mempalace_check_duplicate` | 归档前检查重复 |
| `mempalace_get_aaak_spec` | AAAK 方言参考 |

**Palace 写入工具**：

| 工具 | 功能 |
|------|------|
| `mempalace_add_drawer` | 归档逐字内容 |
| `mempalace_delete_drawer` | 按 ID 删除抽屉 |

**知识图谱工具**：

| 工具 | 功能 |
|------|------|
| `mempalace_kg_query` | 时间过滤的实体关系查询 |
| `mempalace_kg_add` | 添加事实 |
| `mempalace_kg_invalidate` | 标记事实已失效 |
| `mempalace_kg_timeline` | 实体编年史 |
| `mempalace_kg_stats` | 图谱概览 |

**导航工具**：

| 工具 | 功能 |
|------|------|
| `mempalace_traverse` | 从某房间出发跨侧厅遍历 |
| `mempalace_find_tunnels` | 找到桥接两个侧厅的房间 |

**Agent 日记工具**：

| 工具 | 功能 |
|------|------|
| `mempalace_diary_write` | 用 AAAK 写日记 |
| `mempalace_diary_read` | 读取近期日记 |

### 3.5 Auto-Save Hooks

为 Claude Code 提供两个自动保存钩子：

- **mempal_save_hook.sh**：每15条消息触发结构化保存（主题、决策、引用、代码变更）
- **mempal_precompact_hook.sh**：上下文压缩前紧急保存

---

## 四、性能基准

### 4.1 LongMemEval（核心基准）

| 系统 | R@5 | LLM 调用 | 成本 |
|------|-----|---------|------|
| **MemPal (hybrid + Haiku 重排)** | **100%**（500/500）| 可选 | ~$0.001/次 |
| Supermemory ASMR | ~99% | 必需（未公开）| — |
| **MemPal (raw, 无 LLM)** | **96.6%** | **无需** | **$0** |
| Mastra | 94.87% | 必需（GPT-5-mini）| API 费用 |
| Hindsight | 91.4% | 必需（Gemini-3）| — |
| Supermemory（生产）| ~85% | 必需（未公开）| — |
| Mem0 | ~85% | 必需 | $19-249/月 |

**MemPalace raw（96.6%）是有史以来公开发布的 LongMemEval 最高分，无需 API key、无需云端、LLM 零调用。**

### 4.2 LoCoMo（Salesforce, 75000+ QA 对）

| 系统 | 得分 | 备注 |
|------|------|------|
| **MemPal** | **92.9%** | 逐字文本 + 语义搜索 |
| Gemini（长上下文）| 70-82% | 全量历史放入上下文窗口 |
| Block extraction | 57-71% | LLM 处理过的块 |
| Mem0 (RAG) | 30-45% | LLM 提取的记忆 |

> 📌 MemPal 比 Mem0 高出 **2倍以上**，原因：Mem0 用 LLM 决定"记住什么"并丢弃其余，MemPalace 存储逐字文本什么都不丢弃。

### 4.3 成本对比

| 方案 | 加载 token 量 | 年度成本 |
|------|-------------|---------|
| 粘贴所有内容 | 1950万（塞不进任何上下文窗口）| 不可能 |
| LLM 摘要 | ~65万 | **~$507/年** |
| **MemPalace wake-up** | **~170 token** | **~$0.70/年** |
| **MemPalace + 5次搜索** | **~13500 token** | **~$10/年** |

---

## 五、与主流方案对比

### 5.1 功能矩阵

| 功能 | MemPalace | Mem0 | Zep | Supermemory |
|------|-----------|------|-----|-------------|
| 存储方式 | ChromaDB+SQLite | 云端向量 | Neo4j+Postgres | 云端 |
| 费用 | **免费** | $19-249/月 | $25/月+ | 付费 |
| 完全离线 | ✅ | ❌ | ❌（企业版才行）| ❌ |
| MCP 支持 | ✅ 19工具 | ❌ | ❌ | ❌ |
| 记忆宫殿结构 | ✅ | ❌ | ❌ | ❌ |
| AAAK 压缩 | ✅ | ❌ | ❌ | ❌ |
| 时序知识图谱 | ✅ | 部分 | ✅ | 部分 |
| 矛盾检测 | ✅ | ❌ | ❌ | ❌ |
| Agent 专家系统 | ✅ | ❌ | ❌ | ❌ |
| Auto-save Hooks | ✅ | ❌ | ❌ | ❌ |

### 5.2 核心差异

**MemPalace vs Mem0**：
- Mem0 用 LLM 决定记住什么 → 信息丢失
- MemPalace 存储所有原文 → 信息零丢失
- MemPalace 比 Mem0 高出 2倍+

**MemPalace vs Zep**：
- Zep 用 Neo4j 云端 → $25/月+
- MemPalace 用 SQLite 本地 → 免费
- 功能几乎等价，但成本差距巨大

**MemPalace 的独特价值**：
1. 记忆宫殿结构——+34% 检索提升的结构化记忆组织方式
2. AAAK 方言——30x 无损压缩，任意 LLM 可读
3. 完全本地运行——隐私优先，无任何云依赖

---

## 六、使用场景

### 场景一：独立开发者跨多项目

```bash
# 挖掘每个项目的对话
mempalace mine ~/chats/orion/  --mode convos --wing orion
mempalace mine ~/chats/nova/   --mode convos --wing nova

# 六个月后查询
mempalace search "database decision" --wing orion
# → "Chose Postgres over SQLite because dataset will exceed 10GB. Decided 2025-11-03."

# 跨项目搜索
mempalace search "rate limiting approach"
# → 在 Orion 和 Nova 中找到各自的方案并展示差异
```

### 场景二：团队负责人管理产品

```bash
# 挖掘 Slack 导出和 AI 对话
mempalace mine ~/exports/slack/ --mode convos --wing driftwood
mempalace mine ~/.claude/projects/ --mode convos

# "Soren 上个 sprint 做了什么？"
mempalace search "Soren sprint" --wing driftwood
# → 14个 closet: OAuth 重构、深色模式、组件库迁移

# "谁决定用 Clerk？"
mempalace search "Clerk decision" --wing driftwood
# → "Kai 推荐 Clerk 而非 Auth0 —— 定价 + 开发者体验。团队 2026-01-15 达成一致。Maya 负责迁移。"
```

### 场景三：Claude Code 自动记忆

连接 MCP 后，Claude Code 每15条消息自动保存记忆，上下文压缩前紧急保存，AI 永远不会丢失工作上下文。

---

## 七、优势与局限

### ✅ 优势

1. **零成本本地运行**：仅依赖 ChromaDB + PyYAML，无需任何 API key
2. **基准测试领先**：LongMemEval 96.6% raw，无 LLM 调用下最高分
3. **记忆宫殿结构**：结构本身带来 +34% 检索提升，想法独特
4. **AAAK 无损压缩**：30x 压缩让数月上下文在 ~170 token 内呈现
5. **矛盾检测**：主动标记知识图谱中的事实冲突
6. **MCP 协议支持**：19个工具，开箱即用
7. **Agent 专家系统**：每个专家有独立 wing 和日记，50个专家配置不变
8. **隐私优先**：所有数据本地，不经过任何云服务

### ⚠️ 局限

1. **生态较新**：2026年4月5日上线，生态（插件、集成、社区）还在早期
2. **无官方中文文档**：目前仅有英文文档
3. **需要手动挖掘**：不能自动监听——需要主动运行 `mempalace mine`
4. **AAAK 学习成本**：团队成员需要学习理解 AAAK 格式
5. **ChromaDB 限制**：向量检索依赖 ChromaDB，大规模部署可能需要调优
6. **benchmark 可复现性存疑**：虽然作者提供了 runners，但基准测试主要由作者独立完成，第三方独立验证较少
7. **无多用户支持**：目前主要面向个人用户，团队协作场景未覆盖

---

## 八、总结与评价

### 核心理念

MemPalace 的核心洞察是：**"大多数记忆系统在做不必要的事"**。

Mem0、Mastra、Supermemory 等都假设需要 LLM 来决定"记住什么"——用 AI 提取事实，丢弃原文，存摘要。但这个假设本身可能是错的。

MemPalace 的做法：存储所有原文，然后依靠结构来让搜索变得可找到。宫殿结构（wing/room/hall）本身就是检索信号，贡献了 +34% 的提升。原始逐字文本在 ChromaDB 中搜索就能达到 96.6% R@5，而这是"什么都没丢弃"的记忆。

### 创新程度

| 创新点 | 评价 |
|--------|------|
| 记忆宫殿映射到 AI 记忆 | ⭐⭐⭐⭐⭐ 极具创意，古希腊方法论的现代应用 |
| AAAK 方言设计 | ⭐⭐⭐⭐⭐ 独特且有实际价值 |
| 矛盾检测 | ⭐⭐⭐⭐ 有实际意义 |
| 纯本地 + 高性能 | ⭐⭐⭐⭐⭐ 极难兼顾 |
| 整体产品完成度 | ⭐⭐⭐⭐ 成熟度超出预期 |

### 适合人群

- **AI 深度用户**：每天使用 Claude/Copilot/Cursor，不想每次从头解释背景
- **独立开发者**：多个项目并行，需要跨项目记住决策历史
- **隐私敏感用户**：不希望记忆数据经过任何云服务
- **长期记忆需求强烈者**：6个月以上的 AI 使用历史需要被有效复用

### 不适合人群

- 需要团队协作功能
- 无法接受命令行操作（目前主要是 CLI + MCP，无 GUI）
- 期望开箱即用的全自动化（需要主动 mine）

### 一句话评价

> MemPalace 将古希腊记忆术与 AI 向量检索结合，用纯本地、零成本的方式实现了比 $249/月 云服务更高的检索精度。96.6% 的无 LLM 调用得分和 30x AAAK 压缩是工程上的意外惊喜——整个领域都在用复杂的方式解决记忆问题，而 MemPalace 证明"存下所有，逐字搜索，结构导航"这个简单思路的表现超出所有人预期。

---

## 九、快速上手

```bash
# 1. 安装
pip install mempalace

# 2. 初始化
mempalace init ~/projects/myapp

# 3. 挖掘数据
mempalace mine ~/projects/myapp --mode convos --wing myapp

# 4. 搜索
mempalace search "why did we switch to GraphQL"

# 5. MCP 接入（Claude Code）
claude mcp add mempalace -- python -m mempalace.mcp_server
```

---

## 参考链接

- GitHub: https://github.com/milla-jovovich/mempalace
- Discord: https://discord.com/invite/ycTQQCu6kn
- 基准测试: `benchmarks/BENCHMARKS.md`
- v3.0.0 | Python 3.9+ | MIT License

---

*调研报告由 AI 自动生成，基于 https://github.com/milla-jovovich/mempalace 仓库源码及文档分析。*
*调研时间：2026-04-07*
