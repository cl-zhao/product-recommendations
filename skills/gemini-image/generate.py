#!/usr/bin/env python3
"""
Gemini Image Generation Tool
Usage: python generate.py "your prompt" [output_path]
"""

import sys
import os
import json
import base64
from pathlib import Path

def load_api_key():
    """从 credentials.json 加载 Gemini API Key"""
    creds_path = Path(__file__).parent.parent.parent / "credentials.json"
    with open(creds_path) as f:
        creds = json.load(f)
    return creds["gemini"]["api_key"]

def generate_image(prompt: str, output_path: str = None) -> str:
    """
    调用 Gemini API 生成图片
    返回保存的文件路径
    """
    from google import genai
    from google.genai import types

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        )
    )

    # 确定输出路径
    if output_path is None:
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        # 用时间戳命名
        import time
        output_path = str(output_dir / f"image_{int(time.time())}.png")

    # 解析响应
    text_parts = []
    image_saved = False

    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text:
            text_parts.append(part.text)
        elif hasattr(part, "inline_data") and part.inline_data:
            # 保存图片
            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)
            image_saved = True

    result = {
        "image_path": output_path if image_saved else None,
        "text": "\n".join(text_parts) if text_parts else None,
        "success": image_saved
    }

    print(json.dumps(result, ensure_ascii=False))
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python generate.py "prompt" [output_path]')
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    generate_image(prompt, output)
