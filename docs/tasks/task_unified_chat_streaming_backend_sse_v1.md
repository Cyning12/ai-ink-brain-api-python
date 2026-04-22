# Task：Unified Chat Streaming（后端 v1 / SSE）

状态：pending  
范围：仅后端 `ai-ink-brain-api-python`  
设计：`docs/UI/v1/UI-03-unified-chat-streaming-sse.md`

## 目标

新增 SSE 接口 `POST /api/py/unified/chat/stream`：

- 流式输出 `chain` 事件（timeline 实时渲染）
- v1 可不做 token 级文本流（可后续增强）
- 保留非流式 `POST /api/py/unified/chat`

## 需求

### 1) 新路由与鉴权

- [ ] `POST /api/py/unified/chat/stream`
- [ ] 与 unified/chat 一致的鉴权（API_KEY 或 admin secret）

### 2) SSE 事件输出

- [ ] 正确设置 header：
  - `Content-Type: text/event-stream; charset=utf-8`
  - `Cache-Control: no-cache`
- [ ] 事件格式：
  - `event: chain` + `data: <json>`
  - `event: done` + `data: <json>`

### 3) 事件语义（v1）

- [ ] 至少覆盖：
  - `tool.call.start/end`
  - `rag.sources`（RAG 路）
  - `sql.result`（Text2SQL 路）
  - `assistant.message`
  - `error`
  - `latency`
- [ ] 事件 `payload` 与非流式 unified/chat 保持一致（便于前端复用渲染逻辑）

### 4) 错误与收敛

- [ ] 任一阶段失败：
  - 输出 `error` 事件
  - 最终输出 `done` 事件（`ok=false`）
- [ ] 确保客户端断开时不再 yield（避免 GeneratorExit）

## 验收

- [ ] curl 可看到连续的 `event: chain` 输出
- [ ] RAG 路、Text2SQL 路都可走通并输出 `done`
- [ ] 单测覆盖：授权 / prefer 分支 / 断开安全（可用简化测试）

## 实现备忘

- v1 推荐实现方式：把现有 `handle_unified_chat` 的阶段逻辑抽成“产出事件的生成器”
- RAG 生成可先非流式，完成后一次性发 `assistant.message`

