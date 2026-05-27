# Payload · W（P2 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `W` |
| **task_slug** | `wiki-ctx-ab-v1` |
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

--- FILE: docs/coding_wiki/syntheses/wiki-ctx-ab-v1.md ---
---
title: Wiki-CTX-AB（P1→P2 上下文对照）
slug: wiki-ctx-ab-v1
layer: L2
source_task: docs/tasks/done/task_wiki_ctx_ab_v1.md
freeze_id: WIKI-CTX-AB@2026-05-25
closed_date: 2026-05-26
status: compiled
---

# Wiki-CTX-AB v1

## 摘要

对照 **H-lean**（Harness+task 精简包）与 **W**（仅 `coding_wiki/`）在同一 gold slug 上的载荷效率与正确性。P1 推荐 T3 taxonomy；**P2 accepted**：W 相对 H-lean **-78.8%** 字符、**4/4** 正确性不降。

## 决策要点（P2 签收）

- **推荐默认读序**：关账回顾先 `index` + `syntheses`（→ Agent 读序 task 常模化）。  
- **禁止** W 臂为答题回读全量 `invokes/` / done task 全文。  
- Gold slug：`harness-p1-docs-consolidation`（与 T1b 同页）。

## 指针（L1 · 实验轨）

→ `docs/tasks/done/task_wiki_ctx_ab_v1.md`  
→ `docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md`  
→ [[syntheses/harness-p1-docs-consolidation]]

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 3902 |
| `file_count` | 2 |
| `notes` | P2 仅 Wiki：`index.md` + `syntheses/wiki-ctx-ab-v1.md` |
