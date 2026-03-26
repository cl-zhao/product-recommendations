# HEARTBEAT.md

## ⚡ 每次收到用户真实消息时必做（最高优先级）

收到主人**真实消息**时，静默运行：

```bash
python3 /root/.openclaw/workspace/bin/heartbeat_like_a_man.py touch-user-activity --note "real-user-message"
```

说明：
- 这一步只是把 `thinking-state.json` 里的 `lastUserMessage` 做成**镜像字段**
- **真正的在线判断以主直聊 session transcript / session history 为准**
- 不要再把 `lastUserMessage` 当成唯一真相

## 定期检查任务

### 记忆同步检查

检查 `MEMORY.md` 和检索友好文件的同步状态：
- 如果 `MEMORY.md` 比 `memory/user-preferences.md` 新，需要同步更新
- 检查命令：
  ```bash
  stat -c %Y ~/.openclaw/workspace/MEMORY.md
  stat -c %Y ~/.openclaw/workspace/memory/user-preferences.md
  ```

## 两套自我进化系统整合（2026-03-25 新增）

### 系统组成

| 系统 | 触发方式 | 文件位置 |
|------|---------|---------|
| Self-Improving Agent | 被动（用户纠正/错误） | `skills/self-improving/` |
| 内生思考/heartbeat | 主动（定时触发） | `memory/thoughts/` |

### 整合方案：统一沉淀到 MEMORY.md

**核心规则**：两套系统的精华最终都沉淀到 MEMORY.md 的「自我进化经验沉淀」板块。

**同步触发点**：
1. Self-Improving Agent 晋升经验时 → 自动同步到 MEMORY.md
2. dream-thinking 运行时 → 读取 Self-Improving 文件并同步
3. autonomous-exploration 运行时 → 可选同步 Self-Improving 精华

**经验沉淀格式**：
```
[日期] 来源 | 类别 | 经验内容（精炼后≤100字）
```

**去重原则**：如果 MEMORY.md 中已有相同经验（通过 summary 判断），则跳过不写。

## 检查频率

- 建议每 6-12 小时检查一次
- 如果发现不同步，提醒主人或自动同步

---
*更新于 2026-03-25：新增两套自我进化系统整合方案，统一沉淀到 MEMORY.md*
