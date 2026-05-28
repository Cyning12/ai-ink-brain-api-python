---
title: Coding Wiki A1 — synthesis test_strategy 补全
slug: coding-wiki-ingest-test-strategy
layer: L2
source_task: docs/tasks/done/task_coding_wiki_ingest_test_strategy_v1.md
freeze_id: CODING-WIKI-A1-TEST-STRATEGY@2026-05-26
closed_date: 2026-05-26
status: compiled
graph_nodes: []
---

# Coding Wiki A1 — test_strategy 补全

## 摘要

Wiki Loop A1–A4 **A1** round：为首批 ingest 的 syntheses 补全 `test_strategy` 元数据（`required` / `recommended` / `not_applicable`），使 CODING_WIKI schema 完整；纯 docs 元数据补洞。

## 决策要点

- `test_strategy` 须与 source task 一致；不一致时以 task 为准。
- 不新增 pytest、不改 `api/`。
- 为后续 Batch ingest 提供 schema 校验样板。

## 指针（L1）

→ `docs/tasks/done/task_coding_wiki_ingest_test_strategy_v1.md`
→ `docs/coding_wiki/CODING_WIKI.md`
