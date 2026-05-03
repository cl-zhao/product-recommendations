# Zep 接入成本调研（面向 OpenClaw）

> 调研时间：2026-03-13
> 
> 结论先说：**当前这台 2C / 3.6G / 无 GPU 的机器，不建议跑 Zep Self-hosted（legacy CE）全套栈**；**最稳妥方案是接 Zep Cloud**。如果一定要自建，建议至少升到 **4 vCPU / 8GB RAM / 40GB+ 可用磁盘**，更推荐 **4 vCPU / 12GB RAM**。

---

## 1. 研究范围与事实来源

本次主要参考：

### 官方 / 一手来源
- Zep 官网与文档：
  - https://www.getzep.com/
  - https://help.getzep.com/
  - https://www.getzep.com/pricing/
  - https://help.getzep.com/quick-start-guide.mdx
  - https://help.getzep.com/performance.mdx
- Zep GitHub 仓库：
  - https://github.com/getzep/zep
- 仓库内 legacy/self-hosted 文件：
  - `legacy/docker-compose.ce.yaml`
  - `legacy/zep.yaml`
  - `legacy/Dockerfile.ce`
- 仓库内 MCP Server：
  - `mcp/zep-mcp-server/README.md`

### 上游依赖 / 补充依据
- Neo4j 官方文档：
  - system requirements
  - memory configuration

### 用户反馈 / 问题线索
- GitHub Issues 中与 self-host/docker 相关的问题：
  - #331 `Is the zep-nlp server required?`
  - #341 `store.type must be set`
  - #350 `level=fatal msg="store.type must be set"`
  - #196 / #276 关于 local model / CPU embeddings 的讨论

---

## 2. 先看一个关键变化：现在 Zep 的重点已经转向 Cloud

从当前 `getzep/zep` 仓库 README 可以确认：

- **Zep Community Edition 已经 deprecated / no longer supported**
- 社区版代码被移到仓库里的 `legacy/` 目录
- 官方明确建议：**优先使用 Zep Cloud**

这点很关键，因为它直接影响接入成本：

- **Cloud 成本：钱换运维省心**
- **Self-host 成本：机器 + 运维 + 调参 + 兼容性风险**

所以如果目标是把 Zep 接入 OpenClaw，而不是折腾基础设施，**Cloud 是默认推荐项**。

---

## 3. 系统要求分析

## 3.1 CPU 需求（核心数、架构）

### 官方能明确确认的部分
从 legacy 的 `docker-compose.ce.yaml` 看，Self-hosted 版至少包含以下服务：

1. `zep`（主服务，Go）
2. `db`（Postgres + pgvector）
3. `graphiti`（Python 服务）
4. `neo4j`（图数据库）

这意味着 **不是一个轻量单进程服务**，而是至少 **4 个容器/进程** 的组合。

### CPU 架构
你的机器是：
- **AMD EPYC 7543**
- Linux x86_64

这类架构对 Docker / Go / Python / Postgres / Neo4j 都是常见目标平台，**CPU 架构本身没有问题**。

### 核心数判断
官方当前文档**没有给出 Zep Self-hosted CE 的明确最低核心数**。但从服务组成看：

- Zep API 服务本身不算重
- `graphiti` 会做抽取/处理
- `neo4j` 与 `postgres` 都会吃 CPU
- 并发一上来，2 核会明显紧张

**经验判断：**
- **2 核：勉强实验级，不适合稳定长期运行**
- **4 核：比较像最低可用线**
- **8 核：更适合生产或中等并发**

### GPU 是否必须
**不必须。**

理由：
- legacy compose 里没有 GPU 依赖
- 官方 Cloud/SDK 文档也没有要求本地 GPU
- Graphiti/Zep 主要依赖外部 LLM/API（如 OpenAI）做抽取，而不是强制本地 GPU 推理

但要注意：
- **没有 GPU ≠ 没有模型成本**
- 如果走 self-host，通常仍需要外部 LLM API key（legacy compose 中 `graphiti` 默认就是 `OPENAI_API_KEY`）

**结论：Zep 不是 GPU 型系统，GPU 不是门槛。**

---

## 3.2 内存需求

这是当前设备最大的瓶颈。

### 官方线索
legacy compose 直接拉起：
- Zep
- Postgres/pgvector
- Graphiti
- Neo4j

其中：
- **Neo4j 是内存敏感型组件**
- Neo4j 官方 memory 文档明确说：
  - 操作系统本身要预留内存
  - **1GB 是 dedicated Neo4j server 给 OS 的一个 good starting point**
  - Neo4j 的 heap / page cache 还要另外分配

此外，Neo4j 社区页面和官方 requirements 相关线索里，常见最低讨论就是 **2GB VM 级别只是下限**，不代表适合带图索引/向量/并发查询的场景。

### 对 Zep 全栈的实际推断
粗略分解：

- `neo4j`：通常就希望有 **1.5GB~3GB+** 的可用内存空间才比较从容
- `postgres + pgvector`：**0.5GB~1GB+**
- `graphiti`（Python + LLM 调用 + 抽取）：**0.5GB~1.5GB+**
- `zep` 主服务：**几百 MB 内**
- Docker / OS / page cache / 临时峰值：再留一截

### 实际判断
你的机器：
- 总内存 **3.6G**
- 可用 **2.3G**

这对单个轻量服务还行，但对 `zep + postgres + graphiti + neo4j` 全家桶来说：

**明显偏小。**

最可能出现的问题：
- 容器频繁抢内存
- `neo4j` 启动后性能差或 OOM
- `graphiti` 在抽取阶段波动大
- 系统开始 swap，整体延迟和稳定性崩掉

### 内存建议
- **不推荐低于 6GB RAM** 跑完整 self-host Zep legacy 栈
- **最低建议：8GB RAM**
- **更稳妥：12GB RAM**

---

## 3.3 磁盘空间需求

### 组件视角
Self-hosted 至少有两块持久化数据：
- Postgres volume：`zep-db`
- Neo4j volume：`neo4j_data`

再加上：
- Docker image 层
- 容器日志
- 系统临时文件
- 未来 memory / graph 数据增长

### 你的机器
- 总盘：60G
- 可用：33G

### 判断
**33G 可用磁盘短期测试够用，长期不宽裕但不是第一瓶颈。**

建议理解为：
- **开发/验证：够用**
- **长期运行：偏紧，尤其日志和图库增长后要盯着**
- **生产建议：至少留 40~60G 可用空间更安心**

### 磁盘结论
- 当前磁盘 **不是硬伤**
- 但在内存不足的前提下，即使盘够，整体也跑不稳

---

## 4. 部署方式分析

## 4.1 Self-hosted 方案的硬件要求

### 从 compose 文件看到的真实依赖
`legacy/docker-compose.ce.yaml` 不是单机 SQLite 小工具，而是：

- Zep API
- Postgres/pgvector
- Graphiti
- Neo4j

也就是说，**Self-hosted 的真正成本不只是“起个 Docker”**，而是维护一个小型多服务知识图谱系统。

### Self-host 最低可用配置（建议值）
> 这是基于官方 compose 结构 + Neo4j 内存特性 + 轻量单机经验给出的保守建议，不是 Zep 官方 SLA。

#### 仅开发测试 / 低负载
- **CPU：4 vCPU**
- **内存：8GB**
- **磁盘：40GB 可用**
- **GPU：不需要**

#### 稍稳定一点的长期运行
- **CPU：4~8 vCPU**
- **内存：12GB~16GB**
- **磁盘：60GB+ 可用**

### 当前机器能不能 self-host？
**不建议。**

原因不是 CPU 架构，也不是磁盘，而是：
- **可用内存只有 2.3G，离四服务栈的舒适区差太多**
- 2 核也会让 `neo4j + graphiti + postgres` 彼此抢资源

---

## 4.2 Cloud 方案定价

根据当前官网 Pricing：

### Free
- **每月 1,000 credits 免费**
- 低速率限制
- 适合试用/PoC

### Flex
- **$25 / 月**
- 含 **20,000 credits**
- 超出后 **$25 / 20,000 credits**
- 600 RPM
- 5 Projects

### Flex Plus
- **$475 / 月**
- 含 **300,000 credits**
- 超出后 **$125 / 100,000 credits**
- 1,000 RPM
- 5 Projects
- 自定义抽取规则、webhooks、7天 API logs 等

### Enterprise
- 不公开价，联系销售
- 提供 Managed / BYOK / BYOM / BYOC 等模式

### 对你这个场景的含义
如果只是给 OpenClaw 做记忆能力验证：
- **先上 Free** 就够试
- 如果开始稳定使用，再看 **Flex $25/月**

这比升级 VPS/云主机 + 运维数据库 + 排查 Docker 问题，通常更划算。

---

## 4.3 Docker 部署的资源消耗

### 直接成本
Self-host Docker 版不是单容器：
- 至少 4 个服务
- 至少 2 个持久化卷
- 至少 4 份日志流

### 隐性成本
GitHub issues 能看到几类典型问题：
- 环境变量配置不完整导致无法启动（如 `store.type must be set`）
- 版本/配置变动造成 compose 不兼容
- 需要理解 Postgres、Neo4j、Graphiti 三层依赖

### 总体评价
**Docker 能部署，但不等于低成本。**

它更像：
- 运维复杂度中等偏上
- 机器资源需求明显高于“普通聊天记忆服务”
- 对小规格 VPS 不友好

---

## 5. 与 OpenClaw 集成的成本

## 5.1 有没有现成 OpenClaw 集成？

**目前没有看到 Zep 的现成 OpenClaw 官方集成方案。**

我做了两类检查：
- 在当前 OpenClaw workspace 内 grep，没有现成 Zep 相关内容
- Web 搜索没有发现明确的 **OpenClaw × Zep 官方 skill / extension**

但注意：**没有现成集成 ≠ 很难接**。

### 能借用的现成东西
Zep 仓库里有：
- 官方 SDK：Python / TypeScript / Go
- 若干 agent framework integration（如 Autogen）
- 一个 **Zep MCP Server**

其中 Zep MCP Server 的 README 显示：
- 它是给 **Zep Cloud** 用的
- **只读**访问 knowledge graph / memory
- 适合 Claude Desktop / Cline 一类 MCP client

### 对 OpenClaw 的实际意义
OpenClaw 当前更现实的两种接法：

#### 方案 A：在 OpenClaw skill / extension 里直接调 Zep SDK 或 HTTP API
这是最靠谱的。

例如：
- 用户消息进入 OpenClaw 时，调用 Zep `thread.add_messages`
- 生成回复前，调用 `thread.get_user_context` 或 graph search
- 把返回的 context 拼到 prompt / memory pipeline 里

#### 方案 B：自己包一层中间服务
如果不想把 Zep 逻辑散落到 skill 内，可以做一个小服务：
- OpenClaw → 你的 memory adapter → Zep

优点：
- 后期更容易切换 Mem0 / 自研 memory
- 更适合统一日志、缓存、重试

### 方案 C：MCP 间接接入
理论上可行，但当前仓库里的 Zep MCP Server 偏 **只读查询**，不适合作为完整“写入+召回”的 agent memory 主链路。

所以：
- **能辅助检索**
- **不适合单独承担完整记忆接入**

---

## 5.2 需要多少额外配置？

### 如果用 Zep Cloud
额外配置其实不多，核心是：

1. 申请 Zep 账号
2. 拿 `ZEP_API_KEY`
3. 在 OpenClaw 的 skill / runtime 里初始化客户端
4. 约定好映射关系：
   - OpenClaw user/session → Zep user/thread
5. 在消息写入与上下文召回两个位置接入

### 接入工作量估算（Cloud）
如果你已经熟 OpenClaw 技术栈：
- **PoC：0.5 ~ 1 天**
- **可用版：1 ~ 2 天**
- **做得比较稳（重试/缓存/观测/裁剪策略）：2 ~ 4 天**

### 如果用 Self-hosted
除了上面的逻辑接入，还要额外做：
- Docker compose 部署
- Postgres / Neo4j 数据持久化
- Graphiti / OpenAI key 配置
- 服务健康检查
- 备份 / 升级 / 故障处理

### 接入工作量估算（Self-host）
- **PoC：1 ~ 2 天**（前提是机器资源够 + 部署顺利）
- **稳定可用：3 天以上**
- 如果机器资源不够，时间会被环境问题无限吞掉

---

## 6. 针对当前设备的判断

你的设备：
- **CPU：2 核 AMD EPYC 7543**
- **无 GPU**
- **内存：3.6G（可用 2.3G）**
- **磁盘：60G（可用 33G）**
- **系统：Linux OpenCloudOS**

## 6.1 能否运行 Zep Cloud 接入？
**可以，完全可以。**

因为 Cloud 方案本地只需要：
- 跑 OpenClaw 本身
- 发 HTTP 请求给 Zep Cloud
- 本地不承担图数据库/抽取服务/存储

这台机器跑 Cloud 客户端接入没有问题。

## 6.2 能否运行 Zep Self-hosted？
**理论上可能勉强拉起来，实际上不建议投入。**

原因：
- **内存是决定性短板**
- 2 核对四服务栈偏紧
- legacy CE 本身已 deprecated，遇到坑时回报率低

### 最现实判断
- **用于“我就试试看能不能启动”**：有概率能靠调参碰碰运气
- **用于实际给 OpenClaw 提供稳定记忆能力**：**不适合**

---

## 7. 如果不能，最低硬件升级建议

如果目标是 **自建 Zep legacy CE**，最低建议如下：

### 最低升级线
- **CPU：4 vCPU**
- **RAM：8GB**
- **磁盘：至少 40GB 可用**

### 更推荐的线
- **CPU：4 vCPU**
- **RAM：12GB**
- **磁盘：60GB 可用**

### 为什么不是先升 CPU？
因为你当前最缺的是 **RAM**，不是算力。

优先级建议：
1. **先把内存升到 8GB+**
2. 再看 CPU 是否升到 4 核
3. 磁盘目前次要

如果只能做一件事：
- **优先换到 8GB 内存以上的机器**

---

## 8. 推荐接入方案

## 8.1 总推荐：**Zep Cloud + OpenClaw 自定义接入**

这是我最推荐的方案，原因很直接：

- **适配当前机器**：几乎无本地资源压力
- **接入路径清晰**：SDK / HTTP API 都现成
- **官方主推方向**：比 legacy self-host 更稳
- **成本可控**：先用 free / flex
- **运维最少**：不需要你自己养 Neo4j + Postgres + Graphiti

### 推荐落地方式
在 OpenClaw 中做一个小的 memory adapter：

- `on_message` 时：写入 `user/thread/messages`
- `before_llm` 时：取 `context block`
- `after_response` 时：把 assistant 回复也回写

这样基本就能形成完整闭环。

## 8.2 不推荐：当前机器上直接 self-host

不推荐原因：
- 机器太小
- legacy CE 已不再是官方重点
- 你会把时间花在基础设施，而不是业务接入

## 8.3 只有在以下条件下才考虑 self-host

只有当你明确需要：
- 数据必须自持有
- 不能接受托管 SaaS
- 有更大机器（至少 4C8G）
- 有时间做数据库/图数据库运维

这时才值得评估 self-host。

---

## 9. 最终结论（给决策用）

## 能否在当前设备上运行？
- **Zep Cloud 接入：能，且推荐**
- **Zep Self-hosted legacy：不建议，实际可用性差**

## 如果不能，最低硬件升级建议
- **最低：4 vCPU / 8GB RAM / 40GB+ 可用磁盘**
- **更推荐：4 vCPU / 12GB RAM / 60GB+ 可用磁盘**
- **GPU 不需要**

## 推荐接入方案
**首选：Zep Cloud**

### 推荐理由
- 当前设备可直接使用
- 官方主推，文档/SDK齐全
- 接入 OpenClaw 只需做一层自定义 skill / adapter
- 额外配置少，PoC 快
- 总成本通常低于自建运维成本

---

## 10. 对 OpenClaw 集成的实施建议（简版）

如果后续要真的开干，建议按这个顺序：

1. **先用 Zep Free / Flex 做 PoC**
2. 在 OpenClaw 中实现：
   - `ensureUser(userId)`
   - `ensureThread(threadId, userId)`
   - `appendMessages(threadId, messages)`
   - `getContext(threadId)`
3. 先只接：
   - 单用户
   - 单会话线程
   - 对话消息记忆
4. 跑通后再加：
   - 业务数据 ingestion
   - graph search
   - context template
   - 失败重试 / 限流 / 观测

---

## 11. 我自己的判断（一句话版）

**这台 2C3.6G 机器拿来接 Zep Cloud 很合适，拿来跑 Zep Self-hosted 基本是在给自己上强度。**
