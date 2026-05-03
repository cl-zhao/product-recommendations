#!/usr/bin/env python3
"""
Google Gemini (Nano Banana) 图片生成工具
直接调用 Google Generative Language API

使用方法:
    python3 nanobanana.py "画一只可爱的黑猫" [--output image.png] [--model gemini-3.1-flash-preview-05-20]
"""

import os
import sys
import argparse
import json
import base64
import urllib.request
import urllib.error


# API 配置
API_KEY = "AIzaSyBjwd3ADcqgIqOMXkRLNtGyYJ9KHnxZ22A"
API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"


def generate_image(prompt: str, model: str = DEFAULT_MODEL, output_path: str = None) -> str:
    """
    调用 Google Gemini API 生成图片
    
    Args:
        prompt: 图片描述
        model: 模型名称
        output_path: 输出文件路径
    
    Returns:
        生成的图片文件路径
    """
    url = f"{API_BASE_URL}/models/{model}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"🎨 调用 Google Gemini (Nano Banana) 生成图片...")
    print(f"   Prompt: {prompt}")
    print(f"   Model: {model}")
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            # 检查是否有图片
            if "candidates" in result:
                candidate = result["candidates"][0]
                if "content" in candidate:
                    parts = candidate["content"]["parts"]
                    for part in parts:
                        if "inlineData" in part:
                            # 获取图片数据
                            mime_type = part["inlineData"]["mimeType"]
                            image_data = part["inlineData"]["data"]
                            
                            # 解码图片
                            img_bytes = base64.b64decode(image_data)
                            
                            # 确定输出路径
                            if output_path is None:
                                safe_name = "".join(c if c.isalnum() else "_" for c in prompt[:30])
                                output_path = f"nanobanana_{safe_name}.png"
                            
                            # 保存图片
                            with open(output_path, "wb") as f:
                                f.write(img_bytes)
                            
                            print(f"✅ 图片已保存: {output_path}")
                            print(f"   大小: {len(img_bytes)} bytes")
                            print(f"   格式: {mime_type}")
                            return output_path
                
                # 如果没有图片，可能有 text 回复
                if "content" in candidate:
                    parts = candidate["content"]["parts"]
                    for part in parts:
                        if "text" in part:
                            print(f"📝 模型回复: {part['text']}")
            
            # 检查错误
            if "error" in result:
                error = result["error"]
                print(f"❌ API Error: {error.get('message', 'Unknown error')}", file=sys.stderr)
                return None
            
            print("❌ 未找到生成的图片", file=sys.stderr)
            print(f"   Response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
            return None
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"❌ HTTP Error {e.code}: {error_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Google Gemini (Nano Banana) 图片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 基本用法
    python3 nanobanana.py "一只可爱的黑猫"
    
    # 指定输出文件
    python3 nanobanana.py "一幅中国山水画" --output landscape.png
    
    # 使用指定模型
    python3 nanobanana.py "未来城市" --model gemini-3.1-flash-preview-05-20
"""
    )
    
    parser.add_argument("prompt", help="图片描述文本")
    parser.add_argument("-o", "--output", default=None, help="输出文件路径")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help="模型名称")
    
    args = parser.parse_args()
    
    result = generate_image(args.prompt, args.model, args.output)
    
    if result:
        print(f"\n🎉 完成！图片: {result}")
        return 0
    else:
        print(f"\n❌ 生成失败", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
