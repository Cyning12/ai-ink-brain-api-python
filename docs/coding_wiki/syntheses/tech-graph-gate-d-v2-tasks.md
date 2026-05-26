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
