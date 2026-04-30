# Task：Unified Chat（后端 v1）— 融合 RAG + Text2SQL + events[]

> **状态**：done（2026-04-28 验收通过）  
> **归档路径**：`docs/tasks/done/done_unified_chat_backend_v1.md`  
> **范围**：仅后端 `ai-ink-brain-api-python`  
> **设计**：`docs/UI/v1/UI-02-unified-chat-plan.md`  
> **关联任务**：SSE 流式见 `docs/tasks/done/done_unified_chat_streaming_backend_sse_v1.md`

---

## 目标

新增接口 `POST /api/py/unified/chat`：

- 自动（或按 prefer）选择 RAG / Text2SQL
- 返回统一 `events[]`，供前端 Chain Timeline 渲染
- 不改动现有 `/api/py/chat`（流式）与 `/api/py/text2sql/chat`

---

## 需求（完成情况）

### 1) 新接口与鉴权

- [x] `POST /api/py/unified/chat`
- [x] 鉴权逻辑复用现有（API_KEY 或 admin secret）

**落点**

- 路由：`api/index.py` 注册 `/api/py/unified/chat`
- 处理：`api/unified_chat.py::handle_unified_chat`
- 鉴权：`api/unified_chat.py::_require_unified_auth`

### 2) 意图识别（极简）

- [x] `prefer=rag|text2sql|auto`：
  - `rag`：强制走 RAG
  - `text2sql`：强制走 Text2SQL
  - `auto`：使用路由器决定（Text2SQL / RAG / no_data）

**落点**

- `api/unified_chat.py::_parse_prefer`
- `api/intent_router.py` + `api/unified_chat.py::decide_intent`（统一决策事件：`router.decision`）

### 3) 事件输出（统一）

- [x] `events[]` 至少包含：
  - `assistant.message`
  - `tool.call.start/end`
  - `error`
  - `latency`（total + stages_ms）
- [x] Text2SQL 路增加：
  - `sql.result`
- [x] RAG 路增加：
  - `rag.sources`（结构化 sources，避免前端再解析 header/marker）

**落点**

- 事件生成：`api/unified_chat.py::_event`
- RAG sources 打包：`api/unified_chat.py::_build_rag_sources_event`

### 4) 结果截断

- [x] `sql.result.rows` 默认最多 20 行（`truncated` 标记）
- [x] `rag.sources` 默认最多 10 条（snippet 截断）

---

## 验收（完成情况）

- [x] 查库问题：返回 `mode=text2sql`，包含 `sql.result`
- [x] 知识问题：返回 `mode=rag`，包含 `rag.sources`
- [x] 任一失败：仍返回 `events[]`，且包含 `error` 事件（可定位阶段）
- [x] 单测覆盖：授权/成功/失败/auto 分支（见下）

---

## 测试与证据

- 单测：`tests/test_unified_chat_backend_v1.py`
- 路由/auto 分支：`tests/test_intent_router_backend_v1.py`

---

## 实现备忘（最终实现）

- Text2SQL 分支：沿用“chain 风格 events”，并输出 `sql.result + assistant.message + latency`
- RAG 分支 v1：非流式生成（一次性 answer + sources + latency），事件更完整更易展示
