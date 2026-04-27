# Task：Unified Chat（后端 v1）— 融合 RAG + Text2SQL + events[]

> **状态**：pending  
> **范围**：仅后端 `ai-ink-brain-api-python`  
> **设计**：`docs/UI/v1/UI-02-unified-chat-plan.md`  
> **前端依赖**：`task_frontend_unified_chat_ui_v1.md`（events[] 渲染 + Timeline UI）

## 目标

新增接口 `POST /api/py/unified/chat`：

- 自动（或按 prefer）选择 RAG / Text2SQL
- 返回统一 `events[]`，供前端 Chain Timeline 渲染
- 不改动现有 `/api/py/chat`（流式）与 `/api/py/text2sql/chat`

## 需求

### 1) 新接口与鉴权

- [ ] `POST /api/py/unified/chat`
- [ ] 鉴权逻辑复用现有（API_KEY 或 admin secret）

### 2) 意图识别（极简）

- [ ] `prefer=rag|text2sql|auto`：
  - `rag`：强制走 RAG
  - `text2sql`：强制走 Text2SQL
  - `auto`：使用现有 `is_text2sql_intent()` 判断

### 3) 事件输出（统一）

- [ ] `events[]` 至少包含：
  - `assistant.message`
  - `tool.call.start/end`
  - `error`
  - `latency`（total + stages_ms）
- [ ] Text2SQL 路增加：
  - `sql.result`
- [ ] RAG 路增加：
  - `rag.sources`（结构化 sources，避免前端再解析 header/marker）

### 4) 结果截断

- [ ] `sql.result.rows` 默认最多 20 行（`truncated` 标记）
- [ ] `rag.sources` 默认最多 10 条（snippet 截断）

## 验收

- [ ] 查库问题：返回 `mode=text2sql`，包含 `sql.result`
- [ ] 知识问题：返回 `mode=rag`，包含 `rag.sources`
- [ ] 任一失败：仍返回 `events[]`，且包含 `error` 事件（可定位阶段）
- [ ] 单测覆盖：授权/成功/失败/auto 分支

## 实现备忘

- 可复用现有 `api/chain_chat.py`（Text2SQL events）为子模块
- RAG 路 v1 可先做非流式（一次性 answer + sources + latency），事件更完整更易展示

