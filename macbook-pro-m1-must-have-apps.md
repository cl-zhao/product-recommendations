# MacBook Pro M1 (2021款) 装机必备应用清单

> 面向从 Windows 转向 macOS 的 C#/Python 后端开发者

**参考来源**：本清单参考了 Reddit (r/MacOS、r/macapps)、Medium 技术博客、TechRadar、Setapp、AlternativeTo、XDA Developers、Lifehacker 等 15+ 篇权威资料。

---

## 目录

1. [系统工具类](#1-系统工具类)
2. [开发工具类](#2-开发工具类)
3. [效率工具类](#3-效率工具类)
4. [办公协作类](#4-办公协作类)
5. [娱乐媒体类](#5-娱乐媒体类)
6. [Mac 独占优质应用](#6-mac-独占优质应用)
7. [必装 TOP 10](#7-必装-top-10)
8. [Homebrew 一键安装脚本](#8-homebrew-一键安装脚本)
9. [安装顺序建议](#9-安装顺序建议)

---

## 1. 系统工具类

### 1.1 窗口管理

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Rectangle** | 免费 (开源) | DisplayFusion / WinSplit | ⭐⭐⭐ |
| **Amethyst** | 免费 (开源) | 自动铺排窗口工具 | ⭐⭐ |
| **Magnet** | ¥30 | Windows 窗口拖拽对齐 | ⭐⭐ |
| **Witch** | $10 | Alt+Tab 窗口切换器 | ⭐⭐ |

> **为什么必装**：Mac 默认的窗口管理远不如 Windows 灵活。Rectangle 完全免费且开源，是从 Windows 转换后**第一个应该安装**的应用，可通过快捷键快速调整窗口大小和位置[^1]。

### 1.2 截图工具

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Xnip** | 免费 / ¥68 高级版 | Snipaste | ⭐⭐⭐ |
| **CleanShot X** | $14 | Snipaste / ShareX | ⭐⭐ |
| **Lightshot** | 免费 | Snipaste | ⭐⭐ |

> **为什么必装**：Mac 自带截图功能（Cmd+Shift+3/4/5）较为基础。Xnip 提供滚动截图、贴图、标注等高级功能，对开发者截取代码非常实用[^2]。

### 1.3 剪贴板管理

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Clipy** | 免费 (开源) | ClipboardFusion | ⭐⭐⭐ |
| **Paste** | $17 | Ditto | ⭐⭐ |

> **为什么必装**：Mac 剪贴板只能保留一项内容。Clipy 完全免费且开源，可保存剪贴板历史，支持代码片段收藏。

### 1.4 菜单栏管理

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Bartender** | $15 | 无直接对应 | ⭐⭐ |

> **为什么必装**：Mac 菜单栏图标众多，Bartender 可隐藏不常用的菜单栏图标，保持界面整洁[^3]。

### 1.5 系统监控

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **iStat Menus** | ¥128 | Task Manager / HWiNFO | ⭐⭐⭐ |
| **TG Pro** | $10 | Core Temp | ⭐⭐ |
| **MenuMeters** | 免费 | Task Manager | ⭐ |

> **为什么必装**：iStat Menus 是 macOS 最知名的系统监控工具，可在菜单栏实时显示 CPU、内存、温度、风扇速度等。M1 芯片的功耗和温度监控对开发者尤为重要[^4]。

### 1.6 软件卸载

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **App Cleaner & Uninstaller** | 免费 / ¥78 专业版 | Revo Uninstaller | ⭐⭐⭐ |
| **CleanMyMac X** | ¥199/年 | CCleaner | ⭐⭐ |

> **为什么必装**：Mac 虽然可以将应用拖到废纸篓卸载，但残留文件较多。App Cleaner 可彻底卸载应用并清理残留文件[^5]。

### 1.7 磁盘清理

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Disk Inventory X** | 免费 | TreeSize | ⭐⭐ |
| **OmniDiskSweeper** | 免费 | WinDirStat | ⭐⭐ |

> **为什么必装**：帮助快速识别占用磁盘空间的大文件，清理无用的安装包和缓存。

### 1.8 DNS 优化

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **1.1.1.1** | 免费 | 无直接对应 | ⭐⭐⭐ |
| **Control D** | 免费 / $4.99/月 | 无直接对应 | ⭐⭐ |

> **为什么必装**：1.1.1.1 是 Cloudflare 提供的 DNS 服务，可加速网络访问、保护隐私。M1 Mac 开发者网络访问频繁，DNS 优化很有必要[^6]。

---

## 2. 开发工具类

### 2.1 开发环境

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **VS Code** | 免费 | VS Code (相同) | ⭐⭐⭐ |
| **Rider** | ¥1,890/年 (个人免费) | Visual Studio | ⭐⭐⭐ |
| **PyCharm** | 免费社区版 / ¥3,490专业版 | PyCharm (相同) | ⭐⭐⭐ |

> **为什么必装**：C# 开发用 Rider，Python 开发用 PyCharm，VS Code 作为通用编辑器。对于 M1 Mac，需要安装支持 Apple Silicon 的版本（Rider 和 PyCharm 都有原生 M1 版本）[^7]。

### 2.2 Docker

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Docker Desktop for Mac** | 免费 (个人) | Docker Desktop | ⭐⭐⭐ |

> **为什么必装**：后端开发必备。M1/M2/M3 Mac 需要安装支持 Apple Silicon 的版本（docker pull 时注意选择 arm64 架构）[^8]。

### 2.3 API 测试

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Postman** | 免费 / $15/月 | Postman (相同) | ⭐⭐⭐ |
| **Insomnia** | 免费 / $5/月 | Postman | ⭐⭐ |
| **HTTP Client** (VS Code 插件) | 免费 | 无直接对应 | ⭐⭐ |

> **为什么必装**：Postman 是 API 测试的行业标准，功能全面，支持团队协作。Insomnia 更加轻量级，有漂亮的 UI 设计[^9]。

### 2.4 数据库管理

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **TablePlus** | 免费 / $89 终身版 | Navicat / DBeaver | ⭐⭐⭐ |
| **DBngin** | 免费 | 无直接对应 | ⭐⭐⭐ |

> **为什么必装**：TablePlus 是 macOS 上最漂亮的数据库客户端，支持 MySQL、PostgreSQL、Redis 等。DBngin 是 TablePlus 团队开发的数据库版本管理工具，可一键启动本地数据库服务，无需 Docker[^10]。

### 2.5 终端工具

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **iTerm2** | 免费 (开源) | Windows Terminal | ⭐⭐⭐ |
| **Warp** | 免费 | Windows Terminal | ⭐⭐⭐ |
| **Oh My Zsh** | 免费 | 无直接对应 | ⭐⭐⭐ |

> **为什么必装**：Mac 自带 Terminal 远不如 iTerm2 功能丰富。Warp 是 AI 时代的终端，内置 AI 命令补全。iTerm2 + Oh My Zsh 是经典组合，主题和插件生态丰富[^11]。

### 2.6 Git 图形化

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **GitHub Desktop** | 免费 | GitHub Desktop | ⭐⭐⭐ |
| **Sourcetree** | 免费 | Sourcetree | ⭐⭐ |
| **Fork** | 免费 / $59 终身 | GitKraken | ⭐⭐ |

> **为什么必装**：Git 命令行虽然强大，但图形化工具更直观。GitHub Desktop 简洁易用，是 GitHub 官方推荐。

### 2.7 SSH 工具

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Termius** | 免费 / $9.99/月 | PuTTY / Xshell | ⭐⭐⭐ |

> **为什么必装**：跨平台的 SSH 客户端，支持 SSH 密钥管理、多设备同步。Mac 上没有 Xshell，Termius 是很好的替代品[^12]。

### 2.8 包管理器

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Homebrew** | 免费 | Chocolatey / Scoop | ⭐⭐⭐ |

> **为什么必装**：macOS 必备的包管理器，安装命令行工具（如 git、node、python、docker 等）的首选方式。**新 Mac 第一件事就是安装 Homebrew**[^13]。

### 2.9 DevOps 工具

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **kubectl** | 免费 | kubectl (相同) | ⭐⭐⭐ |
| **Terraform** | 免费 | Terraform (相同) | ⭐⭐⭐ |
| **Helm** | 免费 | 无直接对应 | ⭐⭐ |

> **为什么必装**：如果涉及 Kubernetes 和云基础设施，这些命令行工具是必备的，都可通过 Homebrew 安装。

---

## 3. 效率工具类

### 3.1 快速启动器

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Raycast** | 免费 / $9/月 专业版 | Wox / Listary | ⭐⭐⭐ |
| **Alfred** | 免费 / £39 终身 | Wox / Listary | ⭐⭐ |

> **为什么必装**：Raycast 是 macOS 2020 年代最火的效率工具，可快速搜索文件、运行命令、控制系统。免费版功能足够，对开发者非常友好[^14]。Alfred 是老牌启动器，功能强大但收费。

### 3.2 笔记 /知识管理

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Obsidian** | 免费 / $10/月 | Notion / Logseq | ⭐⭐⭐ |
| **Notion** | 免费 / $10/月个人版 | Notion (相同) | ⭐⭐⭐ |

> **为什么必装**：Obsidian 是本地优先的 Markdown 知识管理工具，数据完全本地存储，插件生态丰富。Notion 是在线协作工具，功能全面。

### 3.3 时间管理

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Fantastical** | ¥128/年 | Outlook 日历 | ⭐⭐ |
| **Raycast Calendar** | 免费 | 无直接对应 | ⭐⭐ |

### 3.4 PDF 工具

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **PDF Expert** | ¥318 终身 | Adobe Acrobat | ⭐⭐ |
| **Preview** (自带) | 免费 | Adobe Reader | ⭐⭐⭐ |

> **为什么必装**：Mac 自带的 Preview 功能已经很强大了，足以应对日常 PDF 阅读和简单编辑。

### 3.5 压缩工具

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Keka** | 免费 / ¥38 | 7-Zip / Bandizip | ⭐⭐⭐ |
| **The Unarchiver** | 免费 | 7-Zip | ⭐⭐ |

> **为什么必装**：Mac 自带解压缩支持较弱。Keka 支持 7z、rar、zip 等多种格式，The Unarchiver 是免费替代品[^15]。

### 3.6 云存储

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **阿里云盘** | 免费 / 会员 | 百度网盘 | ⭐⭐⭐ |
| **百度网盘** | 免费 / 会员 | 百度网盘 | ⭐⭐ |

### 3.7 密码管理

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **1Password** | $2.99/月 | LastPass / Bitwarden | ⭐⭐⭐ |
| **Bitwarden** | 免费 / $10/年 | LastPass | ⭐⭐ |

> **为什么必装**：开发者账号多，密码管理非常重要。1Password 是 macOS 原生体验最好的密码管理器，Bitwarden 是免费开源替代品。

---

## 4. 办公协作类

### 4.1 办公套件

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Microsoft 365** | ¥398/年个人版 | Microsoft 365 | ⭐⭐⭐ |
| **WPS** | 免费 / 会员 | WPS | ⭐⭐ |

### 4.2 即时通讯

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **微信 for Mac** | 免费 | 微信 (PC版) | ⭐⭐⭐ |
| **钉钉** | 免费 | 钉钉 | ⭐⭐⭐ |

### 4.3 视频会议

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **腾讯会议** | 免费 / 会员 | 腾讯会议 | ⭐⭐⭐ |
| **Zoom** | 免费 / $15.99/月 | Zoom | ⭐⭐⭐ |

### 4.4 邮件客户端

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Outlook** | 免费 / ¥428/年 | Outlook | ⭐⭐⭐ |
| **Spark** | 免费 / $9.99/月 | 无直接对应 | ⭐⭐ |

> **为什么必装**：Outlook 是微软官方邮件客户端，与 Microsoft 365 深度集成。Spark 以其智能分类和简洁设计著称。

---

## 5. 娱乐媒体类

### 5.1 视频播放器

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **IINA** | 免费 (开源) | VLC | ⭐⭐⭐ |
| **VLC** | 免费 | VLC | ⭐⭐ |

> **为什么必装**：IINA 是专为 macOS 设计的现代视频播放器，基于 MPV，支持几乎所有视频格式，UI 精美[^16]。

### 5.2 音乐

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Spotify** | 免费 / $10.99/月 | Spotify | ⭐⭐⭐ |
| **网易云音乐** | 免费 / 会员 | 网易云音乐 | ⭐⭐⭐ |

### 5.3 浏览器

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Chrome** | 免费 | Chrome | ⭐⭐⭐ |
| **Firefox** | 免费 | Firefox | ⭐⭐ |
| **Edge** | 免费 | Edge | ⭐⭐ |

> **为什么必装**：Chrome 是开发者必备，强大的开发者工具和插件生态。Edge 最近几年表现不错，可作为备选。

---

## 6. Mac 独占优质应用

### 6.1 系统维护

| 应用 | 价格 | 优先级 |
|------|------|--------|
| **CleanMyMac X** | ¥199/年 | ⭐⭐ |

> **为什么必装**：Mac 最知名的系统维护工具，可清理缓存、卸载应用、管理启动项等。但其实 macOS 本身不太需要这类工具，除非遇到问题[^17]。

### 6.2 虚拟机

| 应用 | 价格 | Windows 对应物 | 优先级 |
|------|------|---------------|--------|
| **Parallels Desktop** | ¥498/年 | VMware Workstation | ⭐⭐ |
| **UTM** | 免费 (开源) | VirtualBox | ⭐⭐ |

> **为什么必装**：M1/M2/M3 Mac 无法运行 Boot Camp。Parallels Desktop 是最成熟的虚拟机方案，可运行 Windows ARM 版。UTM 是免费开源替代品[^18]。

### 6.3 苹果生态联动

| 应用 | 价格 | 优先级 |
|------|------|--------|
| **Handoff** | 免费 (系统自带) | ⭐⭐⭐ |
| **Universal Control** | 免费 (系统自带) | ⭐⭐⭐ |
| **AirDrop** | 免费 (系统自带) | ⭐⭐⭐ |
| **Shortcuts** (快捷指令) | 免费 (系统自带) | ⭐⭐⭐ |

> **为什么必装**：这些是 Mac 独有的苹果生态优势。如果你有 iPhone/iPad，这些功能可以大幅提升工作效率。Shortcuts 可实现强大的自动化[^19]。

---

## 7. 必装 TOP 10

| 排名 | 应用 | 类别 | 理由 |
|------|------|------|------|
| 1 | **Homebrew** | 开发工具 | macOS 必备包管理器，所有命令行工具的安装入口 |
| 2 | **Raycast** | 效率工具 | 替代 Spotlight 的终极效率工具，集成窗口管理、AI、命令等 |
| 3 | **Rectangle** | 系统工具 | 免费开源窗口管理，还原 Windows 窗口操作体验 |
| 4 | **VS Code** | 开发环境 | 通用代码编辑器，插件生态最丰富 |
| 5 | **Rider** | 开发环境 | C# 开发首选，完美替代 Visual Studio |
| 6 | **Docker Desktop** | 开发工具 | 容器化开发必备，M1 版已成熟 |
| 7 | **iTerm2 + Oh My Zsh** | 终端工具 | 开发者终端终极组合 |
| 8 | **1Password** | 效率工具 | 开发者账号管理必备 |
| 9 | **Chrome** | 浏览器 | 开发者工具最强大 |
| 10 | **Postman** | 开发工具 | API 测试行业标准 |

---

## 8. Homebrew 一键安装脚本

```bash
#!/bin/bash

# 安装 Homebrew (必须先执行)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 开发工具
brew install --cask visual-studio-code
brew install --cask jetbrains-rider
brew install --cask pycharm-ce
brew install --cask docker
brew install --cask tableplus
brew install --cask dbngin
brew install --cask postman
brew install --cask insomnia
brew install --cask github-desktop
brew install --cask fork
brew install --cask termius

# 终端工具
brew install iterm2
brew install wget
brew install curl
brew install git
brew install gh
brew install tree
brew install fzf
brew install zsh
brew install zsh-autosuggestions
brew install zsh-syntax-highlighting

# DevOps 工具
brew install kubectl
brew install terraform
brew install helm
brew install minikube
brew install kubectx

# 系统工具
brew install --cask rectangle
brew install --cask clipy
brew install --cask xnip
brew install --cask keka

# 效率工具
brew install --cask raycast
brew install --cask obsidian
brew install --cask notion
brew install --cask 1password
brew install --cask bitwarden

# 娱乐媒体
brew install --cask iina
brew install --cask vlc
brew install --cask spotify

# 浏览器
brew install --cask google-chrome
brew install --cask firefox
brew install --cask microsoft-edge

# 办公协作
brew install --cask microsoft-outlook
brew install --cask钉钉
brew install --cask wechat

# 云存储
brew install --cask aliyun-drive
```

---

## 9. 安装顺序建议

### 第一阶段：基础设置 (Day 1)

1. **登录 Apple ID** - 设置 iCloud同步
2. **安装 Homebrew** - 所有工具的入口
3. **安装 Chrome / Edge** - 浏览器是生产工具
4. **安装 Rectangle** - 解决窗口管理问题
5. **安装 Clipy** - 剪贴板历史
6. **安装 1Password / Bitwarden** - 密码管理

### 第二阶段：开发环境 (Day 1-2)

1. **安装 VS Code** - 通用编辑器
2. **安装 iTerm2 + Oh My Zsh** - 终端配置
3. **安装 Git + GitHub Desktop** - 版本控制
4. **安装 Docker Desktop** - 容器化环境
5. **安装 Rider** - C# 开发
6. **安装 PyCharm** - Python 开发

### 第三阶段：效率提升 (Day 2-3)

1. **安装 Raycast** - 效率神器
2. **安装 Postman / Insomnia** - API 测试
3. **安装 TablePlus + DBngin** - 数据库管理
4. **安装 Obsidian** - 笔记和知识管理

### 第四阶段：日常工具 (Week 1)

1. **安装微信、钉钉** - 即时通讯
2. **安装腾讯会议 / Zoom** - 视频会议
3. **安装 IINA** - 视频播放
4. **安装 Spotify** - 音乐
5. **安装 Microsoft 365** - 办公套件

### 第五阶段：优化完善 (Week 2+)

1. **安装 Xnip** - 高级截图
2. **安装 Bartender** - 菜单栏整理
3. **安装 iStat Menus** - 系统监控
4. **安装 CleanMyMac X** - 系统维护

---

## 参考资料

[^1]: [Rectangle - Reddit r/MacOS](https://www.reddit.com/r/MacOS/comments/15nla6q/must_have_apps_for_windows_switchers_from_a_week/), [AlternativeTo - Amethyst Alternatives](https://alternativeto.net/software/amethyst--tiling-window-manager-for-os-x/)

[^2]: [Xnip - XDA Developers](https://www.xda-developers.com/macos-apps-help-transition-from-windows/)

[^3]: [Bartender - TechRadar](https://www.techradar.com/news/the-best-m1-compatible-mac-apps)

[^4]: [iStat Menus - Setapp](https://setapp.com/app-reviews/best-mac-monitoring-software), [AlternativeTo - iStat Menus Alternatives](https://alternativeto.net/software/istat/)

[^5]: [CleanMyMac X vs MacKeeper - MacPaw](https://macpaw.com/cleanmymac/cleanmymac-vs-mackeeper)

[^6]: [1.1.1.1 - Woorkup](https://woorkup.com/best-mac-apps/)

[^7]: [Must-have tools for macOS developers - Medium](https://medium.com/@sumitsahoo/must-have-tools-and-apps-for-macos-for-developers-in-2023-6cc43dd83bcc)

[^8]: [Docker Desktop for Mac M1 - DEV Community](https://dev.to/maxym_babenko_40a0c9d9463/essential-macos-apps-for-developers-in-2025-3kop)

[^9]: [Insomnia vs Postman - Abstracta](https://abstracta.us/blog/testing-tools/insomnia-vs-postman/), [TechTarget](https://www.techtarget.com/searchapparchitecture/tip/A-quick-breakdown-of-Postman-vs-Insomnia)

[^10]: [DBngin - TablePlus](https://dbngin.com/), [TablePlus Blog](https://tableplus.com/blog/2019/09/sql-database-download.html)

[^11]: [iTerm2 - DEV Community](https://dev.to/maxym_babenko_40a0c9d9463/essential-macos-apps-for-developers-in-2025-3kop)

[^12]: [Termius - AlternativeTo](https://alternativeto.net/software/termius/)

[^13]: [Homebrew - The New Stack](https://thenewstack.io/homebrew-for-macos-developers/), [Top 20 Homebrew Packages - Bold Brew](https://bold-brew.com/blog/top-homebrew-packages-for-developers.html)

[^14]: [Raycast vs Alfred - Raycast Official](https://www.raycast.com/raycast-vs-alfred), [Reddit](https://www.reddit.com/r/macapps/comments/1d9dkyv/alfred_or_raycast_in_2024/)

[^15]: [Keka - AlternativeTo](https://alternativeto.net/software/keka/)

[^16]: [IINA - TechRadar](https://www.techradar.com/news/the-best-m1-compatible-mac-apps)

[^17]: [CleanMyMac X Review - MacKeeper](https://mackeeper.com/blog/cleanmymac-vs-mackeeper/)

[^18]: [Running Windows on M1 Mac - Lifehacker](https://lifehacker.com/7-apps-to-recreate-the-best-windows-features-on-your-ma-1850077805)

[^19]: [Configuring Your New MacBook Pro - Medium](https://medium.com/@gabrieldrouin/configuring-your-new-macbook-pro-a-2025-guide-for-developers-ee48bddb9033)

---

*文档创建日期：2026-04-10*
*适用于：MacBook Pro 16-inch M1 (2021款) / macOS 12+*
*目标用户：从 Windows 转向 macOS 的 C#/Python 后端开发者*