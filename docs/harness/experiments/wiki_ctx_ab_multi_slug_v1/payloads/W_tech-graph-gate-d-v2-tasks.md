# Payload · W（Multi 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `W` |
| **task_slug** | `tech-graph-gate-d-v2-tasks` |
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

--- FILE: docs/coding_wiki/syntheses/tech-graph-gate-d-v2-tasks.md ---
---
title: 闸口 D — graph_query v2 五题扩域
slug: tech-graph-gate-d-v2-tasks
layer: L2
source_task: docs/tasks/done/task_engineering_tech_graph_gate_d_v2_tasks_v1.md
freeze_id: TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0
closed_date: 2026-05-21
status: compiled
---

# 闸口 D — v2 题集扩域

## 摘要

在 C/C′/C″ 已 **accepted** 前提下，将 `gate_ctx_ab` 题集从 v1 三题扩至 **v2 五题**（+T004 ChatBI/Text2SQL、+T005 Intent/路由）。**维持** `CTX_V2_QUERY` / `graph_query` 为 machine 默认；沿用 C″ 分题物化策略。`test_strategy: required`，关账 PR #41。

## 架构决议（摘录）

- **禁止** 升 `CTX_DUAL_MD` 为默认；禁止覆盖 C 系 accepted 结论文。  
- T004 物化对齐 T002（contract + manifest + impact）；T005 对齐 intent 子图种子。  
- 结论文：→ `docs/diary/jsonPKmermaid/reports/conclusion_gate_d_ctx_v2_tasks_v1_zh.md`（实验轨，按需打开）

## 指针（L1 真值）

- Task：→ `docs/tasks/done/task_engineering_tech_graph_gate_d_v2_tasks_v1.md`  
- 50 复检：→ `docs/harness/reviews/task_engineering_tech_graph_gate_d_v2_tasks_v1_reinspect_R1_20260521.md`（历史路径；新审查看 `by-task/`）  
- 方法论：治理仓 `AGENT_GRAPH_CONSUMPTION` §6.1

## 相关

- 图谱消费默认：**graph_query**，非整包 `graph.json`  
- [[../concepts/llm-wiki-layers]]

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 2978 |
| `file_count` | 2 |
| `notes` | Multi 仅 Wiki：`index.md` + `syntheses/tech-graph-gate-d-v2-tasks.md` |
