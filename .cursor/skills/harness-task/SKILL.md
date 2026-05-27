---
name: harness-task
description: >-
  Single Harness task hat chain (22→30→40→50→close): invoke paths, semi_auto,
  HANDOFF rules, test_strategy vs 50. Use for one active task in docs/tasks/active/.
  Not for Loop batch (multi subtask, HG-LOOP-BATCH, LOOP_MANIFEST).
disable-model-invocation: true
---

# Harness 单 task 帽链（22 → 关账）

> **便携真值**：[`docs/tasks/skills/SKILL-harness-task.md`](../../../docs/tasks/skills/SKILL-harness-task.md)（**v1 草案**）

## 何时使用

- **一个** `docs/tasks/active/task_*.md` · `semi_auto: true`
- 22→30→40→50→关账 · invoke / review / reinspect 落盘
- 改 Harness prompts/rules（`audit_profile: full`）

## 硬约束

1. **Loop 勿用本文** — 多 round 见 [`harness-loop-batch`](../harness-loop-batch/SKILL.md)
2. 每帽：**invoke §3 全文 + commit**（[`HANDOFF_AUTO_COMMIT`](../../../docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md)）
3. 关账：`git mv` + `_views/done.md` **同一 commit**；PR 前跑 [`docs-governance`](../docs-governance/SKILL.md) H1–H5
4. **关账前 ST1–ST6**（真值见便携 SKILL §ST1–ST6）：22/30/40/50/CLOSE + RECENT + hygiene
5. **禁止跳帽**：未 invoke+commit 不得进下一帽
6. **非 Cursor**：须显式 `@` 模板路径（无 `.mdc` 自动加载）

## 落盘速查

| 帽 | 路径 |
|----|------|
| invoke | `docs/harness/invokes/by-task/<task_slug>/invoke_*_{22,30,40,50,CLOSE}_*.md` |
| 22 | `docs/harness/reviews/by-task/<task_slug>/` |
| 50 | `docs/tasks/reinspect_results/reinspect_<task_slug>_*.md` |

## 状态

SKILL **`draft`** — 2026-05-27 通则整理
