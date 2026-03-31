# browser-use 调研报告

> 调研时间：2026-03-31
> 调研人：小亮 🐈‍⬛
> 数据来源：GitHub 官方文档 + PyPI + 官方 Discord

---

## 一、项目概览

**GitHub 地址**：https://github.com/browser-use/browser-use

**核心定位**：让 AI Agent 能够控制浏览器，自动完成网页操作任务

| 项目 | 信息 |
|------|------|
| GitHub Stars | **79k+**（增长迅猛） |
| 编程语言 | Python（≥3.11） |
| 开源协议 | AGPL-3.0 |
| 最新维护 | 活跃（2026年持续更新） |
| Discord 社区 | 活跃 |

browser-use 是目前最受欢迎的 AI 浏览器自动化开源库之一，专注于让大语言模型（LLM）能够像真实用户一样操作浏览器——点击、输入、滚动、填表、截图、数据提取等。

---

## 二、核心功能

### 2.1 主要能力

- 🌐 **网页导航与交互**：自动打开网页、点击元素、填写表单、键盘输入、拖拽操作
- 📋 **表单填写**：支持自动填充求职申请、购物、注册等各种表单
- 📸 **截图与状态检查**：获取页面截图、DOM 状态、可视化元素索引
- 🔍 **数据提取**：从网页中提取结构化或非结构化数据
- 🤖 **多步任务自动化**：登录→导航→填表→提交等复杂工作流
- 🔄 **Cookies / Session 管理**：支持持久化登录状态
- 🏗️ **自定义工具扩展**：通过 `@tools.action` 装饰器添加自定义 Python 工具
- 📡 **MCP 服务器支持**：可作为 MCP Server 供其他 AI 工具调用

### 2.2 典型应用场景

| 场景 | 说明 |
|------|------|
| 网页填表 | 自动填写求职申请、调查问卷、注册表单 |
| 购物自动化 | 将购物清单自动加入购物车（Instacart 等） |
| 数据采集 | 抓取产品列表、新闻、评论等 |
| 网站测试 | 端到端测试，用自然语言描述测试步骤 |
| 价格监控 | 监控竞品价格变动并提醒 |
| 邮件/日历操作 | 配合云服务做自动化日程管理 |
| PC 配件选购 | 辅助选购电脑硬件（已有示例） |

### 2.3 官方 Demo 示例

官方 GitHub 仓库提供了 3 个完整的 Demo 视频和代码：

- `apply_to_job.py` — 填写求职申请表（配简历自动填充）
- `buy_groceries.py` — 超市购物车自动填充
- `pcpartpicker.py` — 电脑配件选购辅助

---

## 三、Windows 环境适配

### 3.1 系统支持

browser-use **支持 Windows**，官方文档有明确的 Windows 操作指引。

### 3.2 Windows 安装步骤

**前置要求**：Python ≥ 3.11（建议 3.12）

#### 方式一：使用 uv（推荐）

```bash
# 1. 安装 uv（跨平台 Python 包管理器）
pip install uv

# 2. 创建虚拟环境
uv venv --python 3.12

# 3. 激活虚拟环境（Windows CMD/PowerShell）
.venv\Scripts\activate

# 4. 安装 browser-use
uv pip install browser-use

# 5. 安装 Chromium 浏览器（如果没有的话）
uvx browser-use install
```

#### 方式二：直接 pip

```bash
pip install browser-use
uvx browser-use install   # 安装 Chromium
```

### 3.3 Windows 环境注意事项

| 事项 | 说明 |
|------|------|
| **Chromium 依赖** | 必须安装 Chromium，`uvx browser-use install` 会自动下载 |
| **Playwright 后端** | 底层使用 Playwright，Windows 上运行正常 |
| **浏览器模式** | 支持 `--headed`（有头模式，看得见浏览器窗口）|
| **Chrome Profile** | 支持连接本地已安装 Chrome 的真实 Profile（含 cookies）|
| **CDP 连接** | 支持通过 CDP 协议连接远程 Chrome 或调试端口 |
| **权限** | 管理员权限一般不需要，但部分系统需允许网络访问 |
| **路径问题** | Windows 路径需使用反斜杠（Python 自动处理）|

### 3.4 Windows 有头 / 无头模式

```bash
# 无头模式（默认，后台运行）
browser-use open https://example.com

# 有头模式（可见浏览器窗口）
browser-use --headed open https://example.com
```

### 3.5 Windows 连接真实 Chrome

```bash
# 使用本地 Chrome 的 Default Profile
browser-use --profile "Default" open https://example.com

# 或使用 CDP 自动发现模式
browser-use --connect open https://example.com
```

---

## 四、快速使用指南

### 4.1 环境配置（最小示例）

**第一步：创建项目并安装**

```bash
uv init my-browser-agent
cd my-browser-agent
uv add browser-use
uv sync
```

**第二步：创建 `.env` 文件**

```bash
touch .env   # Linux/macOS
# Windows: echo. > .env
```

`.env` 文件内容（支持多种 LLM 提供者）：

```env
# 方式1：使用 Browser Use 官方优化模型（推荐）
BROWSER_USE_API_KEY=your-key-here

# 方式2：使用 Google Gemini
GOOGLE_API_KEY=your-gemini-key

# 方式3：使用 Anthropic Claude
ANTHROPIC_API_KEY=your-anthropic-key

# 方式4：使用 OpenAI
OPENAI_API_KEY=your-openai-key
```

> API Key 获取地址：
> - Browser Use Cloud: https://cloud.browser-use.com/new-api-key（新用户 5 次免费任务）
> - Google AI Studio: https://aistudio.google.com/app/u/1/apikey
> - Anthropic: https://console.anthropic.com/
> - OpenAI: https://platform.openai.com/api-keys

**第三步：运行第一个 Agent**

```python
# main.py
from browser_use import Agent, Browser, ChatBrowserUse
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    browser = Browser()  # 本地 Chromium

    agent = Agent(
        task="Find the number of stars of the browser-use repo",
        llm=ChatBrowserUse(),  # 官方优化模型
        browser=browser,
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

```bash
python main.py
```

### 4.2 使用其他 LLM

```python
# Anthropic Claude
from browser_use import Agent, ChatAnthropic
llm = ChatAnthropic(model='claude-sonnet-4-0', temperature=0.0)

# Google Gemini
from browser_use import Agent, ChatGoogle
llm = ChatGoogle(model='gemini-flash-latest')

# OpenAI
from browser_use import Agent, ChatOpenAI
llm = ChatOpenAI(model='o3')

# Azure OpenAI
from browser_use import Agent, ChatAzureOpenAI
llm = ChatAzureOpenAI(model='o4-mini')
```

### 4.3 使用 Cloud 模式（更强大）

```python
from browser_use import Agent, Browser, ChatBrowserUse

browser = Browser(use_cloud=True)  # 使用云端隐身浏览器

agent = Agent(
    task="你的任务描述",
    llm=ChatBrowserUse(),
    browser=browser,
)
await agent.run()
```

**Cloud vs Open Source 对比**：

| | 开源版 | Cloud 版 |
|---|---|---|
| 浏览器 | 本地 Chromium | 云端隐身浏览器 |
| 反爬能力 | 一般 | 强（含代理轮换、CAPTCHA 解决）|
| 任务成功率 | 较低 | 高 |
| 集成数量 | 无 | 1000+（Gmail、Slack、Notion 等）|
| 部署方式 | 自托管 | 托管服务 |
| 成本 | 免费（自备 API Key）| 按 token 计费 |
| 适用场景 | 简单任务、自托管 | 复杂任务、生产环境 |

### 4.4 CLI 工具快速上手

```bash
# 初始化项目模板
uvx browser-use init --template default

# 常用 CLI 命令
browser-use open https://example.com        # 打开网页
browser-use state                            # 查看可交互元素
browser-use click 5                          # 点击第5个元素
browser-use type "Hello World"               # 输入文本
browser-use screenshot screenshot.png         # 截图
browser-use close                            # 关闭浏览器
```

---

## 五、接入 Claude Code

browser-use 官方提供了 Claude Code 专用 Skill，安装后可让 Claude Code 具备浏览器自动化能力。

### 5.1 安装步骤

```bash
# 创建 Claude Code Skill 目录
mkdir -p ~/.claude/skills/browser-use

# 下载官方 SKILL.md
curl -o ~/.claude/skills/browser-use/SKILL.md \
  https://raw.githubusercontent.com/browser-use/browser-use/main/skills/browser-use/SKILL.md
```

### 5.2 使用方法

在 Claude Code 中直接用自然语言下达任务，例如：

```
帮我打开 GitHub，搜索 browser-use 仓库，告诉我它的星标数量
```

Claude Code 会自动加载 browser-use Skill，并通过底层 CLI 控制浏览器完成任务。

### 5.3 Skill 核心命令一览

```bash
browser-use open <url>              # 导航
browser-use state                   # 获取可交互元素列表（带索引）
browser-use click <index>           # 按索引点击
browser-use type "text"             # 键盘输入
browser-use screenshot [path]        # 截图
browser-use scroll down              # 滚动
browser-use get html                # 获取页面 HTML
browser-use cookies export <file>   # 导出 Cookies
browser-use wait selector "css"     # 等待元素出现
browser-use --headed open <url>     # 有头模式（可见）
browser-use --profile "Default" open <url>  # 使用 Chrome 真实 Profile
```

### 5.4 支持的 Claude 模型

browser-use Agent 支持以下 Claude 模型（通过 `ChatAnthropic`）：

```python
from browser_use import Agent, ChatAnthropic
llm = ChatAnthropic(model='claude-sonnet-4-0', temperature=0.0)
# 支持 claude-opus、claude-sonnet、claude-haiku 等
```

---

## 六、接入 OpenClaw

### 6.1 方案一：Composio MCP 插件（推荐）

browser-use 可以通过 **Composio** 作为 MCP Server 接入 OpenClaw，实现通过自然语言控制浏览器。

**安装步骤**：

```bash
# 1. 安装 Composio OpenClaw 插件
openclaw plugins install @composio/openclaw-plugin

# 2. 从 https://dashboard.composio.dev/ 获取 API Key

# 3. 配置 OpenClaw
openclaw config set plugins.entries.composio.config.consumerKey "ck_your_key_here"

# 4. 重启 Gateway
openclaw gateway restart
```

**配置文件**（`~/.openclaw/config.yml`）：

```yaml
plugins:
  entries:
    composio:
      enabled: true
      config:
        consumerKey: "ck_your_key_here"
        mcpUrl: "https://connect.composio.dev/mcp"  # 可选，默认就是这个
```

**在 OpenClaw 中使用**：

配置完成后，直接用自然语言让 OpenClaw 操作浏览器，例如：

```
帮我打开 GitHub，搜索 AI Agent 相关项目
```

### 6.2 方案二：OpenClaw 内置 Browser 工具

OpenClaw 自带 Browser 控制工具，**无需额外安装**，但功能和 browser-use 有差距：

| 功能对比 | OpenClaw 内置 | browser-use + Composio |
|----------|--------------|----------------------|
| 基础网页导航 | ✅ | ✅ |
| 元素交互 | ✅ | ✅ |
| AI 智能理解网页 | ❌ | ✅ |
| 反反爬能力 | ❌ | ✅ |
| CAPCHA 解决 | ❌ | ✅ |
| 1000+ App 集成 | ❌ | ✅ |
| 需要额外安装 | ❌ | ✅ |

### 6.3 方案三：直接使用 browser-use Python 库

在 OpenClaw 的 subagent 中直接调用 browser-use Python 代码：

```python
# OpenClaw subagent 中使用
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def run_browser_task(task: str):
    browser = Browser()
    agent = Agent(task=task, llm=ChatBrowserUse(), browser=browser)
    await agent.run()
```

### 6.4 方案四：Chrome DevTools MCP

通过 OpenClaw 的 `chrome-devtools-mcp` 插件连接 browser-use 提供的远程浏览器：

```bash
# 在 OpenClaw Gateway 上启动 chrome-devtools-mcp
npx chrome-devtools-mcp@latest --autoConnect

# 然后通过 browser-use 的 --connect 模式连接
browser-use --connect open https://example.com
```

---

## 七、自定义工具扩展

browser-use 支持通过装饰器添加自定义工具：

```python
from browser_use import Agent, Tools, ActionResult, BrowserSession

tools = Tools()

@tools.action('Ask human for help with a question')
async def ask_human(question: str, browser_session: BrowserSession) -> ActionResult:
    answer = input(f'{question} > ')
    return ActionResult(extracted_content=f'人类回答: {answer}')

agent = Agent(
    task='你的任务',
    llm=llm,
    tools=tools,
)
```

> ⚠️ 注意：参数名必须为 `browser_session`（类型为 `BrowserSession`），否则工具注册会静默失败。

---

## 八、Model Context Protocol (MCP) 支持

### 8.1 browser-use MCP Server

browser-use 可以作为 MCP Server 使用，供任何支持 MCP 的 AI 客户端调用：

```python
# 通过 Composio 调用 browser-use MCP
# 配置 consumerKey 后，工具自动注册到 OpenClaw
```

### 8.2 官方 Claude Code Skill 中的 MCP 集成

browser-use 的 Claude Code Skill 实际上也是基于 MCP 协议实现，提供了一组原子化浏览器操作工具供 Claude Code 调用。

---

## 九、模型性能对比

browser-use 官方在 100 个真实浏览器任务上做了基准测试，结果如下（基于 README 中图表）：

| 模型 | 准确率 | 备注 |
|------|--------|------|
| **ChatBrowserUse (bu-latest)** | ~65% | 官方优化，速度最快（3-5x）|
| Claude Sonnet 4.0 | ~58% | 准确率较高但速度较慢 |
| GPT-4o | ~52% | 中等表现 |
| Gemini Flash | ~45% | 速度最快但准确率较低 |

> 完整基准测试开源：https://github.com/browser-use/benchmark

**ChatBrowserUse 定价（per 1M tokens）**：

| 令牌类型 | bu-latest | bu-2.0（高级版）|
|---------|-----------|---------------|
| 输入 | $0.20 | $0.60 |
| 缓存输入 | $0.02 | $0.06 |
| 输出 | $2.00 | $3.50 |

---

## 十、适用场景总结

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 快速试用 / 简单爬虫 | 开源版 + Gemini | 免费、门槛低 |
| 生产级自动化 | Cloud 版 | 反爬强、成功率高 |
| Claude Code 增强 | Claude Code Skill | 原生集成、体验最好 |
| OpenClaw 增强 | Composio MCP | 功能丰富、跨平台 |
| 自建 AI 应用 | Python SDK | 代码灵活、可定制 |

---

## 十一、风险与注意事项

⚠️ **安全风险**：浏览器自动化工具具有较高系统权限，请务必：
1. 在沙箱环境中运行不信任的任务
2. 不要让 AI Agent 在未授权网站上执行操作
3. 定期检查授权和 Cookie 状态
4. 涉及金融、登录等敏感操作时全程监督

⚠️ **反爬风险**：网站可能检测并封禁自动化浏览器，建议：
- 使用 Cloud 版的隐身浏览器和代理轮换
- 避免高频请求
- 遵守网站的 `robots.txt`

⚠️ **API 成本**：ChatBrowserUse 的输出 token 定价较高（$2/1M），复杂长任务成本需关注。

---

## 十二、相关资源链接

| 资源 | 链接 |
|------|------|
| GitHub 仓库 | https://github.com/browser-use/browser-use |
| 官方文档 | https://docs.browser-use.com |
| Cloud 平台 | https://cloud.browser-use.com |
| Claude Code Skill | https://docs.browser-use.com/llms-full.txt |
| Discord 社区 | https://link.browser-use.com/discord |
| PyPI 页面 | https://pypi.org/project/browser-use/ |
| 官方博客 | https://browser-use.com/posts |
| 基准测试 | https://github.com/browser-use/benchmark |
| Composio 集成 | https://composio.dev/toolkits/browser_tool/framework/openclaw |

---

## 结论与建议

**browser-use** 是一个功能强大、生态完整的 AI 浏览器自动化库，79k+ 的 GitHub Stars 证明了其受欢迎程度。对于开发者来说：

- ✅ **立刻可用**：安装简单，5 分钟跑起来第一个 Agent
- ✅ **灵活接入**：Claude Code、OpenClaw（via Composio）、自建应用均支持
- ✅ **Windows 友好**：官方文档明确支持，安装步骤清晰
- ⚠️ **按需选择**：简单任务用开源免费版，复杂生产任务用 Cloud 版

建议亮老板可以先在本地用开源版体验，对接 OpenClaw 可以通过 Composio 插件实现浏览器增强能力。
