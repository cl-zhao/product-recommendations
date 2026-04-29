# Gemini Image Generation Skill

使用 Google Gemini API 生成图片。

## API Key

存储于：`/root/.openclaw/workspace/credentials.json` → `gemini.api_key`

## 使用方法

### 快速调用（推荐）

```bash
cd /root/.openclaw/workspace/skills/gemini-image
python generate.py "你的提示词" [可选输出路径]
```

输出为 JSON：
```json
{"image_path": "/path/to/image.png", "text": "描述文字（可能为null）", "success": true}
```

### 在 Agent 中使用

1. 构造提示词（英文效果更好）
2. 执行脚本，解析 JSON 输出
3. 用 `message` 工具发送图片（`media` 参数传文件路径）

### 示例提示词

```
A cyberpunk black cat with glowing green circuit patterns, digital art style
A realistic photo of a black cat with neon blue eyes
```

## 模型

- **当前模型：** `gemini-2.5-flash-image`（即"香蕉模型" Nano Banana）
- **其他可用：** `gemini-2.0-flash-exp-image-generation`、`imagen-4.0-generate-001`

## 依赖

```bash
pip install google-genai
```

## 输出目录

默认输出到 `skills/gemini-image/output/`，可通过第二个参数指定路径。

## 注意

- 提示词英文效果更好
- 单次生成耗时约 5-15 秒
- 生成的图片为 PNG 格式
