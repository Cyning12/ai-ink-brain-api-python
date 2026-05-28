---
title: docs/tasks 目录规整（INK-P6）
slug: docs-tasks-reorg-move
layer: L2
source_task: docs/tasks/done/task_docs_tasks_reorg_move_v1.md
closed_date: 2026-05-22
status: compiled
graph_nodes: []
---

# docs/tasks 目录规整

## 摘要

在 **不改正文语义** 前提下，将 `docs/tasks/` 按类型/状态 `git mv` 至 `active/`、`done/`、`specs/`、`templates/`、`legacy/`，并更新 `docs/README.md` 与 `_views/` 索引。仅文档，不涉及 `_tech_graph/` 与代码。

## 规则摘要

| 类型 | 目标 |
|------|------|
| `task_*.md` + 状态 done | `done/` |
| draft/design/pending/in_progress | `active/` |
| `SPEC-*.md` | `specs/` |
| 历史命名 / 无状态 | `legacy/` |

## 指针（L1 真值）

- Task：→ `docs/tasks/done/task_docs_tasks_reorg_move_v1.md`  
- 导航入口：→ `docs/tasks/_views/`

## 相关

- [[harness-p1-docs-consolidation]]（P1 文档依赖稳定 paths）  
- [[../concepts/llm-wiki-layers]]
