# AI Builders Digest - 2026年03月25日 17:20

> 由 OpenClaw 自动生成 | 数据来源: Follow Builders Project | 中英对照版

---

## 📊 今日概览

- **Tweets**: 15 条精选翻译
- **格式**: 中英对照

---

## 🐦 AI Builders 最新动态

### 1. @karpathy
**Andrej Karpathy**

Software horror: litellm PyPI supply chain attack. 

Simple `pip install litellm` was enough to exfiltrate SSH keys, AWS/GCP/Azure creds, Kubernetes configs, git credentials, env vars (all your API keys), shell history, crypto wallets, SSL private keys, CI/CD secrets, database passwords.

LiteLLM itself has 97 million downloads per month which is already terrible, but much worse, the contagion spreads to any project that depends on litellm. For example, if you did `pip install dspy` (which depended on litellm>=1.64.0), you'd also be pwnd. Same for any other large project that depended on litellm.

Afaict the poisoned version was up for only less than ~1 hour. The attack had a bug which led to its discovery - Callum McMahon was using an MCP plugin inside Cursor that pulled in litellm as a transitive dependency. When litellm 1.82.8 installed, their machine ran out of RAM and crashed. So if the attacker didn't vibe code this attack it could have been undetected for many days or weeks.

Supply chain attacks like this are basically the scariest thing imaginable in modern software. Every time you install any depedency you could be pulling in a poisoned package anywhere deep inside its entire depedency tree. This is especially risky with large projects that might have lots and lots of dependencies. The credentials that do get stolen in each attack can then be used to take over more accounts and compromise more packages.

Classical software engineering would have you believe that dependencies are good (we're building pyramids from bricks), but imo this has to be re-evaluated, and it's why I've been so growingly averse to them, preferring to use LLMs to "yoink" functionality when it's simple enough and possible.

软件界的恐怖故事：litellm PyPI 供应链攻击。

只需要简单的 `pip install litellm` 就足以窃取 SSH keys、AWS/GCP/Azure 凭证、Kubernetes 配置、git 凭证、env vars（你所有的 API keys）、shell 历史记录、加密货币钱包、SSL 私钥、CI/CD 机密、数据库密码。

LiteLLM 本身每月就有 9700 万次下载，这已经很糟糕了，但更糟的是，这种污染会传播到任何依赖 litellm 的项目。例如，如果你执行了 `pip install dspy`（它依赖 litellm>=1.64.0），你也会被攻破（pwnd）。任何依赖 litellm 的大型项目都一样。

据我所知（Afaict），被投毒的版本上线不到 1 小时。这次攻击有一个 bug 导致了它的发现——Callum McMahon 在 Cursor 中使用了一个 MCP plugin，该插件将 litellm 作为传递依赖（transitive dependency）引入。当安装 litellm 1.82.8 时，他的机器 RAM 耗尽并崩溃了。所以如果攻击者不是这么随意地（vibe code）编写这次攻击，它可能很多天甚至几周都不会被发现。

像这样的供应链攻击基本上是现代软件中能想象到的最可怕的事情。每次你安装任何依赖时，都可能在其整个依赖树深处的某个地方引入被投毒的包。这对于可能拥有大量依赖的大型项目来说尤其危险。每次攻击中窃取的凭证随后可以用来接管更多账户并破坏更多包。

传统的软件工程会让你相信依赖是好的（我们是用砖块建造金字塔），但在我看来，这需要重新评估。这也是为什么我越来越排斥依赖，更倾向于在简单且可行的情况下，使用 LLMs 直接“抓取”（yoink）功能。

🔗 原文链接 | ❤️ 21171 | 🔁 4006

### 2. @swyx
**Swyx**

seriously @walden_yan cooked, this thing legitimately saves my ass 3-8x a day, and yes it sounds weird that devin can catch devin's own mistakes, but this is basically the equivalent of "sleeping on it" and looking at a PR with fresh/more critical eyes.  btw you should also see the "smart friend" pattern he piloted in Windsurf, it is going to be the design pattern for smarter subagents (usually subagents are dumber) that others are only just catching on to

说真的，@walden_yan 做得太牛了（cooked），这东西每天实实在在地救了我 3-8 次大忙。是的，听起来很奇怪，Devin 能捕捉 Devin 自己的错误，但这基本上等同于“睡一觉冷静一下”，然后用更新鲜、更批判性的眼光去查看 PR。

顺便说一句，你还应该看看他在 Windsurf 中试点的 "smart friend" 模式，这将成为更聪明的子 Agent（subagents）的设计模式（通常子 Agent 比较笨），而其他人才刚刚开始意识到这一点。

🔗 原文链接 | ❤️ 109 | 🔁 3

### 3. @swyx
**Swyx**

first casualty of OpenAI's crackdown on Side Quests:

Sora is dead :( 

OpenAI 打击 Side Quests 的首个牺牲品：

Sora 死了 :(

🔗 原文链接 | ❤️ 122 | 🔁 1

### 4. @joshwoodward
**Josh Woodward**

I've been at @Google since I was an intern, and there's never been a more exciting time. The place is pulsating.

We're hiring :)

@GeminiApp or @GoogleAIStudio: [link]

@GoogleLabs: [link] [link]

我从实习生时期就在 @Google 工作，从来没有像现在这样令人兴奋的时刻。这里充满了活力。

我们正在招聘 :)

@GeminiApp 或 @GoogleAIStudio: [链接]

@GoogleLabs: [链接] [链接]

🔗 原文链接 | ❤️ 1483 | 🔁 103

### 5. @petergyang
**Peter Yang**

Noo they can't talk to each other? Come on @telegram 

不是吧，它们不能互相对话？拜托 @telegram 

🔗 原文链接 | ❤️ 1 | 🔁 0

### 6. @petergyang
**Peter Yang**

My Telegram is just chats with my OpenClaw and now Claude bots. Haven't talked to a single human yet.

我的 Telegram 里全是和我的 OpenClaw 以及现在的 Claude bots 聊天。还没跟任何一个真人说过话。

🔗 原文链接 | ❤️ 25 | 🔁 3

### 7. @petergyang
**Peter Yang**

I hope AI agents will help us all stop obsessing about:

- Specs
- Designs
- Issues
- Roadmaps
- Strategy docs
- Spreadsheets

and instead let us all obsess about improving the end user product and rapid iteration loops with users.

Product development is much more fun that way. 

我希望 AI agents 能帮助我们所有人停止过度纠结于：

- Specs
- Designs
- Issues
- Roadmaps
- Strategy docs
- Spreadsheets

而是让我们都专注于改进终端用户产品以及与用户的快速迭代循环（rapid iteration loops）。

产品开发这样才会更有趣。

🔗 原文链接 | ❤️ 71 | 🔁 6

### 8. @thenanyu
**Nan Yu**

My incentives were to get this agent thing to work so I didn't have to do annoying work anymore!

我的动力就是让这个 agent 东西跑起来，这样我就不用再做那些烦人的工作了！

🔗 原文链接 | ❤️ 2 | 🔁 0

### 9. @thenanyu
**Nan Yu**

Gemini always getting wrecked in these screenshots 

在这些截图里 Gemini 总是被完爆 

🔗 原文链接 | ❤️ 5 | 🔁 0

### 10. @thenanyu
**Nan Yu**

I haven't written a PRD by hand, filed an issue through a form, or hand-written any code in months. 

But the volume of work I'm producing and the quality bar have never been higher. 

我已经几个月没有手写 PRD 了，没有通过表单提交过 issue，也没有手写任何代码。

但我产出的工作量和质量标准（quality bar）从未如此之高。

🔗 原文链接 | ❤️ 266 | 🔁 11

### 11. @_catwu
**Cat Wu**

Excited to see everyone at Code with Claude! What would you like to hear from us at this year's sessions? 

很高兴在 Code with Claude 见到大家！在今年的环节（sessions）中，你们想听我们分享什么？

🔗 原文链接 | ❤️ 211 | 🔁 10

### 12. @trq212
**Thariq**

only available on Teams right now, but working on scaling it 

目前仅在 Teams 上可用，但我们正在努力扩大范围 

🔗 原文链接 | ❤️ 46 | 🔁 0

### 13. @trq212
**Thariq**

turns out being an AI safety company is useful for when you need to make sure AIs can run safely 

事实证明，当你需要确保 AIs 能够安全运行时，成为一家 AI 安全公司还是很有用的 

🔗 原文链接 | ❤️ 1180 | 🔁 35

### 14. @trq212
**Thariq**

I'll be covering how to make the most of this in my livestream on March 31st with Figma! 

You can sign up here: [link] [link]

我将在 3 月 31 日与 Figma 合作的直播中讲解如何充分利用这一点！

你可以在此报名：[链接] [链接]

🔗 原文链接 | ❤️ 190 | 🔁 10

---

## 📚 相关资源

- **Follow Builders Project**: https://github.com/zarazhangrui/follow-builders
- **数据更新频率**: Tweets 每 6 小时

---

*文档生成时间: 2026-03-25 17:20:27*
*由 OpenClaw AI Builders Digest 自动生成 | 中英对照版*
