# Payload · W（Multi 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `W` |
| **task_slug** | `query-rewrite-observability` |
| **freeze_id** | `WIKI-CTX-AB-MULTI@2026-05-26` |
| **generated** | 见运行日 · `python tools/wiki_ctx_ab_materialize_w.py` |

## Agent 约束

只能依据下文作答；**禁止** `docs/harness/`、`docs/tasks/done/` 全文、invoke/review。

---

## 载荷正文

--- FILE: docs/coding_wiki/index.md ---
# Coding Wiki · 索引

> 编译层（L2）导航。真值仍以 L0 图谱与 L1 task 为准。Schema：[`CODING_WIKI.md`](CODING_WIKI.md)

---

## 概念（concepts）

| 页 | 说明 |
|----|------|
| [[concepts/llm-wiki-layers]] | L0/L1/L2 与 Harness / 图谱分工 |
| [[concepts/test-strategy-ink-backend]] | 跨 Epic 测试策略指针（非 coverage 真值） |

---

## 决策（decisions · append-only）

| slug | 页 | 说明 |
|------|-----|------|
| `unit-first-test-archive` | [[decisions/2026-05-26-unit-first-test-archive]] | T1c：Wiki 不镜像 pytest 清单 |

---

## 综合（syntheses · 已关账 task）

| slug | 页 | source_task |
|------|-----|-------------|
| `harness-p1-docs-consolidation` | [[syntheses/harness-p1-docs-consolidation]] | `docs/tasks/done/task_harness_p1_docs_consolidation_v1.md` |
| `tech-graph-gate-d-v2-tasks` | [[syntheses/tech-graph-gate-d-v2-tasks]] | `docs/tasks/done/task_engineering_tech_graph_gate_d_v2_tasks_v1.md` |
| `docs-tasks-reorg-move` | [[syntheses/docs-tasks-reorg-move]] | `docs/tasks/done/task_docs_tasks_reorg_move_v1.md` |
| `query-rewrite-observability` | [[syntheses/query-rewrite-observability]] | `docs/tasks/done/task_05_query_rewrite_observability.md` |
| `chatbi-v3-text2sql-tool-latency-obs` | [[syntheses/chatbi-v3-text2sql-tool-latency-obs]] | `docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md` |

---

## 治理与实验

| 文档 | 说明 |
|------|------|
| [`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) | T1b 试点与 Wiki-CTX-AB 顺序 |
| [`docs/harness/experiments/wiki_ctx_ab_v1/`](../harness/experiments/wiki_ctx_ab_v1/README.md) | 两轮对照实验（完整包 / 精简包 / 仅 Wiki） |
| [`WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](WIKI_REQUIREMENTS_COMPARISON_v1_zh.md) | 需求逐项对比（理论 · SPEC · 交付 · 缺口） |

---

## 维护

- 时间线：[`log.md`](log.md)  
- 新增 ingest：先改 `log.md`，再增 syntheses 行于上表

--- FILE: docs/coding_wiki/syntheses/query-rewrite-observability.md ---
---
title: Rewrite 可观测性（query_compare）
slug: query-rewrite-observability
layer: L2
source_task: docs/tasks/done/task_05_query_rewrite_observability.md
freeze_id: task_05_query_rewrite_obs@2026-05-22
closed_date: 2026-05-22
status: compiled
---

# Rewrite 可观测性（query_compare）

## 摘要

在 `POST /api/py/chat` 的 `rag_conversation_logs.metadata.match` 写入 **raw vs rewrite** 对比（命中数、Top1 分、`is_key_entity_lost` / `missing` 锚点 token）。`DEBUG_RAG=1` 时终端一行摘要。**不改变**对外 API 与 RRF 主策略。

## 决策要点

- Keyword 路对 raw/rewrite **各跑一次计数**（仅观测）。  
- `compare_anchor_tokens` 判定关键实体是否在 rewrite 中丢失。  
- 双查询并行融合、前端 UI **另起 task**。

## 失败路径（pointer）

| # | 要点 |
|---|------|
| F1 | Supabase 不可用 → 检索失败；`query_compare` 可能缺失 |
| F2 | Embedding 失败 → keyword-only；对比仍写入 |
| F3 | rewrite 失败 → `rewritten_query=query`；对比仍有效 |

→ L1 全文：`docs/tasks/done/task_05_query_rewrite_observability.md` §失败路径

## 测试变更

| 动作 | 路径 / 说明 |
|------|-------------|
| **新增** | `tests/test_query_rewrite_compare_anchor.py` — 锚点丢失、`task_04`/文件名/日期等 token 场景（4 条用例级；**非** Wiki 维护的清单真值） |
| **验收命令** | `pytest tests/test_query_rewrite_compare_anchor.py -q`（L1 验收）；全仓见 task 自检 `pytest tests -m "not intent_eval and not intent_benchmark"` |
| **未新增** | Supabase 集成 e2e、改 SQL（L1 非范围） |

**图谱**：行为隐含于 → `docs/_tech_graph/10_flow_rag.md`（本 Epic 未改图正文）。

**实现 pointer**：→ `api/index.py`、`api/keyword_fallback.py`、`api/rag_logging.py`（见 L1 实现备忘）。

## 相关

- [[../decisions/2026-05-26-unit-first-test-archive]]  
- [[../concepts/test-strategy-ink-backend]]

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 3395 |
| `file_count` | 2 |
| `notes` | Multi 仅 Wiki：`index.md` + `syntheses/query-rewrite-observability.md` |
