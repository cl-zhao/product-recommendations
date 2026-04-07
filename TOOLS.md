# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## GitHub 配置

- **账号**: cl-zhao
- **仓库**: product-recommendations
- **Token**: `[GITHUB_TOKEN]` (2026-03-26 更新)
- **Scopes**: repo, workflow, write:packages
- **Remote**: https://github.com/cl-zhao/product-recommendations.git

### ⚠️ 重要规则
- **禁止使用 `git push --force`**
- **只添加内容，不删除/修改已有文件**
- 推送前先 `git pull` 同步远程变更

### 常用命令
```bash
# 推送到 GitHub
git add <file>
git commit -m "描述"
git push origin main

# 同步远程
git pull origin main --no-rebase

# 查看状态
git status
git log --oneline -5
```
