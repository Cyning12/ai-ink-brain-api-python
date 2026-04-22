# UI-03：Unified Chat Streaming（方案 A / SSE）— 事件流 + Timeline 实时渲染

## 目标

将 `Unified Chat` 从一次性 JSON 升级为**流式展示**，实现：

- 前端实时看到 chain timeline（tool start/end、sources、sql.result、latency、error）
- v1 优先保证「事件实时」；token 级文本流可作为 v2 增强

## 协议选型：SSE（Server-Sent Events）

新增后端接口：

- `POST /api/py/unified/chat/stream`

响应：

- `Content-Type: text/event-stream; charset=utf-8`
- `Cache-Control: no-cache`
- `Connection: keep-alive`

## 事件类型（SSE）

每条 SSE 消息使用：

- `event: <name>`
- `data: <json>`

### 1) `event: chain`

用于 timeline 的单条事件：

```json
{ "type":"tool.call.start", "ts": 12, "step_id":"t_rewrite", "payload": { } }
```

`type` 取值沿用 UI-02 的 `events[]` 事件模型：

- `tool.call.start` / `tool.call.end`
- `rag.sources`
- `sql.result`
- `assistant.message`
- `error`
- `latency`

### 2) `event: token`（v1 可选，v2 推荐）

用于逐 token 输出 assistant 文本（若后端支持流式生成）：

```json
{ "text": "..." }
```

### 3) `event: done`

表示一次请求结束：

```json
{ "ok": true, "mode":"rag", "run_id":"uuid" }
```

## 兼容策略

- 保留现有非流式 `POST /api/py/unified/chat`（便于回退与测试）
- 流式接口仅新增，不改动 `/api/py/chat` 与 `/api/py/text2sql/chat`

## v1 实现边界（建议）

- 必须：`chain` 事件流（timeline 实时更新）
- 可选：`token` 事件（文本逐字输出）
- RAG 路 v1 可以仍用非流式生成 answer：生成完成后一次性发 `assistant.message`
- Text2SQL 路 v1 事件可实时：retrieve→generate_sql→execute_sql→summarize

## 验收标准（v1）

- 前端发起请求后，Timeline 至少能实时出现：
  - `tool.call.start/end`（rewrite、retrieve、execute 等）
  - `rag.sources` 或 `sql.result`
  - `assistant.message`
  - `latency`
- 错误路径仍能看到 `error` 事件，且最后有 `done`

