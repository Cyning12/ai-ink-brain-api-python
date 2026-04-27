# Task：Intent Router（后端 v1）— Unified Chat 路由增强（rag/text2sql/no_data/tool）

状态：pending  
范围：仅后端 `ai-ink-brain-api-python`  
设计：`docs/UI/v1/UI-04-intent-router-v1.md`

## 目标

增强 Unified Chat 的 `prefer=auto` 路由能力：

- 新增 `mode=no_data`
- 预留 `mode=tool:*`
- 增加 “规则 + 证据校验” 两段式决策
- 输出 `router.decision` 事件，便于前端可视化与调试

## 范围

- 修改 `POST /api/py/unified/chat` 与 `/api/py/unified/chat/stream`
- 新增/复用路由模块（建议 `api/intent_router.py`）
- 不改现有 `/api/py/chat`

## 需求

### 1) 新增 mode

- [ ] `mode=no_data`：不做检索，仅 LLM 直接回答（仍输出 events）
- [ ] `mode=tool:*`：未实现时返回 error 事件（v1 可仅预留不接入工具）

### 2) evidence check

- [ ] SQL evidence：Text2SQL DDL 检索 topk=3，命中则允许走 text2sql
- [ ] RAG evidence：`keyword_documents(query, match_count=3)` 命中则走 rag，否则偏向 no_data

### 3) 可观测事件

- [ ] 在 events[] 中输出 `router.decision`：
  - prefer/candidate/final/rule_hits/evidence/fallback

### 4) 单测

- [ ] auto → text2sql（ddl 命中）
- [ ] auto → rag（fts 命中）
- [ ] auto → no_data（fts=0 且非 sql）
- [ ] prefer 强制覆盖（rag/text2sql/no_data）

## 验收

- [ ] v1 用例通过（见 UI-04）
- [ ] 前端可展示 router.decision

