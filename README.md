# VLM-Recheck API

基于 **Qwen3-VL** 的图像-任务匹配验证服务。该 API 接收图像文件和任务描述，使用 VLM 模型判断图像内容是否与任务匹配，并返回结构化的验证结果。

## 功能特性

- 🚀 **高性能异步架构**：基于 FastAPI 和 AsyncOpenAI，支持并发请求
- 🎯 **结构化输出**：使用 vLLM 的 guided JSON 确保可靠的响应格式
- 📊 **详细日志**：Loguru 提供结构化 JSON 日志，便于监控和调试
- 🐳 **Docker 部署**：完整的容器化方案，即开即用
- 🔒 **并发控制**：内置信号量机制，优化资源使用

## 项目结构

```
vlm-recheck/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   └── verify.py      # 验证端点
│   │   └── router.py          # API 路由
│   ├── schemas/
│   │   ├── request.py         # 请求模型
│   │   └── response.py        # 响应模型
│   ├── services/
│   │   └── verification.py    # 验证服务逻辑
│   ├── utils/
│   │   ├── logging.py         # 日志配置
│   │   └── prompts.py         # 提示词模板
│   ├── clients.py             # VLM 客户端
│   ├── config.py              # 配置管理
│   ├── exceptions.py          # 异常处理
│   ├── middleware.py          # 中间件
│   └── main.py                # FastAPI 应用入口
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## 快速开始

### 1. 环境配置

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# VLM Service Configuration
VLM_BASE_URL=http://localhost:8001/v1
VLM_MODEL_NAME=Qwen/Qwen2-VL-7B-Instruct
VLM_TIMEOUT=120.0
VLM_MAX_RETRIES=2

# API Configuration
MAX_CONCURRENT_REQUESTS=3

# Logging Configuration
LOG_LEVEL=INFO
LOG_JSON=true
```

### 2. 本地开发

**安装依赖：**

```bash
pip install -r requirements.txt
```

**启动服务：**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问交互式 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Docker 部署

**构建并启动服务：**

```bash
docker-compose up -d
```

**查看日志：**

```bash
docker-compose logs -f vlm-recheck
```

**停止服务：**

```bash
docker-compose down
```

## API 使用示例

### 端点：`POST /api/v1/verify`

**请求方式**：`multipart/form-data`

**请求参数**：
- `image` (file): 图像文件
- `task_description` (string): 任务描述

**请求示例（curl）：**

```bash
curl -X POST "http://localhost:8000/api/v1/verify" \
  -F "image=@/path/to/image.jpg" \
  -F "task_description=检测图像中是否出现了人员拥挤的情况。"

curl -X POST "http://localhost:8000/api/v1/verify" -F "image=@/path/to/image.jpg" -F "task_description=检测图像中是否出现了人员拥挤的情况。"
```

**请求示例（Python）：**

```python
import requests

files = {"image": open("image.jpg", "rb")}
data = {"task_description": "检测图像中是否出现了人员拥挤的情况。"}

response = requests.post(
    "http://localhost:8000/api/v1/verify",
    files=files,
    data=data
)

result = response.json()
print(f"Match: {result['match']}")
print(f"Reason: {result['reason']}")
print(f"Processing time: {result['processing_time']}s")
```

**响应示例：**

```json
{
  "match": true,
  "reason": "检测到图像中人员拥挤的情况。",
  "processing_time": 0.523
}
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `VLM_BASE_URL` | Qwen3-VL 服务的 OpenAI 兼容 API 地址 | `http://localhost:8001/v1` |
| `VLM_MODEL_NAME` | 模型名称 | `Qwen/Qwen2-VL-7B-Instruct` |
| `VLM_TIMEOUT` | 请求超时时间（秒） | `120.0` |
| `VLM_MAX_RETRIES` | 最大重试次数 | `2` |
| `MAX_CONCURRENT_REQUESTS` | 最大并发请求数 | `3` |
| `LOG_LEVEL` | 日志级别（DEBUG/INFO/WARNING/ERROR） | `INFO` |
| `LOG_JSON` | 是否使用 JSON 格式日志 | `true` |

## 架构设计

### 核心特性

1. **分层架构**：API → Services → Clients，职责清晰
2. **异步处理**：全链路异步，提升并发性能
3. **结构化输出**：使用 vLLM 的 guided JSON，确保响应格式一致
4. **并发控制**：信号量限制同时处理的请求数，防止资源耗尽
5. **优雅的错误处理**：区分不同类型的错误，返回合适的 HTTP 状态码

### 提示词策略

系统使用精心设计的提示词模板，确保 VLM 模型准确理解任务：

```
根据任务名称'{task_name}'和任务描述'{task_description}'，请判断输入的图像内容是否与该任务匹配。

请仔细分析图像内容，并基于以下标准进行判断：
1. 图像中是否包含与任务相关的对象、场景或情况
2. 图像的内容是否符合任务描述中的具体要求
3. 图像质量是否足以进行准确判断
```

## 开发指南

### 添加新的验证策略

如需针对特定任务类型定制验证逻辑，可在 [app/utils/prompts.py](app/utils/prompts.py) 中扩展：

```python
def build_custom_prompt(task_name: str, task_description: str) -> str:
    # 自定义提示词逻辑
    pass
```

### 运行测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/
```

### 代码格式化

```bash
# 使用 ruff 检查和格式化
ruff check app/
ruff format app/
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**技术栈：** FastAPI · Qwen3-VL · vLLM · OpenAI SDK · Loguru · Docker
