# Hermes Agent 与 OpenClaw 协作方案调研报告

> 调研日期：2026-04-13
> 调研方式：网络检索（官方文档、GitHub Issues、Reddit、中文社区）
> 参考资料：11 篇

---

## 一、概述

Hermes Agent 和 OpenClaw 是当前开源 AI Agent 生态中定位最相近的两个框架。根据调研，两者已经从早期的"竞争替代"演进为**互补协作**——既可以一键迁移，也可以并行使用。

---

## 二、三大协作方案

### 方案一：从 OpenClaw 迁移到 Hermes（官方工具）

**来源**：GitHub NousResearch/hermes-agent 官方文档
**日期**：2026年4月

Hermes Agent 提供了官方的 OpenClaw 迁移工具 `hermes claw migrate`。

#### 迁移命令

```bash
# 预览迁移内容（推荐先执行）
hermes claw migrate --dry-run

# 完整迁移（包含 API keys）
hermes claw migrate --preset full --yes

# 仅迁移用户数据（不含密钥）
hermes claw migrate --preset user-data

# 覆盖已有冲突文件
hermes claw migrate --overwrite
```

#### 迁移选项说明

| 选项 | 说明 |
|------|------|
| `--dry-run` | 预览，不执行实际迁移 |
| `--preset full` | 默认，包含密钥迁移 |
| `--preset user-data` | 不含 API keys |
| `--overwrite` | 覆盖冲突文件 |
| `--skill-conflict skip/overwrite/rename` | 技能冲突处理方式 |
| `--yes` | 跳过确认提示 |

#### 迁移后验证

```bash
# 检查迁移报告
hermes status

# 测试消息平台
systemctl --user restart hermes-gateway

# 清理旧文件
hermes claw cleanup
```

---

### 方案二：两者并行使用（社区推荐 ⭐）

**来源**：Reddit r/AgentsOfAI、博客园
**日期**：2026年4月

Reddit 社区普遍认为**两者可以同时运行，让每个工具负责最适合的场景**。

#### 典型分工模式

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| 多渠道 orchestration（规划、调度、多 Agent 协调）| OpenClaw | Gateway 控制平面更成熟 |
| 专注执行任务（快速、可重复的循环）| Hermes Agent | 内置学习循环，越用越强 |
| 国内办公沟通（微信/钉钉/飞书）| OpenClaw | 原生支持 |
| 国际通讯（Signal/WhatsApp）| Hermes Agent | 原生支持 |
| MLOps 实验/训练数据生成| Hermes Agent | Atropos 集成 |
| 需要精细手动控制| OpenClaw | 配置文件驱动 |
| 需要 5000+ 社区技能 | OpenClaw | LinSkills 生态 |

> **Reddit 原文引用**（r/AgentsOfAI，2026年4月）：
> *"OpenClaw is strong for multi-channel automation and operational workflows, while Hermes Agent shines with persistent memory and long-term learning. Instead of picking one, you could run both in the same stack and let each handle what it does best."*

---

### 方案三：Skills 生态共享

**来源**：GitHub 官方文档、爱范儿
**日期**：2026年4月

**核心发现**：agentskills.io 格式的 Skills 可以在 Hermes Agent 和 OpenClaw 之间**跨平台共享**。

#### 共享路径

| Skills 来源 | OpenClaw 位置 | Hermes 位置 |
|-------------|---------------|-------------|
| Workspace skills | `workspace/skills/` | `~/.hermes/skills/openclaw-imports/` |
| Managed skills | `~/.openclaw/skills/` | `~/.hermes/skills/openclaw-imports/` |
| 个人跨项目 | `~/.agents/skills/` | `~/.hermes/skills/openclaw-imports/` |

> 官方原文：*"Imported skills land in ~/.hermes/skills/openclaw-imports/"*

---

## 三、实际迁移案例

### 案例一：53AI 杨芳贤的完整迁移记录

**来源**：53AI 网站
**日期**：2026年4月9日

#### 迁移触发原因

> *"最近 OpenClaw 更新非常频繁，每次升级后都会遇到一些兼容性问题，尤其是 ACP 相关的变动比较大。与其不断修补，不如认真考虑一下迁移。"*

#### 实际执行步骤

```bash
# 1. 安装 Hermes（自动处理依赖）
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 2. 健康检查
hermes doctor

# 3. 迁移预览
hermes claw migrate --dry-run

# 4. 执行迁移
hermes claw migrate

# 5. 配置向导
hermes setup
```

#### 迁移后体验

- **技能兼容性**：原 OpenClaw 中创建的 MiniMax Music skill 依然可正确调用
- **工作流透明度**：工具调用展示比 OpenClaw 更清晰
- **定时任务**：Cron Jobs 未自动迁移，需手动配置
- **整体评价**：*"技能、记忆、消息渠道等核心资产都能通过一条命令完成导入，兼容性表现出色"*

---

### 案例二：GitHub Issues 中的迁移问题

**来源**：GitHub Issue #5191
**日期**：2026年4月

#### 报告的问题

使用 `hermes claw migrate` 迁移后，Gateway 启动时存在两个静默失败：
1. 某些配置项未正确迁移
2. 没有警告提示

#### 官方响应

已记录为 Issue，团队正在修复中。建议迁移后运行 `hermes doctor` 检查状态。

---

## 四、社区讨论精选

### Reddit 用户反馈

#### 正向评价（迁移到 Hermes）

| 用户 | 评价 |
|------|------|
| u/damn_brotha | *"use OpenClaw for multi-channel orchestration and Hermes for focused execution tasks"* |
| u/hotdog_sunset | *"可靠性更高，OpenClaw 工作流时好时坏"* |
| u/Comprehensive-Cake-3 | *"Hermes 更稳定，不会每次更新后出问题"* |

#### 负面评价（坚持 OpenClaw）

| 用户 | 理由 |
|------|------|
| u/Ok-Compound-3695 | *"OpenClaw 技能生态更丰富，5000+ 社区技能"* |
| u/Alternative-Card- | *"需要微信/钉钉支持，只能用 OpenClaw"* |

#### 双选观点

> *Reddit r/LocalLLaMA（2026年4月）：*
> *"I ran Hermes + Open-Claw side-by-side for 3 weeks. Switching was the wrong move"* — 但建议**堆叠使用（Stack them）**，让每个负责擅长的场景。

---

### 中文社区反馈

#### 知乎用户总结

> *"两者不互斥，agentskills.io 格式的 Skills 可以在 Hermes Agent 和 OpenClaw 之间共享。如果团队在国内使用微信/钉钉办公，OpenClaw 生态更合适；需要跑 MLOps 实验、生成训练数据、或接入 Signal/WhatsApp 则用 Hermes Agent。"*

---

## 五、技术架构对比

| 维度 | Hermes Agent | OpenClaw |
|------|-------------|----------|
| **核心定位** | Agent 执行循环为中心 | Gateway 控制平面为中心 |
| **编程语言** | Python | Node.js |
| **记忆系统** | 四层结构（常驻→归档→技能→用户建模）| 智能压缩上下文 |
| **技能生成** | ✅ 自动从经验中生成 | ❌ 手动编写 |
| **消息平台（国内）**| ❌ | ✅ 微信/钉钉/飞书/QQ |
| **消息平台（国际）**| ✅ Telegram/Discord/Slack/WhatsApp/Signal | ✅ |
| **沙箱隔离** | Docker/SSH/Singularity/Modal（5种）| 本地运行 |
| **模型支持** | OpenAI 兼容任何端点 | 国产模型原生支持 |
| **训练数据生成** | Atropos 集成 | ❌ 无 |

---

## 六、官方迁移对照表

**来源**：hermes-agent.nousresearch.com 官方迁移文档

| OpenClaw 路径 | Hermes 路径 | 备注 |
|---------------|-------------|------|
| `workspace/SOUL.md` | `~/.hermes/SOUL.md` | 直接复制 |
| `workspace/MEMORY.md` | `~/.hermes/memories/MEMORY.md` | 解析并合并 |
| `workspace/USER.md` | `~/.hermes/memories/USER.md` | 同上 |
| `openclaw.json` | `~/.hermes/config.yaml` | 配置映射 |
| `~/.openclaw/.env` | `~/.hermes/.env` | 含 API keys |
| 消息平台配置 | 环境变量 | TELEGRAM_BOT_TOKEN 等 |

### 不支持自动迁移的项目（需手动配置）

- Cron Jobs → 需用 `hermes cron create` 重建
- Plugins/Hooks → 需手动配置
- 多 Agent 配置 → 需使用 Hermes profiles
- 复杂通道绑定 → 需逐个平台配置

---

## 七、推荐决策框架

```
选择建议：
│
├── 需要微信/钉钉/飞书 → OpenClaw
│
├── 需要 Signal/WhatsApp / MLOps / 训练数据 → Hermes Agent
│
├── 需要 5000+ 社区技能 → OpenClaw + LinSkills
│
├── 需要容器级沙箱 → Hermes Agent (Docker 硬化)
│
└── 长期使用希望 Agent 自我进化 → Hermes Agent
```

---

## 八、资料来源

| # | 来源 | 类型 | 日期 |
|---|------|------|------|
| 1 | GitHub NousResearch/hermes-agent | 官方文档 | 2026-04 |
| 2 | hermes-agent.nousresearch.com | 官方文档 | 2026-04 |
| 3 | 53AI《从 OpenClaw 到 Hermes Agent》| 博客 | 2026-04-09 |
| 4 | 博客园七牛云 | 博客 | 2026-04-12 |
| 5 | 爱范儿《取代龙虾的是爱马仕》| 媒体报道 | 2026-04-10 |
| 6 | Reddit r/AgentsOfAI | 社区讨论 | 2026-04 |
| 7 | Reddit r/LocalLLaMA | 社区讨论 | 2026-04 |
| 8 | GitHub Issue #5191 | 技术问题 | 2026-04 |
| 9 | 知乎专栏 | 社区文章 | 2026-04 |
| 10 | Linux.do | 社区讨论 | 2026-04 |

---

*调研日期：2026-04-13*
