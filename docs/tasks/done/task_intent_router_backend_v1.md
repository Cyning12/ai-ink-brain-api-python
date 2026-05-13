# Task：Intent Router（后端 v1）— Unified Chat 路由增强（rag/text2sql/no_data/tool）

状态：**done（核心已落地；2026-05-08 回补 `rag_rule_hits` 与 no_data 门控验收；2026-05-13 自 `docs/tasks/active/` 迁入 `docs/tasks/done/`）**  
范围：仅后端 `ai-ink-brain-api-python`  
设计：`docs/UI/v1/UI-04-intent-router-v1.md`  
实现真值：`api/intent_router.py`

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

- [x] v1 用例通过（见 UI-04；单测 `tests/test_intent_router_backend_v1.py`）
- [x] 前端可展示 router.decision（见 `ai-ink-brain` 任务 `task_frontend_intent_router_debug_v1.md`）

---

## 2026-05-08 回补：`rag_rule_hits`、候选优先级、RAG 分支 no_data 门控

### 背景与目标

- **问题**：口语里带「查询」等 SQL 关键词、但实际要读 **日记 / `.md` / 文档** 的问句，易被 V1 判为 `text2sql`；证据双空时又过早落到 `no_data`，与「应先走 RAG」的产品预期不一致。
- **改动摘要**（`api/intent_router.py`，已实现）：
  - 新增 **`_rag_rule_hits`**，命中写入 `rule_hits`（如 `rule:rag_keywords`、`rule:date_doc_hint`）。
  - **`prefer=auto` 候选顺序**：在 `no_data` / `text2sql` 之前优先 **`rag_hits` → `rag` 候选**。
  - **`final_mode == "rag"` 且 FTS 无命中**：仅当 **`ddl_hits <= 0` 且 `fts_hits <= 0` 且无 `rag_hits`** 时再降为 `no_data`；否则保持 `rag`（含 `rag_without_evidence_but_rag_signals` / `rag_without_fts_keep_rag_ddl_evidence` 等 `fallback` 标签）。

### 自动化验收

- [x] `tests/test_intent_router_backend_v1.py`：`test_router_rag_signals_priority_over_sql_keywords`、`test_router_rag_keeps_when_ddl_positive_but_fts_empty` 等全部通过。

### 手工 / 联调验收（ChatBI V2 Agent + SSE vNext）

**环境**：`CHATBI_USE_AGENT=true`，意图 LLM 可用；Unified Chat 增量 SSE（`X-ChatBI-Sse-Contract: 2` 等按部署约定）。

| Query | 预期 | 验收结果 |
|--------|------|----------|
| `2026-04-28.md写了什么` | `agent.intent` → `rag_search` / `mode: rag`；`router.decision.final_mode` → `rag`；执行 `rag_search` → `agent.llm.*` `rag_generate` → 可见总结正文 | **符合预期**（2026-05-08） |
| `查询下我的2026-04-28的日记`（V1 超时/降级路径） | V1 侧 **`candidate_mode: rag`**，不因单独「查询」锁死 `text2sql`；证据双空时仍可 **`final_mode: rag`** + `fallback: rag_without_evidence_but_rag_signals`（由单测锁定） | **符合预期**（单测） |

### 非范围

- 不修改 V2 `decide_intent_v2` 的 LLM prompt 本体（本回补仅 V1 规则与证据门控）；意图超时仍可能走 V1，但行为与上表对齐。
- 不保证「无 rag 信号、无证据」类泛问句仍走 RAG（此类仍可 `no_data`，属设计内）。

