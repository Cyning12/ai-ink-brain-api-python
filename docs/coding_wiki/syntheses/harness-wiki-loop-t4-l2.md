---
title: Wiki Loop T4+L2（第四轮真实业务 Loop）
slug: harness-wiki-loop-t4-l2
layer: L2
source_task: docs/tasks/done/task_harness_wiki_loop_t4_l2_v1.md
freeze_id: WIKI-LOOP-T4-L2@2026-05-27
closed_date: 2026-05-27
status: compiled
---

# Wiki Loop T4+L2 母单

## 摘要

**第四轮** `harness-loop-batch`：编排 **T4 图谱桥接** + **L2 测试 manifest** 三条子 round（R1 Pilot · R2 L0 对齐 · R3 manifest 草案），单 PR 关账 · `WIKI-LOOP-T4-L2@2026-05-27`。

## 子 round（pointer）

| round | 主题 | done task |
|-------|------|-----------|
| R1 | T4 Pilot `graph_nodes` | `task_governance_wiki_t4_r1_pilot_v1` → [[governance-wiki-t4-r1-pilot]] |
| R2 | L0 对齐 | `task_governance_wiki_t4_r2_l0_align_v1` |
| R3 | `_test_manifest` 草案 | → [[governance-l2-r3-test-manifest]] |

## 决策要点

- 母单 **不**直接改业务代码；子 task 各自 Harness 关账。  
- 后续单 task：T4 扩面 · L2 Phase B CI · Agent 读序 · 本批次 ingest。

## 指针（L1）

→ `docs/tasks/done/task_harness_wiki_loop_t4_l2_v1.md`  
→ `docs/harness/invokes/by-task/wiki-loop-t4-l2/`（Loop invoke 索引）
