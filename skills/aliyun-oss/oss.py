#!/usr/bin/env python3
"""
阿里云 OSS 文件上传/下载工具
用法:
  上传: python oss.py upload <本地路径> <OSS路径> [--bucket <bucket>]
  下载: python oss.py download <OSS路径> <本地路径> [--bucket <bucket>]
  列举: python oss.py list [<前缀>] [--bucket <bucket>]

凭证从 credentials.json 加载:
  {
    "aliyun_oss": {
      "access_key_id": "...",
      "access_key_secret": "...",
      "region": "cn-hangzhou",
      "bucket": "my-bucket",
      "endpoint": ""  // 可选，不填则自动推断
    }
  }
"""

import sys
import os
import json
import argparse
from pathlib import Path

CREDS_PATH = Path(__file__).parent.parent.parent / "credentials.json"


ALLOWED_BUCKET = "openclaw-home"


def load_config(bucket_override=None):
    """加载阿里云 OSS 配置"""
    with open(CREDS_PATH) as f:
        creds = json.load(f)

    cfg = creds.get("aliyun_oss", {})
    if not cfg:
        raise ValueError("credentials.json 中未找到 aliyun_oss 配置")

    required = ["access_key_id", "access_key_secret", "region"]
    for key in required:
        if not cfg.get(key):
            raise ValueError(f"aliyun_oss 配置缺少字段: {key}")

    if bucket_override:
        if bucket_override != ALLOWED_BUCKET:
            raise PermissionError(f"禁止操作 bucket '{bucket_override}'，只允许使用 '{ALLOWED_BUCKET}'")
        cfg["bucket"] = bucket_override

    if not cfg.get("bucket"):
        raise ValueError("未指定 bucket，请在配置中设置或通过 --bucket 参数传入")

    # 强制校验 bucket
    if cfg["bucket"] != ALLOWED_BUCKET:
        raise PermissionError(f"禁止操作 bucket '{cfg['bucket']}'，只允许使用 '{ALLOWED_BUCKET}'")

    return cfg


def build_client(cfg):
    """构建 OSS 客户端"""
    import alibabacloud_oss_v2 as oss

    credentials_provider = oss.credentials.StaticCredentialsProvider(
        access_key_id=cfg["access_key_id"],
        access_key_secret=cfg["access_key_secret"],
    )

    oss_cfg = oss.config.load_default()
    oss_cfg.credentials_provider = credentials_provider
    oss_cfg.region = cfg["region"]

    if cfg.get("endpoint"):
        oss_cfg.endpoint = cfg["endpoint"]

    return oss.Client(oss_cfg)


def cmd_upload(args):
    """上传文件到 OSS"""
    import alibabacloud_oss_v2 as oss

    local_path = Path(args.local_path)
    if not local_path.exists():
        raise FileNotFoundError(f"本地文件不存在: {local_path}")

    cfg = load_config(args.bucket)
    client = build_client(cfg)

    oss_key = args.oss_path

    # 使用文件上传管理器（自动支持大文件分片）
    uploader = client.uploader()
    result = uploader.upload_file(
        oss.PutObjectRequest(
            bucket=cfg["bucket"],
            key=oss_key,
        ),
        filepath=str(local_path),
    )

    file_size = local_path.stat().st_size
    output = {
        "success": True,
        "action": "upload",
        "local_path": str(local_path),
        "oss_key": oss_key,
        "bucket": cfg["bucket"],
        "region": cfg["region"],
        "file_size": file_size,
        "etag": getattr(result, "etag", None),
    }
    print(json.dumps(output, ensure_ascii=False))


def cmd_download(args):
    """从 OSS 下载文件"""
    import alibabacloud_oss_v2 as oss

    cfg = load_config(args.bucket)
    client = build_client(cfg)

    oss_key = args.oss_path
    local_path = Path(args.local_path)

    # 自动创建目录
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # 使用文件下载管理器（自动支持大文件并发下载）
    downloader = client.downloader()
    result = downloader.download_file(
        oss.GetObjectRequest(
            bucket=cfg["bucket"],
            key=oss_key,
        ),
        filepath=str(local_path),
    )

    file_size = local_path.stat().st_size if local_path.exists() else 0
    output = {
        "success": True,
        "action": "download",
        "oss_key": oss_key,
        "local_path": str(local_path),
        "bucket": cfg["bucket"],
        "region": cfg["region"],
        "file_size": file_size,
    }
    print(json.dumps(output, ensure_ascii=False))


def cmd_list(args):
    """列举 OSS 文件"""
    import alibabacloud_oss_v2 as oss

    cfg = load_config(args.bucket)
    client = build_client(cfg)

    prefix = args.prefix or ""
    objects = []

    paginator = client.list_objects_v2_paginator()
    for page in paginator.iter_page(
        oss.ListObjectsV2Request(
            bucket=cfg["bucket"],
            prefix=prefix,
            max_keys=100,
        )
    ):
        for obj in (page.contents or []):
            objects.append({
                "key": obj.key,
                "size": obj.size,
                "last_modified": str(obj.last_modified) if obj.last_modified else None,
                "etag": obj.etag,
            })

    output = {
        "success": True,
        "action": "list",
        "bucket": cfg["bucket"],
        "prefix": prefix,
        "count": len(objects),
        "objects": objects,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="阿里云 OSS 工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # upload 子命令
    upload_parser = subparsers.add_parser("upload", help="上传文件")
    upload_parser.add_argument("local_path", help="本地文件路径")
    upload_parser.add_argument("oss_path", help="OSS 目标路径（对象键）")
    upload_parser.add_argument("--bucket", help="覆盖配置中的 bucket")

    # download 子命令
    download_parser = subparsers.add_parser("download", help="下载文件")
    download_parser.add_argument("oss_path", help="OSS 源路径（对象键）")
    download_parser.add_argument("local_path", help="本地保存路径")
    download_parser.add_argument("--bucket", help="覆盖配置中的 bucket")

    # list 子命令
    list_parser = subparsers.add_parser("list", help="列举文件")
    list_parser.add_argument("prefix", nargs="?", default="", help="路径前缀（可选）")
    list_parser.add_argument("--bucket", help="覆盖配置中的 bucket")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "upload":
            cmd_upload(args)
        elif args.command == "download":
            cmd_download(args)
        elif args.command == "list":
            cmd_list(args)
    except Exception as e:
        error = {"success": False, "error": str(e)}
        print(json.dumps(error, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
