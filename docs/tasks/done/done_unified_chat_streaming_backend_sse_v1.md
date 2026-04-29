# Task：Unified Chat Streaming（后端 v1 / SSE）

> **状态**：done（2026-04-28 验收通过）  
> **归档路径**：`docs/tasks/done/done_unified_chat_streaming_backend_sse_v1.md`  
> **范围**：仅后端 `ai-ink-brain-api-python`  
> **设计**：`docs/UI/v1/UI-03-unified-chat-streaming-sse.md`  
> **契约真值**：`docs/_tech_graph/_contract_manifest.json`（SSE/events keys 与枚举集合）

---

## 目标

新增 SSE 接口 `POST /api/py/unified/chat/stream`：

- 流式输出 `chain` 事件（timeline 实时渲染）
- v1 可不做 token 级文本流（后续增强）
- 保留非流式 `POST /api/py/unified/chat`

---

## 需求（完成情况）

### 1) 新路由与鉴权

- [x] `POST /api/py/unified/chat/stream`
- [x] 与 unified/chat 一致的鉴权（API_KEY 或 admin secret）

**落点**

- 路由：`api/index.py` 注册 `/api/py/unified/chat/stream`
- 处理：`api/unified_chat.py::handle_unified_chat_stream`
- 鉴权：`api/unified_chat.py::_require_unified_auth`

### 2) SSE 事件输出

- [x] 正确设置 header：
  - `Content-Type: text/event-stream; charset=utf-8`
  - `Cache-Control: no-cache`
- [x] 事件格式：
  - `event: chain` + `data: <json>`
  - `event: done` + `data: <json>`

**落点**

- SSE 格式化：`api/unified_chat.py::_sse`
- 返回：`fastapi.responses.StreamingResponse`

### 3) 事件语义（v1）

- [x] 至少覆盖：
  - `tool.call.start/end`
  - `rag.sources`（RAG 路）
  - `sql.result`（Text2SQL 路）
  - `assistant.message`
  - `error`
  - `latency`
- [x] 事件 `payload` 与非流式 unified/chat 保持一致（便于前端复用渲染逻辑）

### 4) 错误与收敛

- [x] 任一阶段失败：
  - 输出 `error` 事件
  - 最终输出 `done` 事件（`ok=false`）
- [x] 确保客户端断开时不再 yield（避免 GeneratorExit）

---

## 验收（完成情况）

- [x] curl 可看到连续的 `event: chain` 输出（单测校验 `event: chain` + `event: done`）
- [x] RAG 路、Text2SQL 路都可走通并输出 `done`
- [x] 单测覆盖：授权 / prefer 分支 / 断开安全（简化测试）

---

## 测试与证据

- 单测：`tests/test_unified_chat_streaming_sse.py`
- 非流式一致性：`tests/test_unified_chat_backend_v1.py`
