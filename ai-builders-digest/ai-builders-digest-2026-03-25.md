# AI Builders Digest - 2026年03月25日

> 由 OpenClaw 自动生成 | 数据来源: Follow Builders Project | 中英对照版

---

## 📊 今日概览

- **Tweets**: 15 条更新
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

🔗 [查看原文](https://x.com/karpathy/status/2036487306585268612) | ❤️ 21171 | 🔁 4006

---

### 2. @swyx

**Swyx**

seriously @walden_yan cooked, this thing legitimately saves my ass 3-8x a day, and yes it sounds weird that devin can catch devin's own mistakes, but this is basically the equivalent of "sleeping on it" and looking at a PR with fresh/more critical eyes.  btw you should also see the "smart friend" pattern he piloted in Windsurf, it is going to be the design pattern for smarter subagents (usually subagents are dumber) that others are only just catching on to

🔗 [查看原文](https://x.com/swyx/status/2036565584515899445) | ❤️ 109 | 🔁 3

---

### 3. @swyx

**Swyx**

https://t.co/rBYwFF4t5s https://t.co/i4lxZSxVB0

🔗 [查看原文](https://x.com/swyx/status/2036540782925193336) | ❤️ 6 | 🔁 0

---

### 4. @swyx

**Swyx**

first casualty of OpenAI’s crackdown on Side Quests:

Sora is dead :( https://t.co/sfQhNu3IQ5

🔗 [查看原文](https://x.com/swyx/status/2036533647659143630) | ❤️ 122 | 🔁 1

---

### 5. @joshwoodward

**Josh Woodward**

I've been at @Google since I was an intern, and there's never been a more exciting time. The place is pulsating.

We're hiring :)

@GeminiApp or @GoogleAIStudio: https://t.co/otVHg9uuqo

@GoogleLabs: https://t.co/e7zA6GJYDe https://t.co/9J4UFJyWPy

🔗 [查看原文](https://x.com/joshwoodward/status/2036513009661780291) | ❤️ 1483 | 🔁 103

---

### 6. @petergyang

**Peter Yang**

Nooo they can't talk to each other? Come on @telegram https://t.co/47t4ZjGCgw

🔗 [查看原文](https://x.com/petergyang/status/2036669221363761456) | ❤️ 1 | 🔁 0

---

### 7. @petergyang

**Peter Yang**

My Telegram is just chats with my OpenClaw and now Claude bots. Haven't talked to a single human yet.

🔗 [查看原文](https://x.com/petergyang/status/2036664048700600706) | ❤️ 25 | 🔁 3

---

### 8. @petergyang

**Peter Yang**

I hope AI agents will help us all stop obsessing about:

- Specs
- Designs
- Issues
- Roadmaps
- Strategy docs
- Spreadsheets

and instead let us all obsess about improving the end user product and rapid iteration loops with users.

Product development is much more fun that way. https://t.co/vGcLnCTJOn

🔗 [查看原文](https://x.com/petergyang/status/2036621615086309468) | ❤️ 71 | 🔁 6

---

### 9. @thenanyu

**Nan Yu**

My incentives were to get this agent thing to work so I didn’t have to do annoying work anymore!

https://t.co/vI6hR0CVvq

🔗 [查看原文](https://x.com/thenanyu/status/2036631571118084476) | ❤️ 2 | 🔁 0

---

### 10. @thenanyu

**Nan Yu**

Gemini always getting wrecked in these screenshots https://t.co/SjzUe148WU

🔗 [查看原文](https://x.com/thenanyu/status/2036619356730204395) | ❤️ 5 | 🔁 0

---

### 11. @thenanyu

**Nan Yu**

I haven’t written a PRD by hand, filed an issue through a form, or hand-written any code in months. 

But the volume of work I’m producing and the quality bar have never been higher. https://t.co/dSyyn7yzwg

🔗 [查看原文](https://x.com/thenanyu/status/2036549647267709110) | ❤️ 266 | 🔁 11

---

### 12. @_catwu

**Cat Wu**

Excited to see everyone at Code with Claude! What would you like to hear from us at this year's sessions? https://t.co/RxWLfs4kFo

🔗 [查看原文](https://x.com/_catwu/status/2036594646370210229) | ❤️ 211 | 🔁 10

---

### 13. @trq212

**Thariq**

only available on Teams right now, but working on scaling it https://t.co/YlJU3OKrew

🔗 [查看原文](https://x.com/trq212/status/2036515949617037711) | ❤️ 46 | 🔁 0

---

### 14. @trq212

**Thariq**

turns out being an AI safety company is useful for when you need to make sure AIs can run safely https://t.co/DjJZjPrZn4

🔗 [查看原文](https://x.com/trq212/status/2036513038983995820) | ❤️ 1180 | 🔁 35

---

### 15. @trq212

**Thariq**

I’ll be covering how to make the most of this in my livestream on March 31st with Figma! 

You can sign up here: https://t.co/G32hMTFUR4 https://t.co/9owzK6bjWF

🔗 [查看原文](https://x.com/trq212/status/2036442894777594248) | ❤️ 190 | 🔁 10

---



## 🎙️ Podcasts 更新

### 1. 🔬There Is No AlphaFold for Materials — AI for Materials Discovery with Heather Kulik

**频道**: Unknown
**链接**: https://youtube.com/watch?v=KSCCKCz2x04

---


---

## 📚 相关资源

- **Follow Builders Project**: https://github.com/zarazhangrui/follow-builders
- **数据更新频率**: Tweets 每 6 小时, Podcasts 每 24 小时

---

*文档生成时间: 2026-03-25 17:16:17*
*由 OpenClaw AI Builders Digest 自动生成 | 中英对照版*
