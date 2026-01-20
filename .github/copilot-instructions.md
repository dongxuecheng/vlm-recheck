# VLM-Recheck 项目 Copilot 指南

## 项目概况
本项目的目标是开发一个稳健的 API 服务，为图像处理任务提供“二次确认”（复核）机制。外部用户将通过提供原始图像和相应的任务名称（例如“安全帽检测”）来调用此接口。系统利用 **Qwen3-VL** 模型来验证图像内容是否与声明的任务匹配。

## 关键组件与架构

### 1. 外部接口（已部署）
我们将与现有的内部服务集成。我们不应尝试重新部署它，而是调用其 API：
-   **Qwen3-VL 服务**：通过 vLLM 托管。用于高级语义理解、图像字幕或 VQA（视觉问答），以确定场景上下文是否与任务一致。

### 2. 核心 API 服务（待开发）
-   **技术栈**：Python，FastAPI。
-   **功能**：
    -   接收请求：`Image`（Multipart/Form-Data）+ `Task Name`（字符串）+`Task Description`（字符串）。
    -   返回标准化响应/结构化输出：布尔结果、推理原因、处理时间。

## 开发指南

### API 设计
-   **端点**：`POST /verify`（或类似）。
-   **输入 Schema**：
    ```json
    {
      "image": "...", // Multipart/Form-Data
      "task_name": "人员拥挤", // 例如 "crack_detection", "fire_detection"
      "task_description": "检测图像中是否出现了人员拥挤。"
    }
    ```
-   **输出 Schema**：
    ```json
    {
      "match": true,
      "reason": "检测到图像中人员拥挤的情况。",
      "processing_time": 0.5
    }
    ```

### 模型集成逻辑
1.  **提示工程**：根据 `task_name`和 `task_description` 动态构建提示。

### 最佳实践
-   **框架**：使用 FastAPI 以利用其异步功能和内置的文档生成。
-   **文档**：确保代码注释良好，并且 API 输入/输出有文档记录（例如 Swagger/OpenAPI）。
-   **错误处理**：优雅地处理外部模型服务停机或返回垃圾数据的情况。
-   **效率**：要考虑到该接口（/verify）的高并发情况，通常会被连续性的请求。

## 未来规划
-   如果不同的任务需要不同的处理，请维护将 `task_name` 映射到特定验证策略（提示/逻辑）的映射。
