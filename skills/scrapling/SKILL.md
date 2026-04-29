---
name: scrapling
description: |
  自适应 Web Scraping 框架，专为现代网页爬取设计。当用户需要以下场景时使用：
  (1) 爬取有反爬机制的网站（Cloudflare、Turnstile 等）
  (2) 爬取 JavaScript 动态渲染的页面
  (3) 网站结构经常变化，需要自适应解析
  (4) 需要大规模并发爬取（Spider 框架）
  (5) 需要维持登录状态（Session 管理）
  (6) 需要 Proxy 轮换
  (7) 快速简单的单页面爬取
  (8) 想用 AI 辅助数据提取（MCP）
  
  不要在简单的静态页面爬取上过度使用 StealthyFetcher，用 Fetcher 即可。
---

# Scrapling Web Scraping Skill

## 快速开始

### 安装
```bash
pip install scrapling              # 基础
pip install scrapling[stealth]    # 隐秘请求
pip install scrapling[dynamic]    # 动态渲染
pip install scrapling[all]        # 全部
```

### 选择 Fetcher 类型

| 场景 | 推荐 | 导入 |
|------|------|------|
| 简单静态页面 | `Fetcher` | `from scrapling.fetchers import Fetcher` |
| 需并发/异步 | `AsyncFetcher` | `from scrapling.fetchers import AsyncFetcher` |
| 有反爬保护 | `StealthyFetcher` | `from scrapling.fetchers import StealthyFetcher` |
| JS 动态内容 | `DynamicFetcher` | `from scrapling.fetchers import DynamicFetcher` |

## 基础模式

### 一次性请求
```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')
data = page.css('.item::text').getall()
```

### 带 Session（维持 Cookie）
```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate='chrome') as session:
    page = session.get('https://example.com/login')
    # Cookie 会自动维持
```

### 隐秘请求（Cloudflare 等）
```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://cf-protected.com',
    headless=True,
    solve_cloudflare=True
)
```

### 动态内容（JS 渲染）
```python
from scrapling.fetchers import DynamicFetcher

page = DynamicFetcher.fetch(
    'https://spa.example.com',
    headless=True,
    network_idle=True
)
```

## 自适应解析（网站改版后仍有效）

```python
# 首次抓取，保存元素映射
products = page.css('.product', auto_save=True)

# 后续抓取，启用自适应
products = page.css('.product', adaptive=True)
# 即使网站结构改变，也能找到目标元素
```

## Spider 框架（大规模爬取）

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com/"]
    concurrent_requests = 10
    
    async def parse(self, response: Response):
        for item in response.css('.item'):
            yield {
                'title': item.css('h2::text').get(),
                'price': item.css('.price::text').get(),
            }
        
        # 翻页
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0])

result = MySpider().start()
result.items.to_json('output.json')
```

**特性**：
- 并发请求 + 域名限流
- 暂停/恢复（Ctrl+C 后重启继续）
- Streaming 模式实时输出
- 多 Session 类型混合

## 选择器参考

```python
# CSS
page.css('.class #id')           # 组合选择器
page.css('h1::text')             # 获取文本
page.css('a::attr(href)')        # 获取属性
page.css('.item:has(a)')         # 包含子元素

# XPath
page.xpath('//div[@class="item"]')
page.xpath('//text()')

# 自适应（网站改版后仍有效）
page.css('.product', adaptive=True)
```

## 详细参考

查看 `references/quick-reference.md` 获取：
- 多 Session 类型混合配置
- Proxy 轮换设置
- 完整 Spider 示例
- Streaming 模式用法
- 数据导出方法
- MCP/AI 集成说明

## 常见问题

**Q: Cloudflare 一直失败？**
A: 使用 `StealthyFetcher` + `headless=True` + `solve_cloudflare=True`

**Q: 网站结构变了数据抓不到？**
A: 使用 `adaptive=True` 参数启用自适应解析

**Q: 需要登录后抓取？**
A: 使用 `FetcherSession` 或 `StealthySession`，先发送登录请求建立 Session

**Q: 页面是 JS 渲染的？**
A: 使用 `DynamicFetcher` 替代普通 Fetcher

**Q: 爬虫被封 IP？**
A: 使用 `ProxyRotator` 配置代理轮换
