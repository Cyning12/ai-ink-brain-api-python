# Payload · W（P2 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `W` |
| **task_slug** | `harness-p1-docs-consolidation` |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
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
| `governance-l2-manifest-ci` | [[syntheses/governance-l2-manifest-ci]] | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md` |
| `governance-wiki-t4-expand` | [[syntheses/governance-wiki-t4-expand]] | `docs/tasks/done/task_governance_wiki_t4_expand_v2.md` |
| `governance-l2-r3-test-manifest` | [[syntheses/governance-l2-r3-test-manifest]] | `docs/tasks/done/task_governance_l2_r3_test_manifest_v1.md` |
| `harness-wiki-loop-t4-l2` | [[syntheses/harness-wiki-loop-t4-l2]] | `docs/tasks/done/task_harness_wiki_loop_t4_l2_v1.md` |
| `wiki-ctx-ab-v1` | [[syntheses/wiki-ctx-ab-v1]] | `docs/tasks/done/task_wiki_ctx_ab_v1.md` |
| `coding-wiki-pilot` | [[syntheses/coding-wiki-pilot]] | `docs/tasks/done/task_coding_wiki_pilot_v1.md` |
| `chatbi-v3-p2-health-ready` | [[syntheses/chatbi-v3-p2-health-ready]] | `docs/tasks/done/task_chatbi_v3_p2_resilience_health_ready_v1.md` |
| `harness-wiki-loop-c2-verify` | [[syntheses/harness-wiki-loop-c2-verify]] | `docs/tasks/done/task_harness_wiki_loop_c2_verify_v1.md` |
| `governance-wiki-t4-r1-pilot` | [[syntheses/governance-wiki-t4-r1-pilot]] | `docs/tasks/done/task_governance_wiki_t4_r1_pilot_v1.md` |
| `wiki-ctx-ab-multi-slug` | [[syntheses/wiki-ctx-ab-multi-slug]] | `docs/tasks/done/task_wiki_ctx_ab_multi_slug_v1.md` |

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

--- FILE: docs/coding_wiki/syntheses/harness-p1-docs-consolidation.md ---
---
title: Harness P1 文档巩固（P1-3 + P1-2）
slug: harness-p1-docs-consolidation
layer: L2
source_task: docs/tasks/done/task_harness_p1_docs_consolidation_v1.md
freeze_id: HARNESS-P1-DOCS@2026-05-23
closed_date: 2026-05-23
status: compiled
---

# Harness P1 文档巩固

## 摘要

单 PR 完成两项文档治理：**P1-3** 在 `docs/tasks/README.md` 增加 `human_gate` 五列速查；**P1-2** 新建 `docs/tasks/skills/README.md` 定义 6 类 SKILL 与关账蒸馏口径。纯文档，`test_strategy: not_applicable`。

## 决策与验收要点

- 执行顺序硬约束：**先 P1-3 后 P1-2**。  
- 与 diary §九 / HARNESS_V2 §5 无 SKILL 类型冲突（task 内「矛盾单列」已记录）。  
- 非范围：未改 `api/`、CI、工作区 reviews pointer（P1-1 另 task）。

## 指针（L1 真值）

- Task：→ `docs/tasks/done/task_harness_p1_docs_consolidation_v1.md`  
- 排期：→ `docs/tasks/RECENT_TASK_SCHEDULE.md` §0.4  
- Wiki-CTX-AB gold slug：**本页 slug** 用于 P1/P2 实验对照

## 相关

- [[docs-tasks-reorg-move]]（tasks 目录结构前提）  
- [[../concepts/llm-wiki-layers]]

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 4042 |
| `file_count` | 2 |
| `notes` | P2 仅 Wiki：`index.md` + `syntheses/harness-p1-docs-consolidation.md` |
