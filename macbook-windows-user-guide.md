# 🎯 Windows 用户 MacBook Pro M1 上手指南

> 适用机型：MacBook Pro 2021 款（M1 Pro/Max 芯片）
> 目标读者：从 Windows 转向 macOS 的开发者

---

## 📋 目录

1. [macOS 初始化设置](#1-macos-初始化设置首次开机必做)
2. [Windows 用户必知的 macOS 基础概念](#2-windows-用户必知的-macos-基础概念)
3. [推荐安装的必备软件](#3-推荐安装的必备软件)
4. [Windows 习惯在 macOS 的对应操作](#4-windows-习惯在-macos-的对应操作)
5. [开发环境配置](#5-开发环境配置针对-cpython-后端开发)
6. [macOS 日常维护](#6-macos-日常维护)

---

## 1. macOS 初始化设置（首次开机必做）

### 1.1 Apple ID 创建和 iCloud 设置

**如果没有 Apple ID：**

1. 开机后选择 **「创建 Apple ID」**
2. 按提示填写：邮箱、密码、姓名、生日
3. **建议使用 Gmail 或Outlook 邮箱**，国内邮箱有时收不到验证码
4. 开启 **双重认证**（必开！）

**iCloud 设置建议：**

| 功能 | 推荐状态 | 理由 |
|------|---------|------|
| iCloud Drive | ✅ 开启 | 跨设备同步文件 |
| 照片 | ✅ 开启 | 自动备份照片 |
| 备忘录 | ✅ 开启 | 跨设备同步 |
| 钥匙串 | ✅ 开启 | 密码管理 |
| 查找 Mac | ✅ 开启 | 防丢必备 |

> 💡 **技巧**：iCloud Drive 可以让你在 Finder 中直接访问云端文件，就像 OneDrive 一样。

### 1.2 系统偏好设置推荐配置

按 `Command + ,` 打开系统偏好设置（或者点苹果图标 → 系统偏好设置）

**必改设置：**

```
🔧 通用
├── 外观：选择「深色」模式（程序员首选）
├── 菜单栏显示：勾选「电池百分比」
└── 侧面点击：选择「打开启动台」

🔧 触控板
├── 全部勾选：轻点来点按、轨迹手势...
├── 关闭「查找」的三指轻点（与 JetBrains 冲突）
└── 推荐开启「辅助点按」= 右键菜单

🔧 显示器
├── 关闭「夜览」（保护视力）
└── 分辨率：「缩放」- 选更大的字体

🔧 电池
├── 启用「使用电池时自动调节亮度」
└── 关闭「使用电池时启用电源通知」
```

### 1.3 通知/聚焦/Siri 初始配置

**通知中心：**

- 关闭大部分 app 的通知，只保留 **微信、钉钉、邮件**
- 专注模式（Focus）：工作时段开启「勿扰模式」

**Siri：**

- 首次开机可能需要区域选择，选 **中国大陆**
- 建议关闭「语音反馈」（用键盘更快）

---

## 2. Windows 用户必知的 macOS 基础概念

| macOS 名称 | Windows 对应 | 说明 |
|------------|-------------|------|
| **Finder** | 文件资源管理器 | 打开 Finder（`Command + E` 或点 Dock 左上角的笑脸）|
| **系统偏好设置** | 控制面板 | 相当于 Windows 的「设置」+「控制面板」|
| **启动台 (Launchpad)** | 开始菜单 | `F4` 键或点击 Dock 里的火箭图标 |
| **程序坞 (Dock)** | 任务栏 | 底部那条放常用 app 的横条 |
| **活动监视器** | 任务管理器 | `Command + 空格` 搜索「活动监视器」|
| **终端 (Terminal)** | CMD/PowerShell | `Command + 空格` 搜索「终端」|
| **废纸篓** | 回收站 | Dock 最右边，删东西都在这里 |
| **Safari** | Edge | macOS 自带浏览器 |
| **Preview** | Photos | 看图、PDF、截图自带软件 |

> 💡 **记住**：macOS 里没有 C 盘 D 盘，只有 **Macintosh HD**。文件通常放在 **/Users/你的用户名/** 下面。

---

## 3. 推荐安装的必备软件

### 3.1 安装方法

**方式一：App Store**（最简单）
- 点 Dock 里的 App Store 图标
- 搜索 → 点击 → 安装

**方式二：官网下载**（推荐）
- 百度搜索软件名 + macOS 版
- 下载 .dmg 文件 → 打开 → 拖到「应用程序」文件夹

**方式三：Homebrew**（最 geek，见下文）

---

### 3.2 必备软件清单

#### 🧰 工具类

| 软件 | 用途 | 安装方式 |
|------|------|---------|
| **Homebrew** | 包管理器，macOS 必备 | 终端运行安装脚本（见下文）|
| **Chrome / Firefox** | 浏览器 | 官网下载 |
| **The Unarchiver / Keka** | 解压 rar/7z | App Store 或官网 |
| **VLC** | 播放任何格式视频 | 官网下载 |
| **IINA** | 进阶视频播放器（更好用）| Homebrew: `brew install iina` |

#### 💼 办公类

| 软件 | 用途 |
|------|------|
| **Microsoft 365** | Word/Excel/PPT（订阅制）|
| **WPS** | 免费办公套件（国产）|
| **Notion** | 笔记/知识库（强烈推荐）|
| **Obsidian** | 本地笔记（你的主力工具）|

#### 🖥️ 开发类

| 软件 | 用途 |
|------|------|
| **VS Code** | 轻量级编辑器 |
| **Rider** | C# 开发（你的主力）|
| **PyCharm** | Python 开发 |
| **Docker Desktop** | 容器化（见下文）|
| **iTerm2** | 终端替代品（比自带 Terminal 强）|
| **Oh My Zsh** | 终端主题（见下文）|

#### 📸 效率类

| 软件 | 用途 | 快捷键 |
|------|------|--------|
| **Xnip** | 截图/贴图 | `Command + Shift + 4` |
| **CleanShot X** | 截图进阶版 | 同上，功能更全 |
| **Raycast** | 快速启动器（替代 Spotlight）| `Option + 空格` |
| **Karabiner-Elements** | 改键位（把 CapsLock 改成 Ctrl）| - |

#### ⌨️ 输入法

| 软件 | 状态 |
|------|------|
| **系统自带拼音** | ✅ 默认 |
| **搜狗输入法** | 可选（有时弹广告）|
| **百度输入法** | 可选 |
| **RIME** | 进阶用户首选 |

> 💡 **推荐**：先用系统自带输入法，够用且无广告。后期再考虑 RIME。

---

## 4. Windows 习惯在 macOS 的对应操作

### 4.1 键盘差异

| Windows | macOS | 说明 |
|---------|-------|------|
| `Ctrl + C` | `Command + C` | 复制 |
| `Ctrl + V` | `Command + V` | 粘贴 |
| `Ctrl + X` | `Command + X` | 剪切（但有限制，见下）|
| `Ctrl + Z` | `Command + Z` | 撤销 |
| `Ctrl + S` | `Command + S` | 保存 |
| `Ctrl + A` | `Command + A` | 全选 |
| `Ctrl + F` | `Command + F` | 查找 |
| `Ctrl + Tab` | `Command + Tab` | 切换应用 |
| `Win` | `Command` (⌘) | 修饰键 |
| `Alt` | `Option` (⌥) | 修饰键 |

> 🎯 **核心区别**：macOS 用 `Command` 键替代了 `Ctrl` 键的位置！

---

### 4.2 剪切功能（重要⚠️）

**Windows**：可以剪切文件/文本，移动到新位置
**macOS**：只能剪切**文本**，不能剪切文件！

**替代方案：**

1. **拖拽文件**：直接拖到目标文件夹（保持原文件）
2. **快捷键**：`Command + C` 复制 → `Command + Option + V` 移动（不是复制！）
3. **右键菜单**：按住 `Option` 会变成「移动到...」

---

### 4.3 卸载软件

**Windows**：控制面板 → 程序和功能 → 卸载
**macOS**：

1. 打开 **启动台** (Launchpad)
2. 找到要卸载的 app
3. **长按** app 图标直到抖动起来
4. **拖到废纸篓**（或点左上角 × 号）
5. 清空废纸篓

> 💡 也可以用 **App Cleaner**（Homebrew: `brew install appcleaner`）彻底清理残留文件。

---

### 4.4 刷新页面

| 操作 | Windows | macOS |
|------|---------|-------|
| 刷新网页 | `F5` | `Command + R` |
| 强制刷新 | `Ctrl + F5` | `Command + Shift + R` |

---

### 4.5 截图快捷键

| 功能 | 快捷键 | 保存位置 |
|------|--------|---------|
| 全屏截图 | `Command + Shift + 3` | 桌面 |
| 区域截图 | `Command + Shift + 4` | 桌面 |
| 区域截图（不保存）| `Command + Shift + 4` 然后空格 | 剪贴板 |
| 窗口截图 | `Command + Shift + 4` 然后空格 | 桌面 |

**进阶截图（推荐配合 Xnip）：**

- 截图后可以**直接贴图**在屏幕上
- 可以标注、箭头、模糊敏感信息

---

### 4.6 窗口分屏

**Windows**：窗口拖到屏幕边缘 → Snap 分屏
**macOS**：

1. **拖拽法**：窗口拖到屏幕最顶部 → 出现分屏选项 → 选择左/右半屏
2. **快捷键**：`Control + Command + F` 进入全屏 → 拖拽调整
3. **第三方工具**：Rectangle（免费，比 Windows Snap 还好用）

> 💡 推荐安装 **Rectangle**：`brew install rectangle`

---

### 4.7 其他常用快捷键

| 操作 | 快捷键 |
|------|--------|
| 强制退出 | `Command + Option + Esc` |
| 切换窗口 | `Command + ``（反引号）` |
| 最小化窗口 | `Command + M` |
| 隐藏当前应用 | `Command + H` |
| 隐藏其他应用 | `Command + Option + H` |
| 打开 Finder | `Command + N` 新窗口 |
| 调出 Spotlight | `Command + 空格` |
| 显示桌面 | `Command + F3`（或四指滑动手势）|

---

## 5. 开发环境配置（针对 C#/Python 后端开发）

### 5.1 Homebrew 安装（第一步）

打开 **终端 (Terminal)**，粘贴下面的命令：

```bash
# 安装 Homebrew（回车后可能需要按回车确认）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**验证安装成功：**

```bash
brew --version
```

> ⚠️ 如果提示 `command not found`，需要把 Homebrew 加入 PATH。终端会给出提示，按提示执行。

---

### 5.2 安装 .NET SDK

```bash
# 安装 .NET SDK（长期支持版）
brew install --cask dotnet-sdk

# 验证
dotnet --version
```

> 💡 .NET 会在 `~/Library//dotnet` 安装，项目会自动使用。

---

### 5.3 安装 Python

```bash
# 安装 Python 3（Homebrew 版本）
brew install python@3.11

# 验证
python3 --version
pip3 --version
```

> ⚠️ macOS 自带 Python 2.7（已废弃），但不要动它。安装的新版会叫 `python3`。

**配置 pip 镜像（国内加速）：**

```bash
mkdir -p ~/.pip
cat > ~/.pip/pip.conf <<EOF
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
EOF
```

---

### 5.4 安装 Docker Desktop

```bash
# 通过 Homebrew 安装
brew install --cask docker

# 或者官网下载：https://www.docker.com/products/docker-desktop
```

**M1/M2 特别注意：**

- 一定要下载 **Apple Silicon** 版本！
- Intel 版在 M1 上也能跑，但性能差很多
- 安装后打开 Docker Desktop，等待绿色灯亮起

---

### 5.5 安装 Rider / PyCharm

**方式一：JetBrains Toolbox（推荐）**

```bash
# 安装 Toolbox
brew install --cask jetbrains-toolbox
```

打开 Toolbox，勾选你要的 IDE：
- **Rider** - C# 开发
- **PyCharm Professional** - Python 开发（学生/个人免费）

**方式二：官网直接下载**

- Rider: https://www.jetbrains.com/rider/
- PyCharm: https://www.jetbrains.com/pycharm/

---

### 5.6 Git 配置

```bash
# 安装 Git（通常已自带）
brew install git

# 配置用户名和邮箱
git config --global user.name "你的名字"
git config --global user.email "your@email.com"

# 初始化 SSH key
ssh-keygen -t ed25519 -C "your@email.com"
```

**GitHub SSH 绑定：**

```bash
# 查看生成的公钥
cat ~/.ssh/id_ed25519.pub
```

1. 打开 https://github.com/settings/keys
2. 点击 **New SSH key**
3. 把上面的内容粘贴进去
4. 标题随意写，如「MacBook Pro」

**验证连接：**

```bash
ssh -T git@github.com
```

看到 `Hi xxx! You've successfully authenticated` 就成功了！

---

### 5.7 iTerm2 + Oh My Zsh（终端美化）

```bash
# 安装 iTerm2
brew install --cask iterm2

# 安装 Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**推荐插件：**

```bash
# zsh-autosuggestions（命令补全建议）
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting（命令语法高亮）
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

编辑 `~/.zshrc` 启用插件：

```bash
plugins=(git docker python zsh-autosuggestions zsh-syntax-highlighting)
```

---

## 6. macOS 日常维护

### 6.1 磁盘清理

**Windows**：用「磁盘清理」或 CCleaner
**macOS**：

1. **系统自带**：
   - 苹果图标 → 关于本机 → 存储空间 → 点「管理」
   - 这里可以看到「邮件」「废纸篓」「系统」占用

2. **清理缓存**：
   ```bash
   # 清理系统缓存（谨慎使用）
   sudo rm -rf ~/Library/Caches/*
   ```

3. **Homebrew 清理**：
   ```bash
   brew cleanup  # 清理旧版本
   brew autoremove  # 清理不需要的依赖
   ```

> 💡 macOS 会自动管理磁盘，一般不需要手动清理。除非空间实在不够。

---

### 6.2 内存管理

**重要概念**：

- **不需要像 Windows 那样经常重启！**
- macOS 的内存管理比 Windows 好很多，空闲内存会被用来缓存
- **不需要清内存 app**（那些都是智商税）

**强制退出卡死程序**：

1. `Command + Option + Esc` 打开强制退出面板
2. 选择卡死的程序 → 点「强制退出」
3. 或者：`Command + 空格` 搜索「活动监视器」→ 选中进程 → 点左上角 ×

---

### 6.3 系统更新

**检查更新**：

```bash
# 终端检查
softwareupdate -l
```

或者：苹果图标 → 系统偏好设置 → 软件更新

> ⚠️ **建议**：新 MacBook 收到系统更新后，等一周再升级（等第一批 bug 修复）。

---

## 🎉 快速检查清单

初次设置后，勾选完成：

- [ ] Apple ID 登录 + iCloud 开启
- [ ] 系统偏好设置调整完毕
- [ ] Homebrew 安装成功
- [ ] Chrome/Edge 安装
- [ ] VS Code / Rider / PyCharm 安装
- [ ] Docker Desktop 安装并运行
- [ ] Git 配置 + SSH key 添加到 GitHub
- [ ] iTerm2 + Oh My Zsh 装好
- [ ] 截图软件（Xnip）安装

---

## 📚 进阶资源

- **macOS 使用手册**：https://support.apple.com/zh-cn/guide/mac-help/welcome/mac
- **Homebrew 文档**：https://brew.sh
- **Oh My Zsh 主题**：https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
- **Rectangle 窗口管理**：https://github.com/rxhanson/Rectangle

---

> 🐈‍⬛ 祝你在 macOS 上开发愉快！有疑问随时问我。