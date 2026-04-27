#!/usr/bin/env python3
"""Translate AI Builders Digest to bilingual format"""

import re

def translate_tweet(en_text):
    """Translate tweet text to Chinese - conversational style"""
    translations = {
        "Most Al chatbots give you basic \"projects.\" Gemini just built you a second brain. 🧠": "大多数 AI 聊天机器人只给你基本的「项目」。Gemini 直接给你造了个第二大脑。🧠",
        "Introducing Notebooks: some of the magic from @NotebookLM, integrated directly into @GeminiApp.": "发布 Notebooks：@NotebookLM 的部分魔法功能，直接整合进了 @GeminiApp。",
        "Here's what changes for you today:": "今天的改变如下：",
        "📚 Upload 100 sources for free": "📚 免费上传 100 个资料源",
        "📂 Organize your chats - the wait is officially over :)": "📂 组织整理你的聊天——终于不用等了 :)",
        "🔄 Sources, chats, and emojis sync": "🔄 资料源、聊天和表情全部同步",
        "People are using Gemini and NotebookLM in tandem, and we'll keep building both.": "大家都在 Gemini 和 NotebookLM 之间配合着用，两个产品我们都会继续做下去。",
        "To manage capacity, we're rolling this out NOW on the web and going from Ultra ➡️ Pro ➡️ Plus ➡️ Free. (Mobile, EU, and Workspace are up next!)": "为了控制容量，我们现在先从网页端开始推送，逐步开放顺序是 Ultra ➡️ Pro ➡️ Plus ➡️ Free。（移动端、欧盟和 Workspace 随后跟上！）",
        "With Google I/O right around the corner, we are just getting started. Enjoy!": "Google I/O 近在眼前，一切才刚开始。Enjoy！",
        "Five Erdos problems at once! The proofs are getting more elegant as the models improve 👀": "一次性解决五个 Erdős 问题！随着模型能力提升，证明过程也越来越优雅了 👀",
        "Titles don't matter": "Title 不重要",
        "Support my friend Aadit's new company - great name btw :)": "支持一下我朋友 Aadit 的新公司——名字很酷 :)",
        "As much as I love using Claude Max and ChatGPT Pro, I don't think these all-you-can-use AI subscriptions will last forever.": "虽然我超爱用 Claude Max 和 ChatGPT Pro，但我不觉得这种「无限畅用」的 AI 订阅能一直持续下去。",
        "Here's my new deep dive that covers:": "这是我的新深度分析，涵盖了：",
        "→ Why Anthropic cut off OpenClaw access": "→ Anthropic 为什么断了 OpenClaw 的访问权限",
        "→ How to run local models on your Mac": "→ 如何在 Mac 上运行本地模型",
        "→ What I'm seeing on the ground in China": "→ 我在中国实地看到了什么",
        "📌 Read now:": "📌 立即阅读：",
        "would like to start with people I know already so we can get over initial awkwardness!": "想从我认识的人开始，这样能一起跨过最初的尴尬期！",
        "I want to do some streams where I work with non-technical people using Claude Code to figure out how they might be able to improve their process.": "我想做几场直播，和非技术人员一起用 Claude Code，帮他们看看有哪些地方可以提升效率。",
        "My feeling is that just a few tips could make a big difference in efficiency. Any mutuals interested?": "我觉得就几个小技巧就能让效率大幅提升。有没有人感兴趣？",
        "The docs are a gold mine, read more here:": "官方文档就是金矿，更多内容在这里：",
        "There's a reason bootstrapped solo businesses are accelerating on Replit… we gave builders entire teams.": "在 Replit 上，自力更生的个人业务正在加速增长……因为我们给开发者配备了整支团队。",
        "🔥": "🔥",
        "AI Gateway is quite literally a \"peace of mind\" product:": "AI Gateway 简直就是一款「安心」产品：",
        "✅ No downtime": "✅ 无停机",
        "✅ No lock-in": "✅ 不被绑定",
        "✅ No keys": "✅ 不需要 API Key",
        "🆕 No training": "🆕 不用于训练",
        "The best outcome for humanity is many strong AIs competing for the top spot.": "对人类来说，最好的结果是多个强 AI 共同竞争榜首。",
        "Vercel is proudly powering and the infrastructure that made today's model release possible.": "Vercel 很荣幸为和使今天模型发布成为可能的基础设施提供支持。",
        "The web's brightest days are ahead.": "网络的黄金时代还在前面。",
        "1️⃣ The web is AI's natural medium. LLMs are proficient in web tech. The browser is now everyone's IDE. No 'App Store' bs.": "1️⃣ 网络是 AI 的天然媒介。大语言模型精通 Web 技术。浏览器现在就是每个人的 IDE。没有「App Store」那些破事。",
        "2️⃣ As we approach coding superintelligence, powerful low-level web APIs are maturing: WebGPU, HTML in Canvas, WebAssembly. The performance ceiling of the web will vanish, and you'll witness the most impressive, whimsical, and multi-dimensional pages and apps.": "2️⃣ 当我们接近编程超级智能时，强大的底层 Web API 也正在成熟：WebGPU、Canvas 内嵌 HTML、WebAssembly。Web 的性能天花板即将消失，你将见证史上最惊艳、最天马行空、最多维的页面和应用。",
        "3️⃣ Generative UI is AI's final form. The web will be the birthplace of \"AGUI\". Each hyperlink providing a just-in-time, beautifully personalized experience.": "3️⃣ 生成式 UI 是 AI 的终极形态。网络将成为「AGUI」的诞生地。每一条超链接都将提供即时、精美、个性化的体验。",
        "If you bet on the web, you bet on the right horse.": "如果你赌网络，你押对了。",
        "I've found Managed Agents to somehow be both the fastest way to hack together a weekend agent project and the most robust way to ship one to millions of users.": "我发现 Managed Agents 既是最快搞定周末 Agent 项目的方式，也是向百万用户稳健交付的最佳方案。",
        "It eliminates all the complexity of self-hosting an agent but still allows a great degree of flexibility with setting up your harness, tools, skills, etc.": "它省去了自托管 Agent 的所有复杂性，但同时仍保留了大量自由度，可以自定义 harness、工具、skills 等。",
        "Background agents for knowledge work are here. You can use the Box API or MCP to automate any content workflow with Box + Claude Managed Agents. In 2 minutes you can be automating document review processes, data extraction, or connecting content to other IT systems. Crazy times.": "知识工作的后台 Agent 已经来了。你可以用 Box API 或 MCP，通过 Box + Claude Managed Agents 自动化任何内容工作流。2 分钟就能开始自动化文档审查、数据提取，或将内容连接到其他 IT 系统。这时代太疯狂了。",
        "If you're taking advice from 1x speed engineers I don't know what to tell you": "如果你在听 1 倍速工程师的建议，我不知道该说什么好",
        "Don't believe the haters. Speed up with us.": "别听那些唱衰的人。跟我们一起加速吧。",
        "Legit baller": "真牛批",
        "The cool thing about markdown is that the agent itself can decide when a GStack skill will help you": "markdown 很酷的一点是，agent 自己就能决定什么时候 GStack skill 能帮到你",
        "Just make stuff as you might and it'll trigger as needed": "尽管按你的想法去创作，需要时它就会触发",
        "Repo here - fully vibe coded using Opus 4.5:": "代码仓库在此——全程用 Opus 4.5 vibe coded：",
        "Also props to for helping sync X bookmarks, for Substack2Markdown and for writing File over App three years ago!": "同时感谢帮忙同步 X 书签，做的 Substack2Markdown，以及三年前写的 File over App！",
        "Inspired by & , introducing LLMwiki.. fully open source to help build yours.": "受和的启发，发布 LLMwiki.. 完全开源，帮助你构建自己的。",
        "Inputs were tweets, bookmarks, iMessage/WhatsApp, and all my writing.": "输入内容包括推文、书签、iMessage/WhatsApp 和我所有的文字内容。",
        "Spent a bunch of time refining the frontend design to make it look great.": "花了很多时间打磨前端设计，让它看起来很棒。",
        "Even though every single article here was written by AI, it was able to make surprisingly sharp connections.": "虽然这里的每一篇文章都是 AI 写的，但它能做出惊人精准的关联。",
        "To make yours, just give the repo to Claude Code and it'll guide you!": "想建你自己的，只需要把代码仓库丢给 Claude Code，它会引导你！",
    }
    return translations.get(en_text, None)

def main():
    input_file = "/root/.openclaw/workspace/bin/output/ai-builders-digest-en-2026-04-09.md"
    output_file = "/root/.openclaw/workspace/product-recommendations/ai-builders-digest/ai-builders-digest-2026-04-09.md"
    
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split("\n")
    result_lines = []
    i = 0
    in_tweet_block = False
    tweet_texts = []
    
    while i < len(lines):
        line = lines[i]
        
        # Keep headers and structural elements as-is
        if line.startswith("# AI Builders Digest"):
            result_lines.append(line)
            i += 1
            continue
        if line.startswith("> Auto-generated"):
            result_lines.append(line)
            i += 1
            continue
        if line == "---" and i < 3:
            result_lines.append(line)
            i += 1
            continue
        if line.startswith("## 📊"):
            result_lines.append(line)
            i += 1
            continue
        if line.startswith("- **Tweets**") or line.startswith("- **Podcasts"):
            result_lines.append(line)
            i += 1
            continue
        if line.startswith("## 🐦"):
            result_lines.append(line)
            i += 1
            continue
        if line.startswith("## 🎙️"):
            result_lines.append(line)
            i += 1
            continue
        if line.startswith("## 📚"):
            result_lines.append(line)
            i += 1
            continue
        if line.startswith("*Generated"):
            result_lines.append(line)
            i += 1
            continue
        if line.startswith("*By Open"):
            result_lines.append(line)
            i += 1
            continue
        
        # Tweet block starts with ###
        if line.startswith("### "):
            # Flush previous tweet texts if any
            if tweet_texts:
                result_lines.extend(tweet_texts)
                tweet_texts = []
            result_lines.append(line)
            i += 1
            continue
        
        # Handle tweet content lines
        if line.startswith("**") and "·" in line:
            # Author line
            if tweet_texts:
                result_lines.extend(tweet_texts)
                tweet_texts = []
            result_lines.append(line)
            i += 1
            continue
        
        if line.startswith("🔗 [View Original]"):
            result_lines.append(line)
            i += 1
            continue
        
        if line.startswith("❤️") or line.startswith("🔗 [") or line.startswith("📌"):
            result_lines.append(line)
            i += 1
            continue
        
        # Empty line
        if line.strip() == "":
            if tweet_texts:
                result_lines.extend(tweet_texts)
                tweet_texts = []
            result_lines.append(line)
            i += 1
            continue
        
        if line.startswith("---"):
            result_lines.append(line)
            i += 1
            continue
        
        # Text content that needs translation
        stripped = line.strip()
        if stripped and not stripped.startswith("**") and not stripped.startswith("📚") and not stripped.startswith("📂") and not stripped.startswith("🔄") and not stripped.startswith("📌") and not stripped.startswith("→") and not stripped.startswith("🔗") and not stripped.startswith("❤️") and not stripped.startswith("🔁") and not stripped.startswith("✅") and not stripped.startswith("🆕") and not stripped.startswith("1️⃣") and not stripped.startswith("2️⃣") and not stripped.startswith("3️⃣") and not stripped.startswith("🔥") and not stripped.startswith("http") and not stripped.startswith("ok ") and not stripped.startswith("Support") and not stripped.startswith("Repo here") and not stripped.startswith("Also props") and not stripped.startswith("Inspired") and not stripped.startswith("Inputs") and not stripped.startswith("Spent") and not stripped.startswith("Even though") and not stripped.startswith("To make"):
            # Try to translate
            trans = translate_tweet(stripped)
            if trans:
                tweet_texts.append(stripped)
                tweet_texts.append(trans)
            else:
                tweet_texts.append(stripped)
        else:
            tweet_texts.append(stripped)
    
    if tweet_texts:
        result_lines.extend(tweet_texts)
    
    output = "\n".join(result_lines)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"Written to {output_file}")

if __name__ == "__main__":
    main()
