# 阿里云 OSS 工具

上传 / 下载 / 列举 阿里云 OSS 文件。基于官方 Python SDK V2。

## 配置

凭证写入 `credentials.json` → `aliyun_oss` 节点：

```json
{
  "aliyun_oss": {
    "access_key_id": "你的 AccessKey ID",
    "access_key_secret": "你的 AccessKey Secret",
    "region": "cn-beijing",
    "bucket": "默认 bucket 名称",
    "endpoint": ""
  }
}
```

- `endpoint` 可选，不填则根据 region 自动推断公网地址
- 可通过 `--bucket` 参数临时覆盖默认 bucket

## 使用方法

```bash
# 上传文件
python /root/.openclaw/workspace/skills/aliyun-oss/oss.py upload <本地路径> <OSS路径>

# 下载文件
python /root/.openclaw/workspace/skills/aliyun-oss/oss.py download <OSS路径> <本地路径>

# 列举文件
python /root/.openclaw/workspace/skills/aliyun-oss/oss.py list [前缀]

# 指定 bucket
python /root/.openclaw/workspace/skills/aliyun-oss/oss.py upload file.txt img/file.txt --bucket other-bucket
```

## 输出格式（JSON）

**上传成功：**
```json
{
  "success": true,
  "action": "upload",
  "local_path": "/tmp/test.txt",
  "oss_key": "folder/test.txt",
  "bucket": "my-bucket",
  "region": "cn-guangzhou",
  "file_size": 1234,
  "etag": "\"ABC123\""
}
```

**下载成功：**
```json
{
  "success": true,
  "action": "download",
  "oss_key": "folder/test.txt",
  "local_path": "/tmp/test.txt",
  "bucket": "my-bucket",
  "region": "cn-guangzhou",
  "file_size": 1234
}
```

**失败：**
```json
{"success": false, "error": "错误信息"}
```

## 特性

- ✅ 自动分片上传（大文件）
- ✅ 并发下载（大文件）
- ✅ 自动 CRC64 校验
- ✅ 自动创建本地目录
- ✅ JSON 输出，易于解析

## 依赖

```bash
pip3 install alibabacloud-oss-v2
```

已安装 ✅
