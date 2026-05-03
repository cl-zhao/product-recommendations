# Scrapling Quick Reference

## 安装

```bash
pip install scrapling
pip install scrapling[dynamic]    # 动态渲染
pip install scrapling[stealth]     # 隐秘请求
pip install scrapling[all]         # 全部
```

## Fetcher 类型选择

| 类型 | 使用场景 |
|------|----------|
| `Fetcher` | 简单 HTTP 请求，快速静态页面 |
| `AsyncFetcher` | 需要并发请求时 |
| `StealthyFetcher` | 有反爬（Cloudflare 等）|
| `DynamicFetcher` | JS 动态加载内容 |

## 基础用法

### 简单 HTTP 请求
```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')
titles = page.css('h1::text').getall()
```

### 带 Session 的请求（维持 Cookie）
```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate='chrome') as session:
    page = session.get('https://example.com')
    data = page.css('.item::text').getall()
```

### 隐秘请求（绕过 Cloudflare）
```python
from scrapling.fetchers import StealthyFetcher, StealthySession

# 一次性请求
page = StealthyFetcher.fetch('https://cf-protected.com', headless=True, solve_cloudflare=True)
data = page.css('#content a::text').getall()

# 或保持 Session
with StealthySession(headless=True, solve_cloudflare=True) as session:
    page = session.fetch('https://cf-protected.com')
```

### 动态内容（JavaScript 渲染）
```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

# 一次性请求
page = DynamicFetcher.fetch('https://spa.example.com', headless=True, network_idle=True)
data = page.css('.product::text').getall()

# 保持 Session
with DynamicSession(headless=True, network_idle=True) as session:
    page = session.fetch('https://spa.example.com')
```

## 选择器语法

### CSS 选择器
```python
page.css('.class #id')           # 类和 ID
page.css('h1::text')            # 文本内容
page.css('a::attr(href)')        # 属性值
page.css('.item:has(.child)')   # 包含特定子元素
```

### XPath 选择器
```python
page.xpath('//div[@class="item"]')
page.xpath('//span/text()')
```

### 自适应选择器（网站改版后仍有效）
```python
# 首次抓取时保存选择器
products = page.css('.product', auto_save=True)

# 后续抓取时自动适应变化
products = page.css('.product', adaptive=True)
```

## Spider 框架

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com/"]
    concurrent_requests = 10  # 并发数
    
    async def parse(self, response: Response):
        # 提取数据
        for item in response.css('.item'):
            yield {
                'title': item.css('h2::text').get(),
                'link': item.css('a::attr(href)').get(),
            }
        
        # 翻页
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0])

# 启动爬虫
result = MySpider().start()
result.items.to_json('output.json')
```

### 多 Session 类型混合
```python
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class MultiSpider(Spider):
    name = "multi_session"
    start_urls = ["https://example.com/"]
    
    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
    
    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            if "protected" in link:
                yield Request(link, sid="stealth")  # 受保护页面用 stealth
            else:
                yield Request(link, sid="fast", callback=self.parse)
```

## 暂停/恢复

```python
# Ctrl+C 优雅关闭，自动保存进度
# 重启时自动从上次停止的地方继续
result = MySpider().start()
```

## Streaming 模式

```python
# 实时获取数据
for item in MySpider().stream():
    print(item)
```

## Proxy 轮换

```python
from scrapling.fetchers import FetcherSession
from scrapling.proxies import ProxyRotator

rotator = ProxyRotator(['http://proxy1:8080', 'http://proxy2:8080'])

with FetcherSession(proxy_rotator=rotator) as session:
    page = session.get('https://example.com')
```

## 导出数据

```python
result = MySpider().start()

result.items.to_json('data.json')
result.items.to_jsonl('data.jsonl')

# 或使用管道
result.items.to_csv('data.csv', columns=['title', 'link'])
```

## 常用选项

### Fetcher 选项
- `headless=True` - 无头模式（浏览器）
- `network_idle=True` - 等待网络空闲
- `solve_cloudflare=True` - 解决 Cloudflare 验证
- `impersonate='chrome'` - 模拟 Chrome 指纹
- `stealthy_headers=True` - 隐秘 headers

### 选择器选项
- `auto_save=True` - 保存选择器映射
- `adaptive=True` - 自适应网站变化
- `first=True` - 只返回第一个

## 错误处理

```python
try:
    page = StealthyFetcher.fetch(url, headless=True)
except Exception as e:
    print(f"请求失败: {e}")
```

## MCP Server (AI 集成)

Scrapling 内置 MCP 服务，支持 Claude 等 AI 辅助抓取：

```bash
scrapling mcp --help
```

详见: https://scrapling.readthedocs.io/en/latest/ai/mcp-server.html
