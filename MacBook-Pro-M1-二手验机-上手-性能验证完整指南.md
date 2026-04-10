# MacBook Pro M1 二手验机 · 上手 · 性能验证 — Windows 用户完整指南

> 适用机型：MacBook Pro 14" 2021 款（M1 Pro/Max 芯片）
> 目标读者：从 Windows 转向 macOS 的开发者
> 调研日期：2026-04-10
> 数据来源：子代理并行调研（硬件验机 / Windows 用户上手 / 性能验证）

---

## 📋 目录

1. [硬件验机指南](#1-硬件验机指南)
2. [macOS 初始化与 Windows 用户上手](#2-macos-初始化与-windows-用户上手)
3. [性能验证与跑分指南](#3-性能验证与跑分指南)
4. [快速检查清单汇总](#4-快速检查清单汇总)

---

## 1. 硬件验机指南

> 面向没有用过 Mac 的 Windows 用户，每一步都有操作说明。

### 1.1 验机前准备

| 准备项 | 说明 |
|--------|------|
| U 盘（16GB+）| 用于制作 macOS 安装盘（备用）|
| 参考手机 | 拍下验机过程留证 |
| 网络 | 连接 Wi-Fi 下载验机工具 |

**Mac 基础操作速查（Windows 对照）：**

| Windows 习惯 | Mac 对应 |
|-------------|---------|
| `Win` 键 | `Command (⌘)` 键 |
| `Ctrl` 键 | `Control` 键 |
| `Alt` 键 | `Option (⌥)` 键 |
| 文件资源管理器 | `Finder`（`Command + N`）|
| 任务管理器 | `活动监视器`（`Command + 空格` 搜索）|
| 终端 | `Terminal`（`Command + 空格` 搜索）|

---

### 1.2 电池健康检测

**方法一：系统自带（最简单）**

1. 点击左上角 **🍎 苹果图标** → **关于本机**
2. 点击 **"服务"** → **"电池健康"**
3. 查看关键指标：

| 指标 | 正常值 | 需要注意 |
|-----|-------|---------|
| **最大容量** | ≥ 80% | < 80% 建议更换 |
| **循环次数** | ≤ 1000 次 | > 1000 电池明显衰减 |

**方法二：命令行（更详细）**

打开终端（`Command + 空格` → 输入 "Terminal" → 回车），输入：

```bash
ioreg -l -w0 | grep -i "cyclecount"
ioreg -l -w0 | grep -i "maxcapacity"
```

**输出解读：**
- `CycleCount`：循环次数（0-1000 为健康）
- `MaxCapacity`：当前最大容量百分比

**方法三：第三方工具（最直观）**

推荐 **coconutBattery**（免费）：

1. 下载：https://www.coconut-flavour.com/coconutbattery/
2. 安装后打开，直接显示：
   - Design Capacity（设计容量）
   - Current Capacity（当前容量）
   - Cycle Count（循环次数）

**电池更换标准：**
- 循环次数 **> 1000** 或 最大容量 **< 80%** → 建议更换
- Apple 官方更换费用：约 ¥1500-2000

---

### 1.3 屏幕检测

**检查亮点 / 暗点：**

1. 下载 **Display Tester**（App Store 免费）
2. 或打开 Safari 访问：https://www.eizoglobal.com/library/test-images/
3. 全屏播放纯色（黑、白、红、绿、蓝）检查

**简单方法（终端）：**

```bash
# 打开纯色窗口
open /System/Library/Frameworks/ScreenSaver.framework/Resources/ScreenSaverEngine.app
```

选择不同纯色背景，肉眼观察是否有：
- ❌ 白背景下的黑点（暗点）
- ❌ 黑背景下的白点（亮点）
- ❌ 固定位置的颜色残影（烧屏）

**检查烧屏：**
1. 打开 TextEdit，全黑文档，调至最高亮度
2. 观察是否有残影
3. 换成全白文档检查

---

### 1.4 风扇检测

**方法一：安装 iStat Menus（推荐）**

1. 下载：https://bjango.com/mac/istatmenus/
2. 安装后菜单栏显示 CPU / 温度 / 风扇转速
3. 观察风扇是否随负载自动加速

**方法二：命令行：**

```bash
sudo powermetrics --samplers smc | grep -i "fan"
```

**压力测试（5 分钟）：**

1. 下载 **Geekbench**（App Store）
2. 运行 CPU 压力测试
3. 观察：
   - ✅ 风扇是否启动
   - ✅ 转速是否随温度上升
   - ❌ 是否有啸叫 / 摩擦声

**异常情况：**
- 风扇完全不转 → 需检查
- 啸叫 / 摩擦声 → 可能轴承问题
- 温度异常高（> 100°C 持续）→ 需检修

---

### 1.5 键盘检测

**逐键测试：**

1. 打开 TextEdit
2. 按每个键输入对应字符
3. 重点检查：空格、Shift、Ctrl、Command、Delete、方向键

**盲打测试表（复制粘贴到 TextEdit）：**
```
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
0123456789
!@#$%^&*()_+-=[]{}|;':",./<>?
```

**Touch Bar 检测（如有机型）：**
1. 系统偏好设置 → 键盘 → Touch Bar
2. 测试滑动亮度 / 音量是否流畅
3. 按压按钮是否有反馈
4. Touch ID（指纹）是否正常

---

### 1.6 触控板检测

**多点触控测试：**

| 手势 | 功能 | 测试方法 |
|-----|------|---------|
| 单指点击 | 选中 / 点击 | 点击不同位置 |
| 双指点击 | 右键 | 双指轻点 |
| 双指滚动 | 滚动页面 | 双指上下滑动 |
| 双指捏合 | 缩放 | 双指张开 / 捏合 |
| 三指滑动 | 切换应用 | 三指左右滑动 |
| 四指上滑 | 调度中心 | 四指向上滑动 |

**力度感应测试：**
1. 系统偏好设置 → 触控板
2. 勾选"轻点来点按"
3. 测试不同力度点击是否有不同反馈

---

### 1.7 摄像头 / 麦克风检测

**摄像头测试：**

1. 打开 **Photo Booth**（`Command + 空格` 搜索）
2. 观察画面是否清晰、无噪点、无黑屏
3. 测试拍照 / 录像功能

**麦克风测试：**

1. 打开 **语音备忘录**（`Command + 空格` 搜索）
2. 录制一段语音
3. 播放检查是否有杂音 / 失真
4. 或：系统偏好设置 → 声音 → 输入，对着麦克风说话观察输入电平是否跳动

---

### 1.8 扬声器检测

**测试方法：**

1. 系统偏好设置 → 声音 → 输出
2. 选择"MacBook Pro 扬声器"
3. 调整音量滑块，检查是否有爆音 / 杂音
4. 播放不同类型音乐（人声、器乐、低音）检查是否有破音或异响

---

### 1.9 接口检测

**MacBook Pro 14" 2021 接口分布：**

| 位置 | 接口 | 测试方法 |
|-----|------|---------|
| 左侧 | 2× Thunderbolt 4 (USB-C) | 插入 U 盘 / 硬盘 / 充电器 |
| 右侧 | 1× Thunderbolt 4 (USB-C) | 同上 |
| 右侧 | 1× HDMI 接口 | 连接外接显示器 |
| 右侧 | 1× SD 卡槽 | 插入 SD 卡 |
| 右侧 | 1× 3.5mm 耳机孔 | 插入耳机测试音频 |

**接口测试清单：**
- [ ] 每个 USB-C 接口插入 U 盘测试数据传输
- [ ] MagSafe 充电是否正常
- [ ] HDMI 输出外接显示器是否正常
- [ ] SD 卡槽识别 SD 卡
- [ ] 耳机孔音频输出

---

### 1.10 Wi-Fi / 蓝牙检测

**Wi-Fi 测试：**
1. 连接 Wi-Fi（支持 Wi-Fi 6）
2. 测试 2.4GHz 和 5GHz 频段
3. 访问 https://speedtest.net 测速

**蓝牙测试：**
1. 系统偏好设置 → 蓝牙
2. 配对测试：无线鼠标、键盘、AirPods
3. 检查是否断连或延迟明显

---

### 1.11 存储健康检测

**SSD 健康度：**

```bash
# 安装 smartmontools
brew install smartmontools

# 检查 SSD 健康
smartctl -a /dev/disk0
```

**读写速度测试（Blackmagic Disk Speed Test）：**

1. 下载：https://www.blackmagicdesign.com/products/blackmagicosxfs（免费）
2. 打开 → 点击 "Start"
3. 等待结果

**M1 Pro 参考速度（1TB 版本）：**

| 测试项 | 预期速度 |
|--------|---------|
| 顺序读取 | 5,000-7,400 MB/s |
| 顺序写入 | 3,900-7,000 MB/s |

> ⚠️ 512GB 版本比 1TB 版本读写速度低约 30%，这是正常的，不是故障。

---

## 2. macOS 初始化与 Windows 用户上手

### 2.1 macOS 首次开机设置

**Apple ID 创建（必做）：**

1. 开机后选择"创建 Apple ID"
2. 建议使用 Gmail 或 Outlook 邮箱（国内邮箱有时收不到验证码）
3. 开启**双重认证**（必开！）

**iCloud 推荐配置：**

| 功能 | 推荐状态 |
|------|---------|
| iCloud Drive | ✅ 开启 |
| 照片 | ✅ 开启 |
| 备忘录 | ✅ 开启 |
| 钥匙串 | ✅ 开启（密码管理）|
| 查找 Mac | ✅ 开启（防丢）|

---

### 2.2 系统偏好设置必改配置

按 `Command + ,` 打开系统偏好设置：

```
通用
├── 外观：深色模式（开发者首选）
├── 菜单栏：勾选"电池百分比"
└── 关于本机 → 存储空间：点"管理"查看占用

触控板
├── 全部勾选触控手势
├── 关闭"查找"的三指轻点（与 JetBrains 冲突）
└── 开启"辅助点按"= 右键菜单

电池
├── 开启"使用电池时自动调节亮度"
└── 关于续航：MacBook Pro M1 Pro 实际 11-14 小时

网络
└── Wi-Fi → 位置：创建"自动"位置

键盘
├── 快捷键 → 选择"所有控制"
└── 输入法 → 添加自己习惯的输入法
```

---

### 2.3 Windows → macOS 核心概念对照

| macOS | Windows 对应 | 说明 |
|-------|------------|------|
| **Finder** | 文件资源管理器 | `Command + E` 或点击 Dock 笑脸 |
| **系统偏好设置** | 控制面板 | 相当于设置 + 控制面板 |
| **启动台 (Launchpad)** | 开始菜单 | `F4` 或 Dock 里火箭图标 |
| **程序坞 (Dock)** | 任务栏 | 底部放常用 app 的横条 |
| **活动监视器** | 任务管理器 | `Command + 空格` 搜索 |
| **终端 (Terminal)** | CMD / PowerShell | `Command + 空格` 搜索 |
| **废纸篓** | 回收站 | Dock 最右边 |
| **Safari** | Edge | macOS 自带浏览器 |

> 💡 **记住**：macOS 没有 C 盘 D 盘，只有 **Macintosh HD**。文件放在 **/Users/你的用户名/** 下。

---

### 2.4 键盘快捷键差异（最关键）

| Windows | macOS |
|---------|-------|
| `Ctrl + C` | `Command + C`（复制）|
| `Ctrl + V` | `Command + V`（粘贴）|
| `Ctrl + X` | `Command + X`（**但不能剪文件！**）|
| `Ctrl + Z` | `Command + Z`（撤销）|
| `Ctrl + S` | `Command + S`（保存）|
| `Ctrl + A` | `Command + A`（全选）|
| `Ctrl + F` | `Command + F`（查找）|
| `Ctrl + Tab` | `Command + Tab`（切换应用）|
| `Win` | `Command` (⌘) |
| `F5` | `Command + R`（刷新）|

> 🎯 **核心区别**：macOS 用 `Command` 键替代了 `Ctrl` 的位置！

**文件剪切（macOS 没有，但有替代）：**
- `Command + C` 复制 → `Command + Option + V` 移动（不是复制）
- 或直接拖拽文件到目标文件夹

---

### 2.5 截图快捷键

| 功能 | 快捷键 | 保存位置 |
|------|--------|---------|
| 全屏截图 | `Command + Shift + 3` | 桌面 |
| 区域截图 | `Command + Shift + 4` | 桌面 |
| 窗口截图 | `Command + Shift + 4` + 空格 | 桌面 |
| 截图到剪贴板 | `Command + Shift + 4` 然后按 `Control` | 剪贴板 |

> 💡 推荐安装 **Xnip**（免费）：截图后可以直接贴图标注，比 Windows Snipping Tool 更好用。

---

### 2.6 窗口分屏

**Windows**：拖拽窗口到屏幕边缘 → Snap 分屏
**macOS**：
1. 窗口拖到屏幕最顶部 → 出现分屏选项 → 选择左 / 右半屏
2. 快捷键：`Control + Command + F` 进入全屏

**推荐安装 Rectangle**（免费，比 Windows Snap 更好用）：
```bash
brew install rectangle
```

---

### 2.7 必备软件清单

#### 🧰 工具类

| 软件 | 用途 | 安装方式 |
|------|------|---------|
| **Homebrew** | macOS 包管理器（必备）| 终端安装（见 2.8）|
| **Chrome / Firefox** | 浏览器 | 官网下载 |
| **The Unarchiver** | 解压 rar / 7z | App Store |
| **VLC** | 视频播放器 | 官网下载 |
| **Xnip** | 截图 + 标注 | App Store |

#### 💼 办公类

| 软件 | 用途 |
|------|------|
| **Microsoft 365** | Word / Excel / PPT |
| **WPS** | 免费国产办公套件 |
| **Notion** | 笔记 / 知识库 |
| **Obsidian** | 本地笔记 |

#### 🖥️ 开发类

| 软件 | 用途 |
|------|------|
| **VS Code** | 轻量级编辑器 |
| **Rider** | C# 开发（你的主力）|
| **PyCharm** | Python 开发 |
| **Docker Desktop** | 容器化 |
| **iTerm2** | 终端替代品（比自带更强）|

#### ⌨️ 输入法

推荐先用**系统自带拼音**，干净无广告。后期可考虑 **RIME**。

---

### 2.8 Homebrew 安装（第一步必做）

Homebrew 是 macOS 最重要的包管理器，相当于 Linux 的 apt / yum。

打开终端，运行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

验证安装成功：

```bash
brew --version
# 输出类似: Homebrew 4.x.x
```

---

### 2.9 开发环境配置（C# / Python 后端）

#### 安装 .NET SDK

```bash
brew install --cask dotnet-sdk
dotnet --version
```

#### 安装 Python

```bash
brew install python@3.11
python3 --version
pip3 --version
```

**配置 pip 镜像（国内加速）：**

```bash
mkdir -p ~/.pip
cat > ~/.pip/pip.conf <<'EOF'
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
EOF
```

#### 安装 Docker Desktop

```bash
brew install --cask docker
```

> ⚠️ **M1 注意**：下载 Apple Silicon 版本！安装后打开 Docker Desktop，等待绿色灯亮起。

#### Git + SSH Key 配置

```bash
# 配置 Git
git config --global user.name "你的名字"
git config --global user.email "your@email.com"

# 生成 SSH Key
ssh-keygen -t ed25519 -C "your@email.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub
```

1. 打开 https://github.com/settings/keys
2. 点击 **New SSH key**
3. 粘贴公钥内容
4. 验证：`ssh -T git@github.com`

#### iTerm2 + Oh My Zsh

```bash
# 安装 iTerm2
brew install --cask iterm2

# 安装 Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

---

### 2.10 macOS 日常维护

**磁盘清理：**
- 苹果图标 → 关于本机 → 存储空间 → 点"管理"
- `brew cleanup`（清理旧版本 Homebrew 包）
- `brew autoremove`（清理不需要的依赖）

**内存管理：**
- **不需要像 Windows 那样经常重启！**
- macOS 内存管理比 Windows 好很多
- **不需要清内存 app**（都是智商税）

**强制退出卡死程序：**
`Command + Option + Esc` → 选择程序 → 点"强制退出"

---

## 3. 性能验证与跑分指南

### 3.1 M1 Pro 基准性能数据

| 测试项目 | M1 Pro (8P+2E CPU / 14GPU) | M1 Pro (10P+2E CPU / 16GPU) |
|---------|-------------------------------|-------------------------------|
| **Geekbench 6 单核** | ~2,360 | ~2,380 |
| **Geekbench 6 多核** | ~10,300 | ~12,500+ |
| **Cinebench R23 单核** | ~1,540 | ~1,540 |
| **Cinebench R23 多核** | ~12,000 | ~14,000 |

**SSD 读写速度（1TB）：**

| 方向 | 速度 |
|------|------|
| 顺序读取 | ~7,000 MB/s |
| 顺序写入 | ~5,000+ MB/s |

> ⚠️ 512GB 版本比 1TB 速度低约 30%（单通道），正常。

---

### 3.2 跑分操作步骤

#### Geekbench 6（推荐）

1. App Store 搜索 "Geekbench 6" 安装（免费）
2. 打开 → 点击 "CPU Benchmark"
3. 点击 "Run CPU Benchmark"
4. 等待 3-5 分钟出结果

**结果判断：**
- ✅ 单核 > 2,000 = 正常
- ✅ 多核 > 10,000（8核）/ 12,000（10核）= 正常

#### Blackmagic Disk Speed Test

1. 下载：https://www.blackmagicdesign.com/products/blackmagicosxfs（免费）
2. 打开 → 点击 "Start"
3. 等待 30 秒

**结果判断：**
- ✅ 读取 > 3,000 MB/s = 正常
- ✅ 写入 > 2,500 MB/s（512GB）/ 4,500 MB/s（1TB）= 正常

---

### 3.3 M1 Pro vs 其他芯片对比

| 型号 | 单核 | 多核 | 说明 |
|------|------|------|------|
| **M1 Pro (10核)** | ~2,380 | ~12,500 | 2021 MacBook Pro |
| **M1 普通版** | ~2,300 | ~7,700 | M1 Pro 多核强 34% |
| **Intel i7-11800H** | ~1,600 | ~9,000 | 2021 游戏本常见 |
| **M3 Air** | ~3,000 | ~10,500 | 单核更强，但多核弱于 M1 Pro |

**结论**：M1 Pro 至今性能仍然非常强，多核性能接近 2022 年 Intel i7-12700H 水平。

---

### 3.4 M1 Mac 必须知道的事情

#### Rosetta 2（原理解释）

Rosetta 2 是苹果的"翻译层"，让 x86 软件能在 ARM Mac 上运行。

**性能损失**：约 10-20%，日常使用感知不强。

**自动提示**：首次打开 Intel 软件时会弹出安装提示，点击"安装"即可。

**手动安装：**
```bash
softwareupdate --install-rosetta
```

#### 如何判断软件是 ARM 原生还是 Intel

1. Finder → Applications → 右键点击 App → "显示简介"
2. 查找"种类"：
   - ✅ "Apple Silicon" = 原生 ARM
   - ❌ "Intel" = 需要 Rosetta 转译

#### Homebrew 安装注意

| 版本 | 安装路径 | 适用 |
|------|---------|------|
| **ARM 版（推荐）** | `/opt/homebrew` | 原生 ARM，速度快 |
| x86 版 | `/usr/local` | 需要跑旧 Intel 软件 |

ARM 版为默认版本，一般不需要手动指定。

#### Docker Desktop M1 注意事项

- ✅ 下载 **Apple Silicon** 版本（不是 Intel 版）
- 官方镜像（如 nginx、mysql）基本都有 `arm64v8` 版本
- 如果报错 `exec format error`，尝试加 `--platform linux/amd64`（但会有性能损失）

---

### 3.5 温度和续航验证

**正常温度范围：**

| 状态 | 温度 |
|------|------|
| 空闲 / 日常办公 | 35-45°C |
| 浏览网页 / 文档 | 40-55°C |
| 轻度负载（看视频）| 50-65°C |
| 满载（渲染 / 跑分）| 80-100°C |

> 🌡️ M1 Pro 最高可跑到 100°C 不降频，偶尔跑到 90-100°C 不用慌。

**风扇噪音：**

| 状态 | 转速 | 噪音 |
|------|------|------|
| 空闲 | 停转或 ~1000 RPM | **0 dB 静音** |
| 中等负载 | 2000-3000 RPM | ~25-30 dB（几乎听不见）|
| 满载 | 5000-6000 RPM | ~35-40 dB（能听到但不吵）|

**续航实测：**
- 官方参考：无线上网 11-14 小时
- 充满电 → 亮度 75% → 播放 YouTube 1080P 视频 → 记录到 20% 的时间

---

### 3.6 常见问题排查

**风扇狂转：**
1. 活动监视器 → 按 CPU 排序 → 找高占用进程
2. 重置 SMC：关机 → 按住 `Control + Option + Shift + 电源键` 10 秒 → 等 30 秒再开机
3. 检查是否在跑系统更新

**发热异常：**
1. 是否正在充电（充电发热正常）
2. 降低屏幕亮度
3. 关闭 Chrome（CPU 占用高）
4. 活动监视器找高占用进程

**Wi-Fi 断连：**
1. 系统设置 → 网络 → 忽略此网络 → 重新连接
2. 关闭蓝牙试试（部分设备存在干扰）
3. 更新 macOS

**USB-C 不识别：**
1. 换个端口试试（有些端口供电不足）
2. 换根线（有些线材质量差）
3. 重置 SMC
4. 苹果菜单 → 关于本机 → 系统报告 → USB → 查看是否识别

---

## 4. 快速检查清单汇总

### 硬件验机

```
□ 电池：循环次数 < 1000，最大容量 > 80%
□ 屏幕：无亮点 / 暗点 / 烧屏
□ 风扇：随负载自动启动，无异响
□ 键盘：每个按键正常，Touch Bar（如有）正常
□ 触控板：多点触控、力度感应正常
□ 摄像头：画面清晰，无黑屏
□ 麦克风：录音清晰，无杂音
□ 扬声器：播放正常，无破音
□ 接口：每个接口正常工作
□ Wi-Fi / 蓝牙：连接稳定
□ 存储：读写速度正常（读取 > 3000 MB/s）
```

### 性能跑分

```
□ Geekbench 6 单核 > 2,000
□ Geekbench 6 多核 > 10,000（8核）/ 12,000（10核）
□ SSD 读取 > 3,000 MB/s
□ 风扇日常使用基本静音
□ 温度空闲时 < 50°C
□ Wi-Fi 稳定不断连
□ USB-C 正常识别设备
```

### 初次设置

```
□ Apple ID 登录 + iCloud 开启
□ 系统偏好设置调整（深色模式、触控板、电池）
□ Homebrew 安装成功
□ Chrome / VS Code / Rider / PyCharm 安装
□ Docker Desktop 安装并运行（绿色灯亮）
□ Git 配置 + SSH key 添加到 GitHub
□ iTerm2 + Oh My Zsh 装好
□ 截图软件（Xnip）安装
□ Rectangle 窗口管理安装
□ .NET SDK 和 Python 安装
```

### 二手 MacBook Pro M1 Pro 购买建议总结

| 检查项 | 合格标准 | 不合格处理 |
|--------|---------|----------|
| 电池循环次数 | < 500 次（优秀）/ < 1000 次（正常）| 预留 ¥1,500 换电池 |
| 电池最大容量 | > 85%（优秀）/ > 80%（正常）| 换电池或压价 |
| 屏幕 | 无亮点 / 暗点 / 烧屏 | 要求降价或退货 |
| 机身外观 | 无异常划痕 / 磕碰 | 拍照留证 |
| 在保状态 | 在保优先 | 压价理由 |
| SSD 读写速度 | 读取 > 3000 MB/s | 可能有硬件问题 |

---

## 📚 参考资源

- Apple 官方 Mac 使用手册：https://support.apple.com/zh-cn/guide/mac-help/welcome/mac
- Homebrew 官网：https://brew.sh
- Apple 官方技术规格：https://support.apple.com/zh-cn/111893
- coconutBattery 下载：https://www.coconut-flavour.com/coconutbattery/
- Blackmagic Disk Speed Test：https://www.blackmagicdesign.com/products/blackmagicosxfs
- iStat Menus：https://bjango.com/mac/istatmenus/

---

*本指南由子代理并行调研生成（2026-04-10）*
*涵盖：硬件验机 / Windows 用户上手 / 性能验证三大模块*
