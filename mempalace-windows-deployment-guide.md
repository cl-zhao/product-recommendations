# MemPalace Windows 部署与快速使用教程

> 本教程面向 Windows 用户，系统讲解如何在 Windows 上部署 MemPalace，并连接 Claude Code / Codex CLI 实现 AI 记忆功能。
>
> **最后更新**：2026-04-08｜基于 MemPalace v3.0.0 官方文档

---

## 目录

1. [前置认知：MemPalace 是什么](#1-前置认知mempalace-是什么)
2. [Windows 部署方案选择](#2-windows-部署方案选择)
3. [方案一：WSL（推荐）—— 完整兼容](#3-方案一wsl推荐--完整兼容)
4. [方案二：原生 Windows（部分兼容）](#4-方案二原生-windows部分兼容)
5. [安装后初始化](#5-安装后初始化)
6. [挖掘数据：建立你的记忆库](#6-挖掘数据建立你的记忆库)
7. [连接 Claude Code](#7-连接-claude-code)
8. [连接 Codex CLI](#8-连接-codex-cli)
9. [自动保存 Hooks 配置](#9-自动保存-hooks-配置)
10. [常用命令速查](#10-常用命令速查)
11. [架构速览：Palace 结构解析](#11-架构速览palace-结构解析)
12. [Windows 常见问题](#12-windows-常见问题)

---

## 1. 前置认知：MemPalace 是什么

MemPalace 是一个**本地运行的 AI 记忆系统**，核心理念来自古希腊演说家的"记忆宫殿"：

- **存储方式**：原始对话 verbatim 存储到 ChromaDB，不摘要，96.6% LongMemEval R@5
- **无需 API**：完全本地运行，不联网，不收费
- **AAAK 压缩**：实验性方言，将上下文压缩到 ~170 token（详见官方说明，v3.0.0 诚实披露了 AAAK 的局限性）
- **MCP 协议**：暴露 19 个工具，供 Claude Code 等 AI 工具调用
- **知识图谱**：SQLite 时序三元组（谁做了什么、什么时候、持续多久）
- **版本**：v3.0.0（2026-04-06）
- **依赖**：Python 3.9+、chromadb>=0.5.0,<0.7、pyyaml>=6.0

> ⚠️ **官方坦诚说明**（来自 GitHub README）：
> - AAAK 并非"30x 无损压缩"，实测在 LongMemEval 上 AAAK 模式（84.2%）低于 raw 模式（96.6%）
> - "+34% palace boost" 是 ChromaDB 元数据过滤的标准功能
> - 矛盾检测（fact_checker.py）尚未接入 KG ops

---

## 2. Windows 部署方案选择

### 三种 Windows 部署路径对比

| 方案 | Claude Code | Codex CLI | MemPalace CLI | Hooks | ChromaDB | 推荐度 |
|------|------------|-----------|--------------|-------|---------|--------|
| **WSL（Linux 子系统）** | ✅ 完美支持 | ✅ 完美支持 | ✅ 完美支持 | ✅ bash 原生 | ✅ 无问题 | ⭐⭐⭐⭐⭐ |
| **原生 Windows + Git Bash** | ✅ 支持 | ✅ MCP 可用 | ⚠️ 部分支持 | ❌ bash脚本无法用 | ⚠️ 可能有编译问题 | ⭐⭐ |
| **原生 Windows + PowerShell** | ✅ 支持 | ✅ MCP 可用 | ⚠️ 部分支持 | ❌ 需改写 | ⚠️ 可能有编译问题 | ⭐ |

### 关键限制说明

1. **MemPalace Hooks 是 bash 脚本**（`.sh`）：原生 Windows 无法直接运行，WSL 环境可完美支持
2. **ChromaDB 依赖 hnswlib**：在 Windows 原生环境可能遇到 C++ 编译错误（CMake 要求），WSL 无此问题
3. **Codex CLI Hooks 在 Windows 上已声明临时禁用**：官方文档明确标注"Windows support temporarily disabled"
4. **MemPalace MCP**：Codex CLI 仅支持 STDIO 传输模式（不支持 SSE/HTTP 远程），本地 STDIO 模式两者均可正常工作

### 结论

> **强烈推荐 WSL 方案**。WSL 提供完整的 Linux 环境，MemPalace 的所有功能均可无差别运行。原生 Windows 方案可作为轻量备用，但 hooks 自动保存功能将无法使用。

---

## 3. 方案一（推荐）：WSL —— 完整兼容

### 3.1 启用 WSL

以**管理员身份**打开 PowerShell，运行：

```powershell
wsl --install
```

重启电脑后，Ubuntu 会自动安装并提示设置用户名密码。

> **推荐 Ubuntu 22.04 或更高版本**。WSL 2 性能更优且支持 sandbox（如果需要）。

验证 WSL 版本（Ubuntu 中运行）：

```bash
wsl --set-version Ubuntu 2   # 如果默认是 WSL 1，升级到 WSL 2
wsl --status                 # 查看状态
```

### 3.2 安装 Python 和 pip

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装 Python 3 和 pip
sudo apt install -y python3 python3-pip python3-venv

# 验证版本
python3 --version
pip3 --version
```

> MemPalace 要求 Python 3.9+。Ubuntu 22.04 默认 Python 3.10，满足要求。

### 3.3 安装 MemPalace

```bash
# 安装（推荐使用虚拟环境）
python3 -m venv ~/.mempalace-venv
source ~/.mempalace-venv/bin/activate

# 安装 MemPalace
pip install mempalace

# 验证安装成功
mempalace --version
# 或
python3 -m mempalace --version
```

### 3.4 配置 PATH（可选，方便全局调用）

```bash
# 将虚拟环境添加到 PATH（添加到 ~/.bashrc）
echo 'alias mempalace="~/.mempalace-venv/bin/python3 -m mempalace"' >> ~/.bashrc
source ~/.bashrc

# 验证
mempalace --help
```

### 3.5 初始化记忆宫殿

```bash
# 创建一个工作目录（用于存放 palace 数据）
mkdir -p ~/mempalace-palace

# 初始化（引导式配置）
mempalace init ~/mempalace-palace

# 交互式配置会询问：
# - 你的名字/身份
# - 主要项目名称
# - 人员名单
# 这会生成 ~/.mempalace/identity.txt 和 ~/.mempalace/wing_config.json
```

> 初始化后，数据默认存储在 `~/.mempalace/` 目录，包含 ChromaDB 向量库和 SQLite 知识图谱。

### 3.6 配置 WSL 与 Windows 文件互操作

MemPalace 部署在 WSL 中，但你的项目文件通常在 Windows 文件系统（`/mnt/c/`）。

```bash
# MemPalace 数据存在 WSL 本地（推荐）
# 项目/对话文件从 Windows 挂载路径访问：
ls /mnt/c/Users/你的用户名/Documents/MyProject

# 在 WSL 中挖掘 Windows 目录的对话：
mempalace mine /mnt/c/Users/你的用户名/Documents/chats --mode convos
```

> 注意：ChromaDB 数据库文件必须保持在 WSL Linux 文件系统内（`~/.mempalace/`），不能放在 `/mnt/c/`（Windows NTFS 文件系统性能差且可能有权限问题）。

### 3.7 启动 MCP Server

在 WSL 终端中运行：

```bash
# 方式一：直接运行 MCP server（Codex CLI / Claude Code 会自动连接）
~/.mempalace-venv/bin/python3 -m mempalace.mcp_server

# 方式二：后台运行
nohup ~/.mempalace-venv/bin/python3 -m mempalace.mcp_server > ~/.mempalace/mcp_server.log 2>&1 &
echo $! > ~/.mempalace/mcp_server.pid

# 停止后台服务
# kill $(cat ~/.mempalace/mcp_server.pid)
```

---

## 4. 方案二：原生 Windows（部分兼容）

> ⚠️ 本方案适用于无法使用 WSL 的场景。但 **Hooks 自动保存功能不可用**，MemPalace 的核心搜索功能不受影响。

### 4.1 安装 Git for Windows（必需）

下载地址：https://git-scm.com/downloads/win

安装时建议选择：
- **Git Bash**：作为默认终端
- **Checkout Windows-style, commit Unix-style**：处理行尾符问题

### 4.2 安装 Python（Windows）

两种方式：

**方式 A（推荐）：Microsoft Store**
```
开始菜单 → 搜索 "Python" → 安装 Python 3.11 或更高版本
```
验证：
```powershell
python --version
python -m pip --version
```

**方式 B：python.org 官网**
- 下载地址：https://www.python.org/downloads/windows/
- 安装时**务必勾选** "Add Python to PATH"
- 验证：`python --version`

### 4.3 安装 MemPalace

以**管理员身份**打开 PowerShell 或 Git Bash：

```powershell
# PowerShell 或 Git Bash 中运行
python -m pip install mempalace

# 权限问题？加 --user
python -m pip install mempalace --user

# 验证
mempalace --version
```

#### ChromaDB 安装问题（已知问题）

ChromaDB 的 hnswlib 依赖在 Windows 上可能编译失败，错误类似：

```
Building wheel for hnswlib ... error
CMake Error: The C++ compiler ... not found
```

**解决方案 A（推荐）：使用预编译 wheel**
```powershell
pip install --only-binary=:all: chromadb
pip install mempalace
```

**解决方案 B：安装 Visual Studio Build Tools**
1. 下载 Visual Studio Build Tools 2022
2. 安装时选择 "C++ Build Tools"
3. 重试：`pip install mempalace`

**解决方案 C：使用 WSL（最省事）**

### 4.4 初始化

```powershell
# PowerShell 或 CMD 中
mempalace init C:\Users\你的用户名\mempalace-palace
```

### 4.5 原生 Windows 的 Hooks 限制

MemPalace 提供的两个 hook 脚本是 bash 脚本：

- `hooks/mempal_save_hook.sh`（每15条消息自动保存）
- `hooks/mempal_precompact_hook.sh`（上下文压缩前保存）

**原生 Windows 无法直接运行 `.sh` 脚本**。如果你使用 WSL，这些脚本可以直接使用。如果坚持原生 Windows，可以手动触发保存或等待后续社区提供 PowerShell 版本。

---

## 5. 安装后初始化

### 5.1 初始化详解

```bash
# 运行初始化（交互式）
mempalace init ~/mempalace-palace
```

初始化会创建以下配置文件（位于 `~/.mempalace/`）：

```
~/.mempalace/
├── identity.txt      # 你的身份描述（L0 层，~50 tokens，每会话加载）
├── wing_config.json  # wing 映射配置（谁、什么项目）
├── palace/           # ChromaDB 向量数据库
│   ├── chroma.sqlite
│   └── ...
└── kg.db             # SQLite 知识图谱
```

### 5.2 手动编辑身份文件

```bash
# 编辑身份描述
nano ~/.mempalace/identity.txt
# 或
notepad ~/.mempalace/identity.txt
```

示例内容：
```
我是亮老板，一名后端工程师。
当前项目：C# AI智能体、Python AI智能体。
常用工具：Rider, PyCharm, VS Code, Obsidian。
关注领域：AI 智能体开发、RAG 系统、Python/C# 全栈。
```

### 5.3 手动配置 Wing

编辑 `~/.mempalace/wing_config.json`：

```json
{
  "default_wing": "wing_general",
  "wings": {
    "wing_kai": {
      "type": "person",
      "keywords": ["kai", "kai's", "Kai"]
    },
    "wing_product_recommendations": {
      "type": "project",
      "keywords": ["product-recommendations", "产品推荐", "调研报告"]
    }
  }
}
```

---

## 6. 挖掘数据：建立你的记忆库

### 6.1 三种挖掘模式

```bash
# 模式 1：项目文件（代码、文档、笔记）
mempalace mine ~/projects/myapp

# 模式 2：对话记录（Claude Code / ChatGPT 导出）
mempalace mine ~/chats/ --mode convos

# 模式 3：通用（自动分类为决策、偏好、里程碑、问题、情感上下文）
mempalace mine ~/chats/ --mode convos --extract general
```

### 6.2 指定 Wing

```bash
# 为挖掘的内容指定 wing（方便后续按项目筛选）
mempalace mine ~/chats/claude-sessions/ --mode convos --wing product-recommendations
mempalace mine ~/chats/python-agent/ --mode convos --wing python-agent
```

### 6.3 分割合并的对话文件

有些对话导出工具会把多个会话合并到一个大文件里，需要先分割：

```bash
# 预览分割方案
mempalace split ~/chats/combined.json --dry-run

# 执行分割（分成每个会话一个文件）
mempalace split ~/chats/combined.json

# 只分割包含 3+ 个会话的文件
mempalace split ~/chats/ --min-sessions 3
```

### 6.4 挖掘完成后验证

```bash
# 查看 palace 概况
mempalace status
```

输出示例：
```
=== MemPalace Status ===
Total drawers: 342
Wings: 3 (wing_product_recommendations, wing_python_agent, wing_general)
Rooms: 17
Protocol: PALACE_PROTOCOL v1
AAAK dialect: loaded (experimental)
```

### 6.5 搜索验证

```bash
# 搜索测试
mempalace search "上次讨论的数据库选型"

# 在指定 wing 中搜索
mempalace search "auth 决策" --wing product-recommendations

# 在指定 room 中搜索
mempalace search "API 设计" --wing python-agent --room api-design
```

---

## 7. 连接 Claude Code

### 7.1 Claude Code 安装（Windows）

**方式 A（推荐）：PowerShell**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**方式 B：CMD**
```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**方式 C：WinGet**
```powershell
winget install Anthropic.ClaudeCode
```

**方式 D：WSL 内安装**（如果你用 WSL 方案）
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

> Windows 上 Claude Code 需要 Git for Windows（自带 Git Bash）或 WSL。官方建议安装 Git for Windows。

### 7.2 配置 Git Bash 路径（Windows 原生方案）

如果 Claude Code 找不到 Git Bash，在 `~/.claude/settings.json` 中配置：

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

### 7.3 添加 MemPalace MCP Server

**在 WSL 中使用 Claude Code**：

```bash
# 在 WSL 终端中运行
claude mcp add mempalace -- ~/.mempalace-venv/bin/python3 -m mempalace.mcp_server
```

**在 Windows 原生 Claude Code 中**（WSL 路径示例）：

```bash
claude mcp add mempalace -- wsl -d Ubuntu ~/.mempalace-venv/bin/python3 -m mempalace.mcp_server
```

或者，如果 MCP server 在 Windows 路径下运行：

```bash
claude mcp add mempalace -- python -m mempalace.mcp_server
```

### 7.4 验证 MCP 连接

```bash
# 查看已连接的 MCP 工具
claude mcp list
# 应看到 mempalace 在列表中

# 运行健康检查
claude doctor
```

### 7.5 使用方式

启动 Claude Code 后，直接用自然语言提问：

```
"我们上次讨论的数据库选型结论是什么？"
"帮我查一下 Python AI 智能体项目的技术栈决策"
"Kai 之前对 API 设计有什么建议？"
```

Claude Code 会自动调用 `mempalace_search` 等工具，在记忆宫殿中检索答案并回答。

### 7.6 配置 Auto-Save Hooks（仅 WSL 方案可用）

编辑 `~/.claude/settings.local.json`（注意是 `settings.local.json`，不是 `settings.json`）：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/home/你的用户名/.mempalace-venv/bin/python3 -m mempalace.mcp_server",
            "timeout": 30
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/home/你的用户名/.mempalace/hooks/mempal_precompact_hook.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

> ⚠️ 原生 Windows Claude Code 无法使用 bash hook。如需自动保存功能，必须使用 WSL 方案。

---

## 8. 连接 Codex CLI

### 8.1 Codex CLI 安装（Windows）

```powershell
# PowerShell
irm https://raw.githubusercontent.com/openai/codex/main/install.ps1 | iex

# 或
npm install -g @openai/codex
```

> 参考：https://developers.openai.com/codex/cli

### 8.2 重要限制：Windows 上 Hooks 临时禁用

> 官方文档明确说明：
> *"Experimental. Hooks are under active development. Windows support temporarily disabled."*

**这意味着**：Codex CLI 在 Windows 上的自动保存 Hooks 功能**目前不可用**，无论使用哪种方案。但 **MCP 连接功能正常**。

### 8.3 配置 MemPalace MCP Server

编辑 `~/.codex/config.toml`：

```toml
[mcp_servers.mempalace]
command = "/home/你的用户名/.mempalace-venv/bin/python3"
args = ["-m", "mempalace.mcp_server"]
# WSL 中运行（如果 Windows 本地安装了 Codex CLI 但 MemPalace 在 WSL 中）
# 需要通过 WSL 路径调用
```

**如果 MemPalace 在 WSL 中，Codex CLI 在 Windows 原生中**，可以使用 WSL 路径：

```toml
[mcp_servers.mempalace]
command = "wsl"
args = ["-d", "Ubuntu", "--", "/home/用户名/.mempalace-venv/bin/python3", "-m", "mempalace.mcp_server"]
```

**通过 codex mcp 命令添加**（更简单）：

```bash
# WSL 中
codex mcp add mempalace -- /home/用户名/.mempalace-venv/bin/python3 -m mempalace.mcp_server

# Windows 原生 PowerShell（如果 MemPalace 在 Windows 上安装了）
codex mcp add mempalace -- python -m mempalace.mcp_server
```

### 8.4 验证连接

```bash
# 在 Codex TUI 中
/mcp

# 应该看到 mempalace 显示为 CONNECTED
```

### 8.5 Codex CLI 可用 Hooks（参考）

Codex CLI 支持的 Hook 事件（但 Windows 暂时禁用）：

| Hook 事件 | 触发时机 | Windows 支持 |
|-----------|---------|-------------|
| SessionStart | 会话开始/恢复 | ❌ 禁用 |
| PreToolUse | 工具执行前 | ❌ 禁用 |
| PostToolUse | 工具执行后 | ❌ 禁用 |
| UserPromptSubmit | 用户提交提示时 | ❌ 禁用 |
| Stop | 对话停止时 | ❌ 禁用 |

---

## 9. 自动保存 Hooks 配置

MemPalace 提供两个 Hook 用于自动保存（减少手动触发）：

### 9.1 Save Hook（mempal_save_hook.sh）

- **触发时机**：每 15 条人类消息后
- **功能**：保存新事实和决策，重建关键事实层（L1）
- **防止无限循环**：通过 `stop_hook_active` 标志

```bash
# 在 WSL 中给脚本加执行权限
chmod +x ~/.mempalace/hooks/mempal_save_hook.sh
chmod +x ~/.mempalace/hooks/mempal_precompact_hook.sh
```

### 9.2 PreCompact Hook（mempal_precompact_hook.sh）

- **触发时机**：Claude Code 上下文窗口压缩之前
- **功能**：在上下文被压缩前强制保存所有内容（安全网）
- **配置示例**（Claude Code）：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/hooks/mempal_save_hook.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/hooks/mempal_precompact_hook.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 9.3 Hook 配置参数

在 hook 脚本中可调整：

```bash
# 编辑 hook 脚本，找到并修改：
SAVE_INTERVAL=15  # 每 N 条人类消息保存一次（可调整）
```

---

## 10. 常用命令速查

### CLI 命令

```bash
# 安装与状态
pip install mempalace
mempalace --version
mempalace status                    # palace 概况
mempalace --help

# 初始化
mempalace init <目录>               # 引导式初始化
mempalace init <目录> --force       # 强制重新初始化

# 挖掘数据
mempalace mine <目录>               # 挖掘项目文件
mempalace mine <目录> --mode convos # 挖掘对话记录
mempalace mine <目录> --mode convos --extract general  # 自动分类
mempalace mine <目录> --wing 项目名  # 指定 wing

# 分割合并对话文件
mempalace split <文件>              # 分割
mempalace split <文件> --dry-run    # 预览
mempalace split <文件> --min-sessions 3  # 仅 3+ 会话

# 搜索
mempalace search "查询内容"          # 全局搜索
mempalace search "查询" --wing 项目  # wing 内搜索
mempalace search "查询" --room 房间  # 精确到房间

# 上下文加载
mempalace wake-up                   # 加载 L0+L1（~170 tokens）
mempalace wake-up --wing 项目        # 指定 wing 的上下文

# 压缩
mempalace compress --wing 项目      # AAAK 压缩

# MCP Server
python3 -m mempalace.mcp_server     # 启动 MCP server
```

### MCP 工具（19个）

**读取工具（Palace）**

| 工具 | 功能 |
|------|------|
| `mempalace_status` | palace 概况 + AAAK 协议 + 记忆协议 |
| `mempalace_list_wings` | 列出所有 wing 及其抽屉数量 |
| `mempalace_list_rooms` | 列出 wing 内的所有房间 |
| `mempalace_get_taxonomy` | 完整 wing → room → count 树 |
| `mempalace_search` | 语义搜索（支持 wing/room 过滤）|
| `mempalace_check_duplicate` | 写入前检查是否重复 |
| `mempalace_get_aaak_spec` | AAAK 方言参考 |

**写入工具（Palace）**

| 工具 | 功能 |
|------|------|
| `mempalace_add_drawer` | 写入原始内容到 palace |
| `mempalace_delete_drawer` | 按 ID 删除抽屉 |

**知识图谱工具**

| 工具 | 功能 |
|------|------|
| `mempalace_kg_query` | 查询实体关系（支持时间过滤）|
| `mempalace_kg_add` | 添加三元组事实 |
| `mempalace_kg_invalidate` | 标记事实失效 |
| `mempalace_kg_timeline` | 实体的时序故事 |
| `mempalace_kg_stats` | 图谱概况 |

**导航工具**

| 工具 | 功能 |
|------|------|
| `mempalace_traverse` | 从某个房间遍历跨 wing 关系 |
| `mempalace_find_tunnels` | 查找连接两个 wing 的走廊 |
| `mempalace_graph_stats` | 图谱连通性概况 |

**Agent 日记工具**

| 工具 | 功能 |
|------|------|
| `mempalace_diary_write` | 写入 AAAK 日记条目 |
| `mempalace_diary_read` | 读取最近 N 条日记 |

---

## 11. 架构速览：Palace 结构解析

### 11.1 层级结构

```
WING（人 / 项目）
 ├── HALL（记忆类型，跨 wing 相同）
 │    ├── hall_facts      —— 决策、已锁定的选择
 │    ├── hall_events     —— 会话、里程碑、调试
 │    ├── hall_discoveries —— 突破、新洞察
 │    ├── hall_preferences —— 习惯、偏好、观点
 │    └── hall_advice     —— 建议和方案
 │
 └── ROOM（具体主题）
      ├── CLOSET（摘要，指向原始内容）
      │    └── DRAWER（原始 verbatim 文件）
      └── CLOSET
           └── DRAWER
```

### 11.2 走廊（Tunnel）—— 跨 Wing 连接

当不同 wing 中出现相同 room 时，走廊自动建立：

```
wing_亮老板 / hall_events / api-design  → "讨论了 REST vs GraphQL"
wing_python-agent / hall_facts / api-design → "决定用 REST"
wing_product-recommendations / hall_advice / api-design → "推荐统一 REST"

→ 同一个 room（api-design），三个 wing，走廊把它们连起来
```

### 11.3 记忆层级（Memory Stack）

| 层级 | 内容 | 大小 | 加载时机 |
|------|------|------|---------|
| L0 | 身份（AI 是谁）| ~50 tokens | 每会话 |
| L1 | 关键事实（团队、项目、偏好）| ~120 tokens | 每会话 |
| L2 | 房间回忆（近期会话、当前项目）| 按需 | 话题触发 |
| L3 | 深度搜索（所有 closet 语义查询）| 按需 | 主动查询 |

### 11.4 AAAK 方言（实验性）

AAAK 是一种有损缩写方言，将重复实体压缩为代码：

```
原始文本（~66 tokens）：
"Priya manages the Driftwood team: Kai (backend, 3 years), 
Soren (frontend), Maya (infrastructure)..."

AAAK 格式（~73 tokens at small scale）：
"TEAM: PRI(lead) | KAI(backend,3yr) SOR(frontend) MAY(infra)
PROJ: DRIFTWOOD(saas.analytics)"
```

> ⚠️ AAAK 在小规模场景下不节省 tokens（overhead 反而更多）。它的价值在于**大规模重复实体**场景（如团队成员在数百条会话中反复出现）。v3.0.0 实测 raw 模式（96.6%）优于 AAAK 模式（84.2%）。

---

## 12. Windows 常见问题

### Q1：`python` / `python3` 命令找不到

**原因**：Python 未安装或 PATH 未配置。

**解决**：
```powershell
# 检查 Python 是否通过 py launcher 安装
py --version

# 如果用的是 Microsoft Store 版本
python --version

# 重新安装，确保勾选 "Add Python to PATH"
```

### Q2：pip install 报 Access Denied

**解决**：
```powershell
# 方案 A：用户级安装
python -m pip install mempalace --user

# 方案 B：管理员 PowerShell
Start-Process powershell -Verb RunAs
# 在新窗口中运行 pip install
```

### Q3：ChromaDB hnswlib 编译失败

**错误示例**：
```
Building wheel for hnswlib ... error
CMake Error: The C++ compiler ... not found
```

**解决**：
```powershell
# 方案 A：强制使用预编译 wheel
pip install --only-binary=:all: chromadb
pip install mempalace

# 方案 B：安装 Visual Studio Build Tools
# 下载：https://visualstudio.microsoft.com/downloads/
# 选择 "C++ Build Tools"

# 方案 C（最推荐）：使用 WSL
wsl --install
# 然后在 WSL 中安装 MemPalace（见方案一）
```

### Q4：Claude Code 找不到 Git Bash

**解决**：在 `~/.claude/settings.json` 中配置路径：

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

### Q5：mempalace 命令找不到（已安装后）

```powershell
# 新开一个 PowerShell / CMD 窗口（pip 安装后需重启 shell）

# 或者用完整路径
python -m mempalace --version

# 检查 pip 安装位置
python -m pip show mempalace
```

### Q6：WSL 中 `curl` 或 `bash` 脚本无法执行

```bash
# 给脚本加执行权限
chmod +x install.sh
chmod +x ~/.mempalace/hooks/*.sh

# WSL 中安装 curl（如果没有）
sudo apt install curl
```

### Q7：Codex CLI MCP 连接失败

**检查**：
```bash
# 确认 MemPalace MCP server 正在运行
python3 -m mempalace.mcp_server

# 确认 config.toml 路径正确
cat ~/.codex/config.toml
```

**常见错误**：
- `command not found`：Python 路径不正确，替换为完整绝对路径
- `timeout`：MCP server 启动超时，增加 `startup_timeout_sec`

### Q8：Claude Code / Codex 连接 MCP 后找不到 mempalace 工具

```bash
# 确认 MCP server 正常运行
python3 -m mempalace.mcp_server

# 验证工具列表（单独测试 MCP）
# 另开一个终端：
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 -m mempalace.mcp_server
```

### Q9：Hook 脚本在 Windows 原生环境无法运行

**现状**：MemPalace Hooks 是 bash 脚本，原生 Windows（无 WSL）无法直接运行。

**替代方案**：
1. **切换到 WSL**（推荐，彻底解决）
2. **手动触发保存**：在 Claude Code 会话结束前，主动说"帮我把今天的讨论保存到 MemPalace"
3. **关注社区**（https://github.com/milla-jovovich/mempalace/discussions）：等待 PowerShell 版 Hook 脚本出现

### Q10：ChromaDB 数据库损坏或查询变慢

```bash
# 查看 palace 状态
mempalace status

# 重建索引（删除旧数据库，重新挖掘）
rm -rf ~/.mempalace/palace/
mempalace mine ~/你的项目路径 --mode convos
```

---

## 附录：参考链接

| 资源 | 地址 |
|------|------|
| MemPalace GitHub | https://github.com/milla-jovovich/mempalace |
| MemPalace PyPI | https://pypi.org/project/mempalace/ |
| MemPalace v3.0.0 发布说明 | https://github.com/milla-jovovich/mempalace/releases/tag/v3.0.0 |
| Claude Code 安装文档 | https://code.claude.com/docs/en/setup |
| Claude Code Windows 指南 | https://claude.ai/public/artifacts/03a4aa0c-67b2-427f-838e-63770900bf1d |
| Codex CLI 文档 | https://developers.openai.com/codex/cli |
| Codex CLI MCP 文档 | https://developers.openai.com/codex/mcp |
| Codex CLI Hooks 文档 | https://developers.openai.com/codex/hooks |
| WSL 官方文档 | https://docs.microsoft.com/windows/wsl/ |
| ChromaDB Windows 问题追踪 | https://github.com/chroma-core/chroma/issues/250 |

---

*本教程基于 MemPalace v3.0.0、Claude Code 最新版、Codex CLI 官方文档编写。*
*Windows 特定限制来自官方文档和社区反馈，如有更新请以官方为准。*
