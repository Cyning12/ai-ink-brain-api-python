# Task · 图谱 YAML · 删除 deprecated `.ai.md`（Post-G0）

> **状态**：`done`（**CLOSE** · PR #179 merged · 2026-06-17）  
> **schedule_ref**：RECENT **§1.7 G0 链 #2**  
> **blocked_by**：[`task_ontology_inventory_scan_g0_v1.md`](../../../docs/harness/tasks/done/harness/task_ontology_inventory_scan_g0_v1.md) · G0 留档 **done**  
> **invoke**：[`invoke_20260617_30_graph-yaml-remove-ai-md.md`](../harness/invokes/by-task/graph-yaml-remove-ai-md/invoke_20260617_30_graph-yaml-remove-ai-md.md)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-remove-ai-md` |
| **test_strategy** | `required` |
| **test_strategy_note** | 删 7 文件 · 须 export/compile/verify 全绿 · pytest 无回归 |
| **audit_profile** | `post_close` |
| **orchestration** | `Claude Code`（30→40 · 50 skip） |
| **git_branch** | `task/graph-yaml-remove-ai-md` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **freeze_id** | `GRAPH-YAML-REMOVE-AI-MD` |
| **epic** | 图谱 YAML 迁移 · G0 后继 |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | **approved** | 30 | G0 关账后开 30 |
| **HG-INVENTORY-ARCHIVED** | **approved** | — | G0 已签 · 2026-06-17 |
| **HG-REINSPECT** | skip | done | 40 后 · skip 50 |

---

## 背景与目标

7× `@deprecated` `.ai.md` 在 export 已改读 YAML 后仅为只读对照。G0 inventory 留档完成后删除，完成 Inform 图源彻底单源。

**完成态**：`docs/_tech_graph/` 下 **0 个** `.ai.md` · CI 全绿。

---

## 范围

- [x] **D1** 删除 7× `.ai.md`
- [x] **D2–D4** 规约 / QNA v1.3 / schema
- [x] **D5** pytest + dual_track_manifest v3
- [x] **D6** RECENT 日志整理
- [x] **D7** verify-tech-graph + pytest 419 passed

## 非范围

- 不改 `graph.json` 拓扑 · 不改 YAML 节点/边
- Sub-graph 死链 → `graph-yaml-subgraph-nit`

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | `fp-g0-not-archived` | 无 HG-INVENTORY-ARCHIVED | STOP · 不得删文件 |
| F2 | `fp-export-regress` | 删后 `export --check` 失败 | 回滚 |
| F3 | `fp-pytest-ai-md` | deprecated 用例仍期望文件存在 | 更新用例 |

---

## 验收标准

- [x] `find docs/_tech_graph -name '*.ai.md' | wc -l` → **0**
- [x] `python tools/tech_graph_graph_export.py --check` → exit 0
- [x] `python scripts/graph_yaml_compile.py --all --check` → exit 0
- [x] `bash scripts/verify-tech-graph.sh` → 全绿
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` → 419 passed
- [x] PR #179 merge · task → `done/`

---

## 实现备忘

| 路径 | 说明 |
| --- | --- |
| `docs/_tech_graph/*.ai.md` | 7 文件已删 |
| `tests/test_graph_yaml_p*_*.py` | 6× `*_ai_md_removed` |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-17 | 初稿 · G0 后继 |
| 2026-06-17 | **CLOSE** · PR #179 merge |
