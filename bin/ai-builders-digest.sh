#!/bin/bash
# ============================================================================
# AI Builders Digest - 自动执行并推送到 GitHub
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FEED_DIR="$SCRIPT_DIR/feed-cache"
OUTPUT_DIR="$SCRIPT_DIR/output"
GITHUB_REPO_DIR="$SCRIPT_DIR/../product-recommendations"

# 创建必要目录
mkdir -p "$FEED_DIR" "$OUTPUT_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === 开始执行 AI Builders Digest ==="

# 1. 获取 feed 数据
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 获取 AI Builders Digest 数据..."

# 使用 Node.js 执行 prepare-digest.js
cd ~/.openclaw/workspace/skills/.agents/skills/follow-builders

# 检查 node_modules 是否存在
if [ ! -d "node_modules" ]; then
    echo "安装依赖..."
    cd scripts && npm install --silent 2>/dev/null && cd ..
fi

# 获取 tweets feed
echo "获取 tweets feed..."
curl -s "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json" -o "$FEED_DIR/feed-x.json" 2>/dev/null

# 获取 podcasts feed
echo "获取 podcasts feed..."
curl -s "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json" -o "$FEED_DIR/feed-podcasts.json" 2>/dev/null

# 获取 prompts
echo "获取 prompt 模板..."
mkdir -p "$FEED_DIR/prompts"
for prompt in summarize-podcast summarize-tweets digest-intro translate; do
    curl -s "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/prompts/${prompt}.md" -o "$FEED_DIR/prompts/${prompt}.md" 2>/dev/null
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Feed 数据获取完成"

# 2. 解析 feed 数据
TWEETS_COUNT=$(grep -o '"id"' "$FEED_DIR/feed-x.json" 2>/dev/null | wc -l || echo "0")
PODCASTS_COUNT=$(grep -o '"id"' "$FEED_DIR/feed-podcasts.json" 2>/dev/null | wc -l || echo "0")

echo "获取到 $TWEETS_COUNT 条 tweets, $PODCASTS_COUNT 个 podcasts"

# 3. 生成 markdown 文档
DATE=$(date '+%Y-%m-%d')
DATE_FULL=$(date '+%Y-%m-%d %H:%M:%S')
DATE_READABLE=$(date '+%Y年%m月%d日 %H:%M')

# 创建 AI Builders Digest markdown 文件
cat > "$OUTPUT_DIR/ai-builders-digest-${DATE}.md" << MARKER
# AI Builders Digest - ${DATE_READABLE}

> 由 OpenClaw 自动生成 | 数据来源: Follow Builders Project

---

## 📊 今日概览

- **Tweets**: ${TWEETS_COUNT} 条更新
- **Podcasts**: ${PODCASTS_COUNT} 个更新

---

## 🐦 AI Builders 最新动态

MARKER

# 从 feed 中提取 tweets 内容并格式化
python3 << 'PYTHON'
import json
import sys
from datetime import datetime

feed_x_path = "/root/.openclaw/workspace/bin/feed-cache/feed-x.json"
output_temp = "/root/.openclaw/workspace/bin/output/ai-builders-digest-temp.md"

try:
    with open(feed_x_path, 'r') as f:
        feed_data = json.load(f)
    
    # 新的 feed 结构：x 数组，每个元素包含 builder 信息和 tweets 数组
    builders = feed_data.get('x', []) if isinstance(feed_data, dict) else []
    
    if builders:
        all_tweets = []
        for builder in builders:
            builder_name = builder.get('name', 'Unknown')
            builder_handle = builder.get('handle', '')
            tweets = builder.get('tweets', [])
            for tweet in tweets:
                tweet['builder_name'] = builder_name
                tweet['builder_handle'] = builder_handle
                all_tweets.append(tweet)
        
        # 只取前20条
        all_tweets = all_tweets[:20]
        
        with open(output_temp, 'w') as out:
            for i, tweet in enumerate(all_tweets, 1):
                builder_name = tweet.get('builder_name', 'Unknown')
                builder_handle = tweet.get('builder_handle', '')
                content = tweet.get('text', '')
                created_at = tweet.get('createdAt', '')
                url = tweet.get('url', '')
                likes = tweet.get('likes', 0)
                retweets = tweet.get('retweets', 0)
                
                # 格式化时间
                time_str = ''
                if created_at:
                    try:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        time_str = dt.strftime('%m-%d %H:%M')
                    except:
                        time_str = created_at[:10]
                
                # 清理内容中的特殊字符
                content = content.replace('\\n', '\n').replace('\\\"', '"').replace('#', '#')
                
                out.write(f"### {i}. @{builder_handle}\n\n")
                out.write(f"**{builder_name}** · {time_str}\n\n")
                out.write(f"{content}\n\n")
                if url:
                    out.write(f"🔗 [查看原文]({url})\n")
                out.write(f"❤️ {likes} · 🔁 {retweets}\n\n")
                out.write("---\n\n")
        
        print(f"处理了 {len(all_tweets)} 条 tweets")
    else:
        print("Tweets 数据格式不正确")
        sys.exit(1)
except Exception as e:
    print(f"处理 tweets 时出错: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON

# 将 temp 文件内容追加到主文件
if [ -f "$OUTPUT_DIR/ai-builders-digest-temp.md" ]; then
    cat "$OUTPUT_DIR/ai-builders-digest-temp.md" >> "$OUTPUT_DIR/ai-builders-digest-${DATE}.md"
    rm "$OUTPUT_DIR/ai-builders-digest-temp.md"
fi

# 添加 podcasts 部分
cat >> "$OUTPUT_DIR/ai-builders-digest-${DATE}.md" << MARKER

## 🎙️ Podcasts 更新

MARKER

# 从 podcasts feed 提取内容
python3 << 'PYTHON'
import json
from datetime import datetime

feed_podcasts_path = "/root/.openclaw/workspace/bin/feed-cache/feed-podcasts.json"
output_podcasts_temp = "/root/.openclaw/workspace/bin/output/ai-builders-podcasts-temp.md"

try:
    with open(feed_podcasts_path, 'r') as f:
        feed_data = json.load(f)
    
    # 新的 feed 结构可能不同，检查 podcasts 字段
    podcasts = None
    if isinstance(feed_data, dict):
        podcasts = feed_data.get('podcasts', feed_data.get('youtube', []))
    else:
        podcasts = feed_data
    
    if isinstance(podcasts, list):
        podcasts = podcasts[:10]  # 只取前10个
        
        with open(output_podcasts_temp, 'w') as out:
            for i, podcast in enumerate(podcasts, 1):
                title = podcast.get('title', 'Untitled')
                channel = podcast.get('channel', podcast.get('channelTitle', podcast.get('channel', 'Unknown')))
                url = podcast.get('url', podcast.get('link', podcast.get('videoUrl', '')))
                published = podcast.get('published', podcast.get('pubDate', podcast.get('createdAt', '')))
                description = podcast.get('description', podcast.get('summary', podcast.get('transcript', '')))
                
                # 格式化时间
                time_str = ''
                if published:
                    try:
                        dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                        time_str = dt.strftime('%Y-%m-%d')
                    except:
                        time_str = str(published)[:10]
                
                out.write(f"### {i}. {title}\n\n")
                out.write(f"**频道**: {channel}\n")
                if time_str:
                    out.write(f"**发布时间**: {time_str}\n")
                if url:
                    out.write(f"**链接**: {url}\n\n")
                if description:
                    # 清理描述
                    description = description.replace('\\n', '\n').replace('\\\"', '"')
                    if len(description) > 300:
                        description = description[:300] + "..."
                    out.write(f"{description}\n\n")
                out.write("---\n\n")
        
        print(f"处理了 {len(podcasts)} 个 podcasts")
    else:
        print("Podcasts 数据为空或格式不正确")
        # 创建一个空的 podcasts temp 文件
        with open(output_podcasts_temp, 'w') as out:
            out.write("*暂无 podcasts 更新*\n\n")
except Exception as e:
    print(f"处理 podcasts 时出错: {e}")
    import traceback
    traceback.print_exc()
PYTHON

# 将 podcasts temp 文件内容追加到主文件
if [ -f "$OUTPUT_DIR/ai-builders-podcasts-temp.md" ]; then
    cat "$OUTPUT_DIR/ai-builders-podcasts-temp.md" >> "$OUTPUT_DIR/ai-builders-digest-${DATE}.md"
    rm "$OUTPUT_DIR/ai-builders-podcasts-temp.md"
fi

# 添加页脚
cat >> "$OUTPUT_DIR/ai-builders-digest-${DATE}.md" << MARKER

---

## 📚 相关资源

- **Follow Builders Project**: https://github.com/zarazhangrui/follow-builders
- **数据更新频率**: Tweets 每 6 小时, Podcasts 每 24 小时

---

*文档生成时间: ${DATE_FULL}*
*由 OpenClaw AI Builders Digest 自动生成*
MARKER

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Markdown 文档生成完成: $OUTPUT_DIR/ai-builders-digest-${DATE}.md"

# 4. 推送到 GitHub
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 推送到 GitHub..."

# 检查仓库是否存在
if [ ! -d "$GITHUB_REPO_DIR" ]; then
    echo "克隆 GitHub 仓库..."
    cd "$SCRIPT_DIR"
    git clone https://github.com/cl-zhao/product-recommendations.git "$GITHUB_REPO_DIR" 2>/dev/null
fi

cd "$GITHUB_REPO_DIR"

# 配置 git
git config user.email "agent@openclaw.ai" 2>/dev/null
git config user.name "OpenClaw Agent" 2>/dev/null

# 创建 AI Builders Digest 目录（如果不存在）
mkdir -p "$GITHUB_REPO_DIR/ai-builders-digest"

# 复制文件
cp "$OUTPUT_DIR/ai-builders-digest-${DATE}.md" "$GITHUB_REPO_DIR/ai-builders-digest/"

# 添加到 git
git add "ai-builders-digest/ai-builders-digest-${DATE}.md"

# 检查是否有更改
if git diff --cached --quiet; then
    echo "没有新的更改需要提交"
else
    # 提交
    git commit -m "Add AI Builders Digest - ${DATE_READABLE}

- Tweets: ${TWEETS_COUNT} 条更新
- Podcasts: ${PODCASTS_COUNT} 个更新
- 自动生成 by OpenClaw"
    
    # 推送到 GitHub
    git push origin main 2>/dev/null || git push https://github.com/cl-zhao/product-recommendations.git main 2>/dev/null
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 已推送到 GitHub"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === AI Builders Digest 执行完成 ==="
