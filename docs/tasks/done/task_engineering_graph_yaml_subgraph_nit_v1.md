# Task · 图谱 Sub-graph 死链修复（NIT-1 · 可并行）

> **状态**：`done`（**CLOSE** · PR #180 merged · 2026-06-17）  
> **schedule_ref**：RECENT **§1.7 并行 NIT**  
> **前置**：#2 `graph-yaml-remove-ai-md` **done**（PR #179）  
> **invoke**：[`invoke_20260617_30_graph-yaml-subgraph-nit.md`](../harness/invokes/by-task/graph-yaml-subgraph-nit/invoke_20260617_30_graph-yaml-subgraph-nit.md)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-subgraph-nit` |
| **test_strategy** | `required` |
| **test_strategy_note** | 改 compile 模板 + 重生成 00_main + pytest 锁链有效性 |
| **audit_profile** | `post_close` |
| **orchestration** | `Claude Code`（30→40 · 50 skip） |
| **git_branch** | `task/graph-yaml-subgraph-nit` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **freeze_id** | `GRAPH-YAML-SUBGRAPH-NIT` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | **approved** | 30 | 2026-06-17 |
| **HG-REINSPECT** | skip | done | 40 PASS · skip 50 |

---

## 背景与目标

Inform P0 将 Sub-graph 链改为「编辑源 `*.graph.yaml`」，但 `01_struct` / `02_version` 无对应 `.graph.yaml`，导致 `00_main.md` 死链。

**完成态**：Struct/Version 不链向不存在的 yaml；7 张 flow 仍链正确 yaml。

---

## 范围

- [x] **D1** `generate_sub_graph_links()`：Struct/Version 仅链 `.md`（手写 · 无 yaml）
- [x] **D2** 重生成 `00_main.md`
- [x] **D3** `test_00_main_subgraph_no_dead_yaml_href`
- [x] **D4** verify-tech-graph 全绿

## 非范围

- 不为 Struct/Version 新建 `.graph.yaml`

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | `fp-dead-yaml-link` | Sub-graph 仍链不存在的 `.graph.yaml` | pytest 失败 · 修模板 |
| F2 | `fp-00-main-drift` | 重生成后 `--check` 失败 | 修 YAML 或 compile |

---

## 验收标准

- [x] `00_main.md` Sub-graph 无死 `.graph.yaml` 链
- [x] flow 子图 yaml 链仍正确
- [x] `pytest tests/test_graph_yaml_compile.py` + verify 全绿
- [x] PR #180 merge · task → `done/`

---

## 实现备忘

| 路径 | 说明 |
| --- | --- |
| `scripts/graph_yaml_compile.py` | `generate_sub_graph_links()` |
| `docs/_tech_graph/00_main.md` | 重生成 |
| `tests/test_graph_yaml_compile.py` | `test_00_main_subgraph_no_dead_yaml_href` |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-17 | 初稿 · NIT-1 |
| 2026-06-17 | **CLOSE** · PR #180 merge |
