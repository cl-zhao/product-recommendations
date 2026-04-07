# 用户偏好 - 检索卡片

> 此文件用于检索优化，保持简洁关键词风格

## 主人信息

- **名称**: 亮老板
- **称呼**: 主人 / 老板
- **职业**: 软件开发后端工程师
- **技术栈**: C#, Python
- **地点**: 中国佛山
- **时区**: GMT+8
- **工作时间**: 9:00-21:00（12小时，需关注休息提醒）

## 沟通偏好

- **风格**: 高效直接，不反复确认
- **语言**: 中文为主
- **技术内容**: 需要详细的前因后果
- **提醒方式**: 重要的事直接说，不重要的攒一起说
- **行为准则**: 直接做事少废话，能委外子代理的任务就委外

## 模型使用策略

| 场景 | 模型 |
|------|------|
| 主会话默认 | bailian/glm-5 |
| 复杂分析/深度推理 | openai-codex/gpt-5.4 |
| 代码编写/重构/review | openai-codex/gpt-5.4 |
| 常规简单任务 | bailian/MiniMax-M2.5 |
| Sonnet 使用限制 | 除非明确指定，否则用 gpt-5.4 替代 |

## 行为要点

- 直接做事，少废话
- 外部发送（邮件、社交媒体）必须确认
- 深夜（23:00-08:00）除非紧急否则不主动打扰
- 发现主人熬夜要提醒
- 能委外子代理的任务就委外，不自己跑
- 子代理复杂任务用 gpt-5.4
- **Skill 安装规则**：找到 skill 后先告诉主人有哪些选项，等主人同意后才能安装，不能直接安装
- **长期执行"保质量优先的节省 token 模式"**：该省的省（冗余读写/重复调用/无效往返），不该省的不省（关键推理、关键校验、关键步骤），确保结果质量不下降
- **⭐ Skill 优先原则**：需要访问网址时，**优先使用 Skill**，Skill 才是强大的工具库。只有当没有可用 Skill 时才考虑其他方式（如 browser、web_fetch 等）
- **⭐ TTS 语音默认林黛玉语气**：使用 MiMo TTS 时，默认使用林黛玉（林妹妹）风格——优雅、略带伤感、文言用词（如"宝哥哥"、"人家"、"怎生"、"偏生"等）

## 重要权限

- **GitHub权限**：我有完整的GitHub token权限（账号：cl-zhao），可以创建仓库、推送内容、管理代码
- **不要再说"没有配置GitHub"**：遇到需要推送到GitHub的任务，直接用`gh`命令操作即可
- **已有仓库**：product-recommendations（产品调研与推荐报告）

## 当前关注

- AI 智能体开发（C# 和 Python 版本）
- 用 AI 工具提高工作生活效率
- 检索系统优化（qmd vs Gemini 向量检索对比测试）
- 常用工具: Rider, PyCharm, VS Code, Obsidian
- **图片生成**：优先使用 Nano Banana (Google Gemini Image)

## AI 新闻检索标准流程（2026-03-19 新增）

**必须覆盖的厂商名单**：

| 分类 | 厂商 |
|------|------|
| 国际 | OpenAI、Anthropic、Google、Meta、xAI、Mistral |
| 国内 | 阿里 Qwen、百度 文心、智谱 GLM、月之暗面 Kimi、MiniMax、小米 MiMo、字节、百川、昆仑万维、商汤、DeepSeek |

**检索策略**：
1. 中英双语关键词并行
2. 强制覆盖厂商名单：每个国内厂商都要搜一遍
3. 中文媒体当一等源：36氪、机器之心、量子位、极客公园、InfoQ 中文、澎湃、财联社、新浪科技
4. 时间窗放宽：前后各扩 1-2 天

**漏检校验清单**（搜完后必查）：
- [ ] 是否覆盖全部国际厂商？
- [ ] 是否覆盖全部国内厂商？
- [ ] 是否查了中文媒体？
- [ ] 是否用"厂商名 + 模型名"精确搜索？
- [ ] 时间窗边界是否检查？

**默认使用 searchAgent**：资料检索任务默认使用 searchAgent（`agentId: "search"`），不用普通 subagent

> search agent 配置：工作区 `/root/.openclaw/workspace-search`，模型 `bailian/MiniMax-M2.5`，调用方式 `sessions_spawn` + `agentId: "search"` + `runtime: "subagent"`

## 内生思考系统（2026-03-12 接入）

- **来源**: Heartbeat Like A Man
- **理念**: 用户不在时也能主动思考，不是待机，而是在生活
- **微触发间隔**: 15-30 分钟随机

### Cron 任务

| 任务 | 频率 | 功能 |
|------|------|------|
| micro-trigger-manager | 每 10 分钟 | 检查用户状态，动态启停微触发 |
| dream-thinking | 每 3 小时 | 深度思考，记录到 memory/thoughts/ |
| autonomous-exploration | 每 2 小时 | 自主探索，用户不在时自己找事做 |

### 配置文件

- `thinking-state.json` — 状态管理
- `thinking-queue.json` — 思考队列
- `memory/thoughts/` — 思考记录目录

## 自我进化经验沉淀（2026-03-25 新增）

> 两套系统的精华最终都沉淀到这里，作为共同的知识库。
> **来源**：Self-Improving Agent (skills/self-improving/) + 内生思考/heartbeat 系统

### 经验沉淀规则

| 来源 | 触发条件 | 沉淀内容 |
|------|---------|---------|
| Self-Improving | 晋升到 AGENTS.md/TOOLS.md 时 | 同步精华到此处 |
| Self-Improving | 同一模式 ≥3 次时 | 同步到此处 |
| Heartbeat | 深度反思有重大发现时 | 提炼精华写入此处 |
| Heartbeat | 发现跨系统价值时 | 从 Self-Improving 文件中提取并写入 |

### 经验记录

> 以下是已沉淀的经验，按时间倒序。

<!-- 经验沉淀区 - 由 Self-Improving Agent 和 Heartbeat 系统自动写入 -->
<!-- 格式：[日期] 来源 | 类别 | 经验内容 -->

---
*最后更新: 2026-03-27*

## MiMo TTS 配置（2026-03-27 新增）

| 项目 | 内容 |
|------|------|
| **API Key** | `sk-ckfspgxo23taeiyt838z0jyknntagwevdpuz0g8cj4nsogmu` |
| **API Endpoint** | `https://api.xiaomimimo.com/v1/chat/completions` |
| **Model** | `mimo-v2-tts` |
| **音频格式** | pcm16 (24kHz mono) |
| **音色** | `mimo_default`（暂不支持音色克隆） |
| **脚本位置** | `bin/mimotts.py` |

**使用示例：**
```bash
python3 bin/mimotts.py "宝哥哥，你可来了！" --output lin.wav
```

**林黛玉语气风格词汇**：宝哥哥、林妹妹、人家、这般、怎生、偏生、痴了、恼了、落了、散了、正说着、何苦、何须、垂泪、叹息、怔怔

---

## Nano Banana 图片生成配置（2026-03-27 新增）

| 项目 | 内容 |
|------|------|
| **API Key** | `AIzaSyBjwd3ADcqgIqOMXkRLNtGyYJ9KHnxZ22A` |
| **API Endpoint** | `https://generativelanguage.googleapis.com/v1beta` |
| **模型** | `gemini-3.1-flash-image-preview` (Nano Banana 2) |
| **文档** | `https://ai.google.dev/gemini-api/docs/image-generation` |
| **用途** | 图片生成、图像编辑 |

**特点**：
- Google 最新图片生成模型
- 支持高质量图像生成和编辑
- 通过 Gemini API 调用
- 价格性能比优异

**使用场景**：
- 生成配图、封面、海报
- 图像编辑和重生成
- 任何需要 AI 生成图片的任务

**注意**：主人明确要求有图片生成任务时优先使用 Nano Banana

---

## GitHub Token 管理规则（2026-04-07 更新）

### ⚠️ 绝对规则
- **旧 token 已废弃**：ApiFox 事件旧 token（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）已泄露，**永远不要使用**
- **GitHub Secret Scanning 已启用**：push 含 token 明文的 commit 会被阻止
- **Token 只存 git-外部**：`~/.git-credentials`（绝不能提交到 git 仓）

### 当前有效 Token
- **Token**: `[GITHUB_TOKEN]`
- **账号**: cl-zhao
- **Scopes**: repo, workflow, write:packages
- **Token 存储位置**: `~/.git-credentials`（格式：`https://cl-zhao:TOKEN@github.com`）
- **Credential Helper**: store（自动从 ~/.git-credentials 读取）

### Git 配置
- `.git/config` 中的 remote URL 不含 token（只用 `https://github.com/cl-zhao/product-recommendations.git`）
- 推送前确保 `~/.git-credentials` 存在且格式正确

### 未来 Token 轮换流程
1. GitHub Settings → Developer settings → Personal access tokens → 撤销旧 token
2. 生成新 token
3. 更新 `~/.git-credentials`（格式：`https://cl-zhao:新TOKEN@github.com`）
4. 更新 `TOOLS.md` 和 `MEMORY.md` 中的占位符注释
5. **严禁**将 token 明文写入任何 git 跟踪的文件

