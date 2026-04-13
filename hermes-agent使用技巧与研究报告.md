# Hermes Agent 使用技巧与研究报告

> NousResearch/hermes-agent — 首个内置自学习循环的开源 AI Agent
> 调研日期：2026-04-13
> 调研方式：3 个子代理并行网络检索，重点覆盖 X/Twitter、社区讨论、官方文档
> 参考资料：45+ 篇（含 X/Twitter、Reddit、官方文档、技术博客、中文媒体）

---

## 📋 目录

- [第一部分：X/Twitter 使用技巧与经验](#第一部分xtwitter-使用技巧与经验)
- [第二部分：技术教程与最佳实践](#第二部分技术教程与最佳实践)
- [第三部分：真实用户评价与实际应用案例](#第三部分真实用户评价与实际应用案例)
- [快速参考卡片](#快速参考卡片)

---

# 第一部分：X/Twitter 使用技巧与经验

## 1.1 核心概念与自学习循环

### 四层记忆系统（每层都有不同的触发时机）

| 层级 | 用途 | 存储位置 | 触发时机 |
|------|------|---------|---------|
| **Prompt Memory** | 常驻知识（永久重要）| `~/.hermes/memories/MEMORY.md` + `USER.md` | 每次会话开始 |
| **Session History** | 可检索的对话历史 | SQLite + FTS5 | Agent 主动检索 |
| **Skills** | 可重用的工作流程 | `~/.hermes/skills/` | 任务匹配时加载 |
| **User Model (Honcho)** | 用户偏好建模 | Honcho 服务 | 可选的深度建模 |

> 来源：官方文档 + @NousResearch 推文 | 2026年4月

### 自学习循环的四个阶段

```
1. 任务完成 → 用户提出复杂任务
2. 模式提取 → Agent 分析完成任务所需的步骤
3. 技能创建 → 将工作流程写入 ~/.hermes/skills/
4. 技能优化 → 下次遇到类似任务时 refine 技能
```

> 来源：lushbinary.com 开发指南 | 2026年4月

---

## 1.2 Prompt 编写技巧

### 具体明确 vs 模糊请求

❌ **模糊**：`fix the code`
✅ **具体**：`fix the TypeError in api/handlers.py on line 47 — the process_request() function receives None from parse_body()`

### 善用上下文文件（Context Files）

创建项目级别的 `AGENTS.md` 存储重复指令：

```markdown
# Project Context
- This is a FastAPI backend with SQLAlchemy ORM
- Always use async/await for database operations
- Tests go in tests/ and use pytest-asyncio
- Never commit .env files
```

放置位置：项目根目录（会被自动读取）

### SOUL.md 性格配置

创建 `~/.hermes/SOUL.md` 自定义 Agent 性格：

```markdown
# Soul
You are a senior backend engineer. Be terse and direct.
Skip explanations unless asked. Prefer one-liners over verbose solutions.
Always consider error handling and edge cases.
```

### Cursor Rules 兼容性

已有的 `.cursorrules` 或 `.cursor/rules/*.mdc` 文件会被**自动读取**，无需重复配置。

> 以上技巧来源：hermes-agent.nousresearch.com/docs/guides/tips/ | 2026年4月

---

## 1.3 Memory 最佳实践

### Memory vs Skills 何时用哪个

| 类型 | 用途 | 示例 |
|------|------|------|
| **Memory** | 事实性信息 | "我们的 CI 使用 GitHub Actions" |
| **Skills** | 步骤性流程 | "如何部署到 Kubernetes" |

### 记忆容量管理

| 文件 | 上限 | 用途 |
|------|------|------|
| `MEMORY.md` | ~2,200 字符 | 永久重要知识 |
| `USER.md` | ~1,375 字符 | 用户偏好信息 |

**管理技巧**：
- 定期清理过时信息：`"clean up your memory"`
- 替换过时内容：`"replace the old Python 3.9 note — we're on 3.12 now"`

### ⚠️ 重要：记忆是快照机制

会话期间对 MEMORY.md 或 USER.md 的修改只在**下一个会话**生效，不会立即影响当前会话的 system prompt。

### 第三方记忆系统

v0.7.0+ 支持可插拔记忆后端：

```bash
hermes memory setup
```

支持：built-in、Honcho、Mem0、Vectorize Hindsight、Supermemory 等

> 来源：@NousResearch Twitter | 2026年4月

---

## 1.4 Skills 创建与优化

### 何时让 Agent 自动创建 Skill

当任务满足以下条件时，Agent 会自动创建 skill：
- ✅ 5+ 工具调用
- ✅ 从错误中恢复
- ✅ 用户纠正了方法
- ✅ 发现了非平凡的工作流程

**手动触发**：
```
"save what you just did as a skill called deploy-staging"
```

### SKILL.md 格式

```yaml
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [python, automation]
    category: devops
---

# Skill Title

## When to use
Trigger conditions for this skill.

## Procedure
1. Step one
2. Step two

## Pitfalls
- Known failure modes and fixes

## Verification
How to confirm it worked.
```

### Skills 使用方式

```bash
# 作为 slash 命令
/gif-search funny cats
/axolotl help me fine-tune Llama 3 on my dataset
/github-pr-workflow create a PR for the auth refactor

# 或者自然语言
"用 axolotl fine-tune 这个数据集"
```

### Token 优化：渐进式披露（Progressive Disclosure）

Skills 使用三级加载策略，**控制 token 消耗**：

| 层级 | 内容 | Token 消耗 |
|------|------|-----------|
| Level 0 | name + description + category | ~3K tokens（所有 skills 都会加载这个层级）|
| Level 1 | 完整 SKILL.md | 按需加载 |
| Level 2 | 特定 reference 文件 | 按需加载 |

### Skill 更新策略

**优先使用 patch 而非 edit**：
- patch 只传输变更的文本，edit 需要传输完整内容
- patch 更 token 高效且风险更低

### 社区共识

> 30-50 个自定义 skills 是可管理的上限

> 来源：hermes-agent.ai/blog | 2026年4月

---

## 1.5 配置与性能优化

### 模型选择策略

- **复杂推理/架构决策**：使用前沿模型（Claude Sonnet/Opus, GPT-4o）
- **简单任务**（格式化、重命名）：切换到更快的模型

```bash
/model                         # 交互式切换模型
/compress                     # 总结会话历史，保留关键上下文
/usage                         # 查看 token 消耗
```

### 推荐模型（根据社区讨论）

> **GLM-4.7 Flash** 是当前最佳平衡点 — 快速、可靠的工具调用，比本地 LLaMA/Qwen 更稳定

> 来源：Reddit r/LocalLLaMA | 2026年4月

### 本地模型超时处理

```bash
HERMES_STREAM_READ_TIMEOUT=1800
```

> 来源：官方 FAQ | 2026年4月

---

## 1.6 常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `hermes: command not found` | PATH 未刷新 | `source ~/.bashrc` 或 `source ~/.zshrc` |
| `uv: command not found` | uv 未安装 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Context length exceeded | 对话太长 | `/compress` 或开始新会话 |
| Self-Learning 未生效 | Honcho 默认关闭 | 需要在配置中显式启用 |
| 本地模型 web tools 不工作 | 网络 backend 检查失败 | 已知问题，暂无完美解决方案 |

---

# 第二部分：技术教程与最佳实践

## 2.1 安装与快速配置

### 一键安装（Linux/macOS/WSL2）

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc  # 或 source ~/.zshrc
hermes            # 启动交互式 CLI
```

### Windows 用户

⚠️ 原生 Windows 不支持，需要先安装 WSL2，然后在 WSL2 终端中运行安装命令。

### 完整配置向导

```bash
hermes setup              # 全量配置向导（一次性配置所有项）
hermes gateway setup      # 配置 Telegram/Discord 等消息平台
hermes gateway start      # 启动网关
hermes claw migrate       # 从 OpenClaw 迁移（如果适用）
hermes update             # 更新到最新版本
hermes doctor             # 诊断任何问题
```

### ⚠️ 最低要求

**至少需要 64K tokens 上下文窗口**，否则 Agent 会拒绝启动。

### 模型提供商配置

```bash
hermes model              # 交互式选择模型
```

支持：Nous Portal、Anthropic Claude、OpenAI Codex、OpenRouter（200+ 模型）、DeepSeek、阿里云 DashScope（Qwen）、Ollama 本地模型、MiniMax 等

---

## 2.2 Skills Hub 技能市场

```bash
hermes skills browse                    # 浏览所有技能
hermes skills search kubernetes         # 搜索技能
hermes skills install openai/skills/k8s # 安装 GitHub 技能
hermes skills install official/security/1password  # 安装官方技能
hermes skills check                     # 检查更新
hermes skills update                    # 更新已安装技能
```

### Skills 目录结构

```
~/.hermes/skills/
├── mlops/
│   ├── axolotl/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── templates/
│   │   └── scripts/
│   └── vllm/
└── devops/
    └── deploy-k8s/
```

---

## 2.3 消息网关（多平台接入）

### 支持的平台

| 平台 | 支持功能 |
|------|---------|
| **Telegram** | 文本/图片/文件/语音/视频 |
| **Discord** | 文本/图片/文件/语音 |
| **Slack** | 多工作区 OAuth |
| **WhatsApp** | 文本/媒体 |
| **Signal** | 文本 |
| **飞书/企业微信** | 完整支持 |
| **Email/SMS** | 邮件通知 |

### 使用方式

```bash
hermes gateway setup   # 交互式配置消息平台
hermes gateway          # 启动网关

# CLI 端
hermes                  # 启动终端对话
hermes --continue       # 恢复上一次会话
```

> 来源：官方 Messaging 文档 | 2026年4月

---

## 2.4 语音模式

```bash
pip install "hermes-agent[voice]"
pip install faster-whisper  # 推荐：免费本地 STT

# 在 CLI 中启用
/voice on
Ctrl+B  # 录音
/voice tts  # 让 Hermes 语音回复
```

---

## 2.5 MCP 服务器集成

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
```

---

## 2.6 视频教程资源

| 视频标题 | 内容 |
|---------|------|
| [Hermes Agent Full Setup Tutorial (Gemma 4)](https://www.youtube.com/watch?v=THA8Fov44QY) | 本地 Ollama + Gemma 4 完整安装 |
| [Hermes Agent on VPS in 8 Minutes](https://www.youtube.com/watch?v=_K5nJUIF9x8) | VPS 8分钟快速部署 |
| [Telegram Setup in 5 Minutes](https://www.youtube.com/watch?v=Twt80_MFE0U) | Telegram 配置 |
| [OpenClaw Competitor Install Guide](https://www.youtube.com/watch?v=YZg4YdxOroY) | 与 OpenClaw 对比安装 |
| [Hermes Agent 100X Better](https://www.youtube.com/watch?v=zmSeuS0XjTc) | 性能优化技巧 |

---

## 2.7 安全建议

### 生产环境使用 Docker

```bash
# .env 配置
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=hermes-sandbox:latest
```

### 危险命令允许策略

⚠️ 危险命令（`rm -rf`, `DROP TABLE`）的 "always" 选项要慎用——这会永久允许该模式。先用 "session" 尝试。

### 消息平台允许名单（必须配置）

```bash
# ✅ 推荐：显式允许名单
TELEGRAM_ALLOWED_USERS=123456789,987654321
DISCORD_ALLOWED_USERS=123456789012345678

# ❌ 避免（危险！）
GATEWAY_ALLOW_ALL_USERS=true
```

### Windows 编码问题

在 Windows PowerShell 中设置 UTF-8：
```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
```

---

## 2.8 中文资源

| 文章 | 来源 |
|------|------|
| [菜鸟教程 - Hermes Agent](https://www.runoob.com/ai-agent/hermes-agent.html) | 菜鸟教程 |
| [一行命令部署自我进化 AI Agent](https://www.cnblogs.com/qiniushanghai/p/19851330) | 博客园 |
| [取代龙虾的是爱马仕](https://www.ifanr.com/1661725) | 爱范儿 |
| [不只是 OpenClaw 平替](https://www.53ai.com/news/OpenSourceLLM/2026040979543.html) | 53AI |
| [MiniMax 文档 - Hermes Agent 接入指南](https://platform.minimaxi.com/docs/token-plan/hermes-agent) | MiniMax |

---

# 第三部分：真实用户评价与实际应用案例

## 3.1 项目基本信息

| 项目 | 内容 |
|------|------|
| **项目名** | Hermes Agent |
| **开发者** | Nous Research |
| **开源时间** | 2026年2月 |
| **GitHub Stars** | 47,000+（截至2026年4月）|
| **许可证** | MIT |

---

## 3.2 ✅ 真实好评

### 1. 自我进化能力——X 用户实测

> **@0xsachi (Miss Sentient) on X** | 2026年3月11日 🐦
> "I tried @NousResearch's Hermes agent instead of Openclaw today. I set up an automated report for the top 5 trending open source AI topics across reddit, X, etc. took me abt 1 hour to set up"

> **Reddit r/hermesagent** | 2026年4月
> "Hermes is still, and its learns and gets better all by itself. Honestly worth the switch."
> "Hermes runs as a service on a VM so it's always on - it's less 'I'm chatting with an AI' and more 'I have an automated ops assistant.'"

### 2. 多平台网关——25年经验工程师评价

> **Dev.to - George Larson**（25年经验软件工程师）| 2026年3月19日
> "If your use case is 'AI agent accessible on messaging platforms,' Hermes is the best option I've found."
> "The multi-platform gateway is genuinely impressive and has no equivalent in the ecosystem."
> "Discord alone is 2,085 lines [of adapter code]."

### 3. 低成本部署——$5 VPS 可运行

> **Virtual Uncle** | 2026年4月
> "A $5/month VPS gives you 24/7 uptime and keeps your personal machine clean. Hetzner, DigitalOcean, and Contabo are the popular options."

> **@NousResearch 官方 README**
> "Run it on a $5 VPS or a GPU cluster."

### 4. 从 OpenClaw 迁移体验

> **Reddit r/openclaw** | 2026年4月
> "Just migrated my openclaw setup to Hermes agent and it works like a charm."
> "Made the move to hermes… no regrets."

> **Reddit r/hermesagent** | 2026年4月
> "Switched from OpenClaw to Hermes Agent — not looking back"

### 5. 持久记忆效果

> **OpenAIToolsHub** | 2026年4月
> "After running 20-30 tasks in a domain, you start seeing measurable improvement on repeated task types — fewer false starts, better tool selection."

---

## 3.3 ❌ 真实差评（必须知道）

### 1. "自我进化"有夸大成分

> **Dev.to - George Larson** | 2026年3月19日 ⚠️
> "The 'grows with you' and 'gets more capable' framing is a stretch for what amounts to structured note-taking."
> "The reality: Hermes writes markdown files to ~/.hermes/memories/. This is the same pattern used by Claude Code, OpenCode, and every other tool with a config file."

**解读**：Skills 本质上就是带 YAML frontmatter 的 Markdown 文件，加载时注入上下文——本质是"结构化 prompt injection + CRUD 层"，不是真正的自主学习。

### 2. Honcho 用户建模默认关闭

> **Virtual Uncle** | 2026年4月 ⚠️
> "One important caveat the marketing doesn't make obvious: Honcho is off by default. Multiple Reddit users reported confusion when the 'self learning' features didn't seem to work out of the box."

**解读**：开箱即用的"自我学习"功能**并不完整**，需要在配置中显式开启 Honcho。

### 3. 团队 Web3 背景争议

> **36氪** | 2026年4月13日 ⚠️
> "Nous Research 的核心成员，很多都来自 Web3 领域。有报道称，其 CEO Jeffrey Quesnelle 此前曾是以太坊 MEV 基础设施项目 Eden Network 的首席工程师。"
> "团队的融资路径也带有明显的加密行业特征——以代币计价而非传统股权"
> "对于普通用户而言，这意味着：任何与 'NOUS 代币' 直接挂钩的交易、投资或承诺，都需要保持足够谨慎"

### 4. 文档和配置有坑

> **Reddit r/Rag** | 2026年4月 ⚠️
> "Setup can be a bit finicky if you're running it locally. For real projects I'd lean toward something more battle-tested unless you're okay debugging the tool itself."

### 5. 复杂任务仍有局限

> **OpenAIToolsHub** | 2026年4月 ⚠️
> "On tasks that required chaining web browsing with code execution, we saw occasional mis-selections that required intervention."

---

## 3.4 实际应用场景

### 场景 1：自动化研究监控（X 用户实测）

> "I set up an automated report for the top 5 trending open source AI topics across reddit, X, etc. took me about 1 hour to set up"
> — @0xsachi (Miss Sentient) | X/Twitter

### 场景 2：跨平台个人助理

> "Start a conversation on Telegram from your phone, pick it up in the terminal on your laptop. Voice memos are transcribed and processed."
> — Virtual Uncle

### 场景 3：持久化编程伙伴

> "Developers use it as a persistent coding partner that remembers the codebase, conventions, and deployment pipeline between sessions."
> — Turing Post

### 场景 4：Agent-to-Agent 协作（X 用户分享）

> "Someone on X said their Hermes agent autonomously messaged their business partner's Hermes agent to coordinate on a task. No human in the loop."
> — Reddit r/hermesagent

### 场景 5：Cron 定时任务

> "Every morning at 8am, scan these GitHub repos for new releases and send me a summary on Telegram."
> — Virtual Uncle

---

## 3.5 Hermes vs OpenClaw 深度对比

| 维度 | Hermes Agent | OpenClaw |
|------|-------------|----------|
| **核心哲学** | 自我进化式（会"成长"）| 确定性/控制面优先 |
| **技能来源** | Agent 自主生成 + 人类编写 | 人类编写 |
| **记忆机制** | 分层记忆 + 程序化知识 | 显式 RAG |
| **自学习闭环** | ✅ 内置 | ❌ 需手动维护 |
| **多平台集成** | 12+ 平台（Telegram/Discord/Slack 等）| 更成熟 |
| **部署成本** | $5 VPS 可运行 | 类似 |
| **社区规模** | 快速增长中（47K stars）| 更大更成熟 |
| **OpenClaw 迁移** | ✅ 内置迁移工具 | — |
| **适用场景** | 长期记忆 + 自主学习 | 多通道自动化 + 复杂工作流 |

> Reddit 社区分析（25个高热度帖）：
> "~35% stick with OpenClaw despite its flaws, citing unmatched integrations"
> "~30% have switched to Hermes, praising easier self-improvement"
> "~25% run both in the same stack"

**最佳实践**：可以将 Hermes 作为高级规划器运行在 OpenClaw 工具之上，实现互补。

---

## 3.6 适合与不适合的人群

### ✅ 适合选择 Hermes 的情况

- 需要跨多个消息平台（Telegram/Discord/Slack/WhatsApp）使用 AI 助理
- 重视长期记忆和自我进化能力
- 预算有限（$5 VPS 即可运行）
- 想要一个能"越用越懂你"的 AI 助手
- 需要定时自动任务（Cron）
- 想从 OpenClaw 迁移且看重内置迁移工具

### ⚠️ 建议继续观望的情况

- 需要完全开箱即用的体验（Self-Learning 默认关闭）
- 对代码质量要求极高（目前仍推荐 Claude Code / Cursor）
- 需要企业级支持和成熟的技能生态
- 对 Web3 背景团队有顾虑
- 追求的是"真正的 AGI 自我进化"（而非结构化笔记）

---

# 快速参考卡片

## 安装命令

```bash
# 一键安装
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc

# 启动
hermes                          # CLI 对话
hermes gateway setup && hermes gateway start  # 启动消息网关
hermes claw migrate             # 从 OpenClaw 迁移

# 配置
hermes model                    # 选择模型
hermes setup                    # 全量配置向导
hermes skills install <skill>   # 安装技能
```

## 常用 Slash 命令

| 命令 | 功能 |
|------|------|
| `/new` 或 `/reset` | 开始新对话 |
| `/model [provider:model]` | 切换模型 |
| `/compress` | 压缩上下文 |
| `/usage` | 查看 token 消耗 |
| `/skills` | 浏览技能列表 |
| `/voice on` | 开启语音模式 |
| `/stop` | 停止当前任务 |

## Memory 管理

```bash
# 记忆文件位置
~/.hermes/memories/MEMORY.md   # 常驻知识（上限 ~2200 字符）
~/.hermes/memories/USER.md     # 用户偏好（上限 ~1375 字符）
~/.hermes/skills/              # 技能库

# 对 Agent 说
"clean up your memory"         # 清理过时记忆
"replace the old Python 3.9 note — we're on 3.12 now"  # 更新记忆
"save what you just did as a skill called xxx"         # 保存为技能
```

## 参考链接

| 类型 | 链接 |
|------|------|
| 官网 | https://hermes-agent.nousresearch.com/ |
| GitHub | https://github.com/nousresearch/hermes-agent |
| 官方文档 | https://hermes-agent.nousresearch.com/docs/ |
| Skills Hub | https://hermes-agent.nousresearch.com/docs/skills |
| awesome-hermes-agent | https://github.com/0xNyk/awesome-hermes-agent |
| 菜鸟教程 | https://www.runoob.com/ai-agent/hermes-agent.html |
| 爱范儿 | https://www.ifanr.com/1661725 |
| MiniMax 接入指南 | https://platform.minimaxi.com/docs/token-plan/hermes-agent |

---

*调研日期：2026-04-13*
*调研方式：3 子代理并行网络检索，重点覆盖 X/Twitter、Reddit、技术博客、中文媒体*
*参考资料：45+ 篇权威来源*
