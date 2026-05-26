---
title: Rewrite 可观测性（query_compare）
slug: query-rewrite-observability
layer: L2
source_task: docs/tasks/done/task_05_query_rewrite_observability.md
freeze_id: task_05_query_rewrite_obs@2026-05-22
closed_date: 2026-05-22
status: compiled
test_strategy: recommended
---

# Rewrite 可观测性（query_compare）

## 摘要

在 `POST /api/py/chat` 的 `rag_conversation_logs.metadata.match` 写入 **raw vs rewrite** 对比（命中数、Top1 分、`is_key_entity_lost` / `missing` 锚点 token）。`DEBUG_RAG=1` 时终端一行摘要。**不改变**对外 API 与 RRF 主策略。L1 **`test_strategy: recommended`**（与 `source_task` 一致）；跨 Epic 读序见 [[../concepts/test-strategy-ink-backend]]。

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

**Harness `test_strategy`**：`recommended` — 关账前须有可失败单测（见下表）；与 L1 task 头字段一致，**非** Wiki 第二真值。

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
