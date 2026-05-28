---
title: L2 _test_manifest 草案（Loop R3）
slug: governance-l2-r3-test-manifest
layer: L2
source_task: docs/tasks/done/task_governance_l2_r3_test_manifest_v1.md
freeze_id: GOV-L2-R3-TEST-MANIFEST@2026-05-27
closed_date: 2026-05-27
status: compiled
graph_nodes:
  - id: E2E_DOC
    relation: documents
---

# L2 _test_manifest 草案（R3）

## 摘要

Wiki Loop **T4+L2** 实例 4 的 **R3** 子 round：落盘 `_test_manifest.json` **v1 草案**（6 entries · Phase A），定义 ERR 码与 `tests/` glob 映射骨架；**不**阻塞 merge（Phase B → [[governance-l2-manifest-ci]]）。

## 决策要点

- Phase A：**不**接入 Required CI（与 Phase B 区分）。  
- 条目须 Epic 前缀稳定 id · `test_paths` 仅 `tests/` 下 glob。  
- 叙事 pointer 至 L1 `failure_paths` 与 L0 `ERR_*` 节点。

## 指针（L1）

→ `docs/tasks/done/task_governance_l2_r3_test_manifest_v1.md`  
→ `docs/_tech_graph/_test_manifest.json`  
→ 母单 [[syntheses/harness-wiki-loop-t4-l2]]（`task_harness_wiki_loop_t4_l2_v1`）
