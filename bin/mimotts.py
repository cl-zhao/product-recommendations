#!/usr/bin/env python3
"""
小米 MiMo TTS 语音合成工具
支持林黛玉（林妹妹）风格语音生成

使用方法:
    python3 mimotts.py "要说话的文本" [--output output.wav] [--style 风格]
    
林黛玉风格示例:
    python3 mimotts.py "宝哥哥，你可来了！" --style lin-daiyu
    
    python3 mimotts.py "人家心里头有好多话想跟你说呢……" --style lin-daiyu
"""

import os
import sys
import base64
import argparse
import numpy as np
import subprocess
from pathlib import Path

# API 配置
API_KEY = os.environ.get("MIMO_API_KEY", "sk-ckfspgxo23taeiyt838z0jyknntagwevdpuz0g8cj4nsogmu")
API_BASE_URL = "https://api.xiaomimimo.com/v1"
MODEL = "mimo-v2-tts"

# 林黛玉风格词汇和语气
LIN_DAIYU_STYLE_WORDS = [
    "宝哥哥", "林妹妹", "人家", "这般", "怎生", "可是", "偏生", 
    "痴了", "恼了", "落了", "散了", "瘦了", "哭了", "笑了",
    "罢罢", "也好", "罢了", "何苦", "何须", "何曾", "不曾",
    "正说着", "听见这话", "低头不语", "掩面而笑", "轻声说道",
    "垂泪", "叹息", "怔怔", "悄悄", "慢慢", "细细"
]

# 林黛玉风格描述词
LIN_DAIYU_DESCRIPTIONS = [
    " sad", " melancholic", " gentle", " soft", " elegant",
    " emotional", " sentimental", " longing", " pensive"
]


def to_lin_daiyu_style(text: str) -> str:
    """
    将文本转换为林黛玉风格
    由于 TTS 不支持音色克隆，通过文字内容来表达林黛玉的语气
    """
    # 保留原始文本，只在前面加上风格提示
    # TTS 会用默认音色朗读，但内容是林黛玉风格的
    styled_text = text
    return styled_text


def call_mimo_tts(text: str, voice: str = "mimo_default", style: str = None) -> bytes:
    """
    调用 MiMo TTS API 生成语音
    
    Args:
        text: 要转换的文本
        voice: 音色选项 (默认 mimo_default)
        style: 风格标签 (如 <style>Happy</style> 或 <style>唱歌</style>)
    
    Returns:
        WAV 格式的音频数据
    """
    import urllib.request
    import urllib.error
    import json
    
    # 构建消息内容
    content = text
    if style:
        content = f"<style>{style}</style>{text}"
    
    # API 请求数据
    # TTS 模型要求 role 为 assistant
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "assistant",
                "content": content
            }
        ],
        "audio": {
            "format": "pcm16",
            "voice": voice
        },
        "stream": False
    }
    
    # 发送请求
    url = f"{API_BASE_URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    print(f"🎤 调用 MiMo TTS API...")
    print(f"   文本: {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"   音色: {voice}")
    if style:
        print(f"   风格: {style}")
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            # 提取音频数据
            audio_data = result["choices"][0]["message"]["audio"]["data"]
            pcm_bytes = base64.b64decode(audio_data)
            
            print(f"✅ 获取到音频数据: {len(pcm_bytes)} bytes")
            return pcm_bytes
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"❌ HTTP Error {e.code}: {error_body}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        raise


def pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000, output_path: str = None) -> str:
    """
    将 PCM 数据转换为 WAV 文件
    
    Args:
        pcm_data: PCM 格式音频数据
        sample_rate: 采样率 (默认 24000 Hz)
        output_path: 输出文件路径
    
    Returns:
        生成的 WAV 文件路径
    """
    try:
        import soundfile as sf
    except ImportError:
        print("⚠️  soundfile 未安装，尝试使用替代方法...")
        # 如果没有 soundfile，使用简单的方法
        output_path = output_path or "output.wav"
        with open(output_path, "wb") as f:
            # 写入简单的 WAV 头
            import struct
            num_channels = 1
            bits_per_sample = 16
            byte_rate = sample_rate * num_channels * bits_per_sample // 8
            block_align = num_channels * bits_per_sample // 8
            data_size = len(pcm_data)
            file_size = 36 + data_size
            
            # RIFF header
            f.write(b"RIFF")
            f.write(struct.pack("<I", file_size))
            f.write(b"WAVE")
            
            # fmt chunk
            f.write(b"fmt ")
            f.write(struct.pack("<I", 16))  # chunk size
            f.write(struct.pack("<H", 1))   # audio format (PCM)
            f.write(struct.pack("<H", num_channels))
            f.write(struct.pack("<I", sample_rate))
            f.write(struct.pack("<I", byte_rate))
            f.write(struct.pack("<H", block_align))
            f.write(struct.pack("<H", bits_per_sample))
            
            # data chunk
            f.write(b"data")
            f.write(struct.pack("<I", data_size))
            f.write(pcm_data)
        
        return output_path
    
    # 使用 soundfile
    if output_path is None:
        output_path = "output.wav"
    
    # 转换 PCM int16 到 float32
    np_pcm = np.frombuffer(pcm_data, dtype=np.int16).astype(np.float32) / 32768.0
    
    # 保存为 WAV
    sf.write(output_path, np_pcm, samplerate=sample_rate)
    
    return output_path


def stream_tts(text: str, voice: str = "mimo_default", output_path: str = None):
    """
    流式调用 TTS，边接收边保存
    """
    import urllib.request
    import urllib.error
    import json
    
    content = text
    
    # TTS 模型要求 role 为 assistant
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "assistant", 
                "content": content
            }
        ],
        "audio": {
            "format": "pcm16",
            "voice": voice
        },
        "stream": True
    }
    
    url = f"{API_BASE_URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    print(f"🎤 流式调用 MiMo TTS...")
    
    collected_chunks = []
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            for line in response:
                line = line.decode("utf-8").strip()
                if not line or line == "data: [DONE]":
                    continue
                
                if line.startswith("data: "):
                    line = line[6:]
                
                try:
                    chunk = json.loads(line)
                    if chunk.get("choices"):
                        delta = chunk["choices"][0].get("delta", {})
                        audio = delta.get("audio")
                        
                        if audio and isinstance(audio, dict):
                            pcm_bytes = base64.b64decode(audio["data"])
                            collected_chunks.append(pcm_bytes)
                            print(f"   收到音频块: {len(pcm_bytes)} bytes")
                except json.JSONDecodeError:
                    continue
        
        if collected_chunks:
            pcm_data = b"".join(collected_chunks)
            output = pcm_to_wav(pcm_data, output_path=output_path)
            print(f"✅ 音频已保存: {output}")
            return output
        else:
            print("❌ 没有收到音频数据", file=sys.stderr)
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        raise


def main():
    parser = argparse.ArgumentParser(
        description="小米 MiMo TTS 语音合成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 基本用法
    python3 mimotts.py "你好，我是林黛玉"
    
    # 指定输出文件
    python3 mimotts.py "宝哥哥，你可来了！" --output lin-daiyu.wav
    
    # 指定风格
    python3 mimotts.py "Tomorrow is Friday, so happy!" --style Happy
    
    # 林黛玉风格
    python3 mimotts.py "人家心里头有好多话想跟你说呢……"
    
环境变量:
    MIMO_API_KEY  - API Key (默认使用脚本内置)
"""
    )
    
    parser.add_argument("text", help="要转换的文本")
    parser.add_argument("-o", "--output", default=None, help="输出文件路径 (默认: output.wav)")
    parser.add_argument("-v", "--voice", default="mimo_default", help="音色 (默认: mimo_default)")
    parser.add_argument("-s", "--style", default=None, help="风格标签 (如 Happy, Whisper, 唱歌)")
    parser.add_argument("--stream", action="store_true", help="使用流式调用")
    parser.add_argument("--api-key", default=None, help="API Key (优先于环境变量)")
    
    args = parser.parse_args()
    
    # 更新 API Key
    if args.api_key:
        global API_KEY
        API_KEY = args.api_key
    
    # 生成输出路径
    output_path = args.output
    if output_path is None:
        # 从文本生成文件名
        safe_name = "".join(c if c.isalnum() else "_" for c in args.text[:20])
        output_path = f"tts_output_{safe_name}.wav"
    
    try:
        if args.stream:
            result = stream_tts(args.text, args.voice, args.style, output_path)
        else:
            pcm_data = call_mimo_tts(args.text, args.voice, args.style)
            result = pcm_to_wav(pcm_data, output_path=output_path)
            print(f"✅ 音频已保存: {result}")
        
        # 尝试播放 (如果安装了 ffplay 或 afplay)
        try:
            if sys.platform == "darwin":
                subprocess.run(["afplay", result], timeout=5)
            elif sys.platform == "linux":
                subprocess.run(["ffplay", "-nodisp", "-autoexit", result], 
                             timeout=5, capture_output=True)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass  # 忽略播放错误
        
        return 0
        
    except Exception as e:
        print(f"❌ 失败: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
