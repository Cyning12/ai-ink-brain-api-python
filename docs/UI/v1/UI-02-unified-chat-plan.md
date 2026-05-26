# UI-02：Unified Chat（v1）方案 — 融合 RAG + Text2SQL + Chain Timeline

## 背景

现状：

- 现有 `/api/py/chat` 是**流式纯文本**（带 sources），不适合做“工具调用链可视化”
- Text2SQL 已有 JSON 形态输出（`/api/py/text2sql/chat`）
- Chain Timeline 已有 v1 雏形（`/api/py/chain/chat` 先覆盖 Text2SQL）

诉求：

- **不改动现有 RAG chat**（保持稳定）
- 新增一个“Unified Chat”入口：同一个页面/接口里可按意图选择：
  - RAG（知识检索问答）
  - Text2SQL（结构化查库）
  - 并统一输出 `events[]` 供前端展示 Chain Timeline（含 SQL/检索/耗时/错误）

## 目标（v1）

- 新增后端接口：`POST /api/py/unified/chat`（返回 JSON，核心字段 `events[]`）
- 前端新增页面：`/unified-chat`（或 `/chain-chat` 升级为 unified），渲染：
  - 左：消息流（自然语言）
  - 中：Chain Timeline（events）
  - 右：模式/工具开关与推荐问法（可简化）
- 统一事件模型：RAG 与 Text2SQL 都映射到相同 `events[]`

## 总体流程（v1）

1. 接收输入 `query`（与 session_id）
2. 意图识别（极简）：
   - 明显查库 → Text2SQL
   - 否则 → RAG
3. 执行对应链路，并在过程中记录 `events[]`
4. 返回：`{ ok, run_id, session_id, mode, events }`

> 说明：v1 不做“自动多路并行融合”；只做单路选择，后续再做 RAG+SQL 混合回答。

## 接口契约（建议）

### `POST /api/py/unified/chat`

请求：

```json
{ "session_id": "string", "query": "string", "prefer": "auto|rag|text2sql" }
```

响应：

```json
{
  "ok": true,
  "run_id": "uuid",
  "session_id": "string|null",
  "mode": "rag|text2sql",
  "events": [ { "type": "...", "ts": 0, "step_id": "...", "payload": {} } ]
}
```

鉴权：

- 与现有一致：`Authorization: Bearer <API_KEY>` 或 admin secret

## 事件模型（统一）

沿用 UI-01 约定，v1 至少包含：

- `assistant.message`
- `tool.call.start / tool.call.end`
- `sql.result`（仅 Text2SQL 路）
- `rag.sources`（仅 RAG 路：结构化 sources，避免前端解析 header/marker）
- `error`
- `latency`（总耗时 + 分阶段耗时）

### RAG 路的 events 映射建议

- `tool.call.start/end`: `rag.rewrite`、`rag.embed`、`rag.retrieve`、`rag.generate`
- `rag.sources`: `sources[]`（包含 relativePath/slug/score/snippet 等）
- `assistant.message`: 最终回答（非流式，v1 可直接返回一次性文本）

> v1 允许“RAG 路不流式”，优先保证事件完整；需要流式体验可在 v2 做 SSE events。

## 前端 UI（v1）

### 页面与入口

- 建议新增页面：`/unified-chat`
- 入口可放在首页模块卡片/顶部 Nav（建议仅管理员可见）

### 组件结构（建议）

- `UnifiedChatPanel`
  - `MessageList`（从 events 提取 assistant/user message）
  - `ChainTimeline`（直接渲染 events）
  - `RightPanel`（模式选择 prefer + 推荐问法）

## 兼容与迁移策略

- **不动** `/chat`（现有 RAG 流式）
- **保留** `/text2sql`（便于单模块验证）
- 新增 `/unified-chat` 作为升级入口；验证稳定后再考虑是否替代旧入口

## v1 里程碑

- M1：后端 `/api/py/unified/chat`（仅 Text2SQL + RAG 非流式）+ events
- M2：前端 `/unified-chat` 渲染 timeline + sql table + sources 卡片
- M3：完善错误与 latency 展示；推荐问法与模式切换

## 验收标准（v1）

- 同一页面内：
  - 查库问题 → 走 Text2SQL，能看到 sql.result 与 tool events
  - 知识问答 → 走 RAG，能看到 rag.sources 与检索/生成阶段 events
- 任一阶段失败：
  - 返回 `events[]`，包含 `error` 事件与可定位信息
- 前端无需解析 `x-sources` header 或尾部 marker 即可展示 sources（统一从 events 获取）

