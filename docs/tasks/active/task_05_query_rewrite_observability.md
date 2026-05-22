# Task：Rewrite 可观测性（raw vs rewrite 召回对比 + 关键实体丢失）

> **状态**：in_progress（2026-05-22 · P0-B/C Harness 试点）  
> **关联图谱**：`docs/_tech_graph/10_flow_rag.md`  
> **关联 Issue/PR**：无  
> **前端依赖**：无（仅 metadata / DEBUG_RAG；前端展示另任务）

> 落盘：`docs/tasks/active/` · Harness 试点见 [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §0.3

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `recommended` |
| **test_strategy_note** | — |
| **freeze_id** | `task_05_query_rewrite_obs@2026-05-22` |
| **gates_before_code** | `failure_paths`, 验收命令, 必读路径 |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/query-rewrite-obs` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | 试点 task 已按模板补齐 |
| HG-AUDIT-R1 | approved | 30 | R1 落盘后 **人** 改 approved（见 `reviews/task_05_*_audit_R1_*.md`） |
| HG-REINSPECT | approved | done | 50 落盘后人签 |

---

## 背景与目标

排查「rewrite 导致检索变差 / 丢失关键 token（如 task_04、文件名、日期）」时，不宜频繁查 Supabase 或翻 `rag_conversation_logs` 全文。

**完成态**：

- 每次 `POST /api/py/chat` 在 `rag_conversation_logs.metadata.match.query_compare` 写入 raw vs rewrite 对比指标；
- `DEBUG_RAG=1` 时终端一行 `query_compare` 摘要。

> 不改变对外 API 契约；双查询并行融合另起任务。

---

## 范围

- [x] `POST /api/py/chat`：`metadata.match.query_compare` 字段（实现见 `api/index.py`）
- [x] Keyword 路 raw/rewrite 各跑一次计数（仅观测，不改变融合策略）
- [x] `compare_anchor_tokens` 关键实体丢失判定（`api/keyword_fallback.py`）
- [x] `DEBUG_RAG=1` 日志摘要
- [x] 单测：`tests/test_query_rewrite_compare_anchor.py`

## 非范围

- 不修改 Supabase SQL
- 不改变 RRF 融合主策略
- 不新增前端 UI

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| API | `POST /api/py/chat` · `api/index.py` |
| 表 | `public.rag_conversation_logs` · `docs/_tech_graph/01_struct.md` |
| 图谱 | `docs/_tech_graph/10_flow_rag.md` |
| 锚点规则 | `api/keyword_fallback.py` · `ANCHOR_TOKEN_PATTERNS` |

---

## 设计（`metadata.match.query_compare`）

| 字段 | 含义 |
|------|------|
| `query_raw` / `query_rewrite` | 原始与改写问句 |
| `recall_raw_count` / `recall_rw_count` | Keyword/FTS 路命中数 |
| `recall_raw_top1_score` / `recall_rw_top1_score` | Keyword Top1 `score`（`score_type: fts_score`） |
| `is_key_entity_lost` | raw 锚点 token 是否在 rewrite 中缺失 |
| `key_entities` | `tokens_raw` / `tokens_rewrite` / `missing` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | Supabase 不可用 | 检索失败；日志可能无 `query_compare` | 是 | 流式仍可能降级；500 类 |
| F2 | Embedding 失败 | keyword-only；`query_compare` 仍写入 | 是 | 无向量路 |
| F3 | rewrite 失败 | `rewritten_query=query`；对比仍有效 | — | 无单独错误码 |

---

## 验收标准

- [x] `metadata.match.query_compare` 含约定字段（`build_rag_match_meta` / `index.py`）
- [x] 含 `task_04` / 文件名 / 日期 时，rewrite 丢 token → `is_key_entity_lost=true` 且 `missing` 含对应 token（单测覆盖）
- [x] `DEBUG_RAG=1` 输出 `query_compare` 一行摘要
- [x] 不影响流式输出与 sources

**测试命令**：`pytest tests/test_query_rewrite_compare_anchor.py -q`

---

## 实现备忘

| 项 | 内容 |
|----|------|
| 涉及文件 | `api/index.py`, `api/keyword_fallback.py`, `api/rag_logging.py`, `tests/test_query_rewrite_compare_anchor.py` |
| 关键 env | `DEBUG_RAG=1` |
| 图谱变更点 | 无（行为已在 `10_flow_rag` 隐含，可选增量） |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `pytest tests/test_query_rewrite_compare_anchor.py -q` |
| 结论 | **pass** |
| 要点 | 4 passed；覆盖 `extract_anchor_tokens`、`compare_anchor_tokens` 丢失/保留场景 |

---

## 给 Cursor

`task_05`、`query_compare`、`rewrite`、`DEBUG_RAG`、`compare_anchor_tokens`、`Harness P0-B/C`
