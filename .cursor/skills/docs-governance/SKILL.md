---
name: docs-governance
description: >-
  Docs and governance task prefill plus post-close hygiene (H1–H6): reinspect
  naming, _views/done.md, RECENT §6.6/§8, cross-refs. Use for pure docs tasks,
  Loop round docs delivery, or PR-before hygiene after task close. Not for api/
  or Loop batch orchestration.
disable-model-invocation: true
---

# Docs / 治理文档（预填 + 关账 hygiene）

> **便携真值**：[`docs/tasks/skills/SKILL-docs-governance.md`](../../../docs/tasks/skills/SKILL-docs-governance.md)（**v1 草案**）

## 何时使用

- 纯 docs / 治理 task（`test_strategy: not_applicable`）
- Loop 子 round 或单 task **关账后、开 PR 前** 索引 hygiene
- reinspect 命名、`_views/done.md`、`RECENT_TASK_SCHEDULE` 同步

## 硬约束

1. **H1**：`reinspect_{task_slug}_YYYYMMDD_vN.md` — **禁止** `reinspec_` typo
2. **H2–H5**：`_views`、RECENT §8/§6.6、交叉引用与 rename 一致
3. **H6**：SPEC `draft`→`active` **仅人审**
4. **非范围**：`api/`、`tests/`、手改 `graph.json`

## 与相邻 SKILL

| SKILL | 关系 |
|-------|------|
| [`harness-task`](../harness-task/SKILL.md) | 单 task 帽链 + 关账 checklist |
| [`harness-loop-batch`](../harness-loop-batch/SKILL.md) | Loop META 后 + `REPORT_completion_*` |

## 状态

SKILL **`draft`** — 蒸馏来源 Wiki Loop T4+L2 N1–N4（2026-05-27）
