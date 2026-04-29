#!/usr/bin/env python3
"""Convert the Doubao AI tutorial markdown to a nicely formatted HTML file."""

import markdown
import re

with open("/root/.openclaw/workspace/ai-usage-tutorial-doubao.md", "r", encoding="utf-8") as f:
    content = f.read()

# Convert markdown to HTML
html_body = markdown.markdown(
    content,
    extensions=[
        'tables',
        'fenced_code',
        'codehilite',
        'nl2br',
        'sane_lists',
    ]
)

# Wrap with full HTML document with CJK font support
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>豆包AI零基础完全教程</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap');
    
    * {{
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Noto Sans SC', 'Noto Sans CJK SC', 'Source Han Sans SC', 
                     'Microsoft YaHei', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
        font-size: 14px;
        line-height: 1.8;
        color: #333;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 30px;
        background: #fff;
    }}
    
    h1 {{
        font-size: 26px;
        color: #1a1a2e;
        border-bottom: 3px solid #1a1a2e;
        padding-bottom: 10px;
        margin-top: 40px;
    }}
    
    h1:first-of-type {{
        font-size: 32px;
        text-align: center;
        border-bottom: none;
        margin-top: 20px;
    }}
    
    h2 {{
        font-size: 20px;
        color: #16213e;
        border-left: 4px solid #16213e;
        padding-left: 12px;
        margin-top: 30px;
    }}
    
    h3 {{
        font-size: 16px;
        color: #0f3460;
        margin-top: 20px;
    }}
    
    p {{
        margin: 8px 0;
        text-align: justify;
    }}
    
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 12px 0;
        font-size: 13px;
    }}
    
    th {{
        background: #1a1a2e;
        color: white;
        padding: 10px 12px;
        text-align: left;
    }}
    
    td {{
        padding: 8px 12px;
        border: 1px solid #ddd;
    }}
    
    tr:nth-child(even) {{
        background: #f9f9f9;
    }}
    
    tr:hover {{
        background: #eef3ff;
    }}
    
    code {{
        background: #f5f5f5;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 12px;
    }}
    
    pre {{
        background: #f5f5f5;
        padding: 12px;
        border-radius: 5px;
        overflow-x: auto;
        font-size: 12px;
        line-height: 1.5;
        border-left: 4px solid #1a1a2e;
    }}
    
    pre code {{
        background: none;
        padding: 0;
    }}
    
    blockquote {{
        border-left: 4px solid #0f3460;
        margin: 10px 0;
        padding: 8px 16px;
        color: #555;
        font-style: italic;
        background: #f9f9f9;
    }}
    
    ul, ol {{
        padding-left: 24px;
    }}
    
    li {{
        margin: 4px 0;
    }}
    
    hr {{
        border: none;
        border-top: 1px solid #ddd;
        margin: 20px 0;
    }}
    
    strong {{
        color: #1a1a2e;
    }}
    
    /* Print styles */
    @media print {{
        body {{
            padding: 20px;
            font-size: 12px;
        }}
        
        h1 {{
            font-size: 22px;
            page-break-before: auto;
        }}
        
        h2 {{
            font-size: 17px;
        }}
        
        h3 {{
            font-size: 14px;
        }}
        
        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        table {{
            font-size: 11px;
        }}
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

output_path = "/root/.openclaw/workspace/ai-usage-tutorial-doubao.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML saved: {output_path}")
print(f"Size: {len(html)} bytes")
