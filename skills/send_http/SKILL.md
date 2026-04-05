---
name: send-http
description: |
  简单的 HTTP 请求发送工具。当用户想要发送 HTTP/HTTPS 请求时使用此 skill，
  特别是需要快速测试 API、发送请求而不想使用复杂的 curl 命令时。
  适用于：发送 HTTP 请求、测试 REST API、快速调试端点、替代 curl 的简单工具。
  用户只需要提供 URL 即可发送请求，支持自定义 header、body 文件、HTTP 方法。
  响应 body 保存到文件。
---

# send-http - 简单 HTTP 请求工具

## 功能概述

发送 HTTP/HTTPS 请求的简单工具，默认参数简单。

## 触发条件

当用户表达以下意图时使用此 skill：
- 发送 HTTP 请求
- 测试 API 端点
- 快速调试 HTTP 服务
- 需要简单的请求工具（替代 curl）
- 发送 POST/GET/PUT/DELETE 等请求

## 核心特性

### 参数设计

```
send_http.py <url> [-b <body_file>] [-H <header>] [-m <method>]
```

- `url`: 必需，HTTP/HTTPS URL
- `-b/--body`: 可选，body 文件路径
- `-H/--header`: 可选，自定义 header（可多次使用），格式：`key=value`
- `-m/--method`: 可选，HTTP 方法（默认 GET）


### 输出逻辑

1. **终端显示**：
   - 始终显示分隔符以上的内容（原始响应）
   - 分隔符以下的内容（工具信息）包括：响应大小、文件保存路径
   
2. **文件保存**：
   - 只保存 response body（不含 status 和 headers）
   - 文件名格式：`{prefix}{timestamp}.txt`
   - 自动创建保存目录

## 使用示例

### 基本 GET 请求
```bash
./send_http.py https://api.example.com/data
```

### POST 请求带 body 文件
```bash
./send_http.py https://api.example.com/post -b request.json
```

### 自定义 header
```bash
./send_http.py https://api.example.com -H "Authorization=Bearer token123"
```

### 自定义 HTTP 方法
```bash
./send_http.py https://api.example.com/resource -m PUT -b data.json
```

### 完整示例
```bash
./send_http.py https://httpbin.org/post \
  -b body.json \
  -H "X-Custom=Value" \
  -H "Authorization=Bearer xyz" \
  -m POST
```

## 输出示例

终端输出（响应 < 1024 字节且为文本）：
```
HTTP/1.1 200 OK
==================================================
{"result": "success", "data": [...]}
==================================================
Response size: 429 bytes
Complete response saved to: ./output/response_1234567890.txt
```

终端输出（响应 >= 1024 字节）：
```
HTTP/1.1 200 OK
==================================================
==================================================
Response size: 27869 bytes
Complete response saved to: ./output/response_1234567890.txt
```

