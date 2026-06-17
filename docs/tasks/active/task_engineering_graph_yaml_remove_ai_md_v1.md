# Task · 图谱 YAML · 删除 deprecated `.ai.md`（Post-G0）

> **状态**：`active`（**30 执行中** · 串行链 **#2/3** · **可开 30**）  
> **schedule_ref**：RECENT **§1.7 G0 链 #2**  
> **blocked_by**：~~G0 留档~~ **done** · [`task_ontology_inventory_scan_g0_v1.md`](../../../docs/harness/tasks/done/harness/task_ontology_inventory_scan_g0_v1.md)  
> **前置 Inform**：[`task_engineering_graph_yaml_export_from_yaml_p1_v1.md`](../done/task_engineering_graph_yaml_export_from_yaml_p1_v1.md) · **done**  
> **invoke**：（30 执行中）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-remove-ai-md` |
| **test_strategy** | `required` |
| **git_branch** | `task/graph-yaml-remove-ai-md` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **freeze_id** | `GRAPH-YAML-REMOVE-AI-MD` |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | **approved** | 30 | G0 关账后开 30 |
| **HG-INVENTORY-ARCHIVED** | **approved** | — | G0 已签 · 2026-06-17 |
| **HG-REINSPECT** | pending | done | 40 后 · skip 50 |

### 开 30 硬闸门（四项齐备 · 缺一 STOP）

| # | 条件 |
| --- | --- |
| 1 | [`task_ontology_inventory_scan_g0_v1.md`](../../../docs/harness/tasks/active/task_ontology_inventory_scan_g0_v1.md) → **`docs/harness/tasks/done/`** |
| 2 | **HG-INVENTORY-ARCHIVED** signed（G0 task 元信息表） |
| 3 | inventory YAML 已在 **`main`**（cyning-harness 或约定路径） |
| 4 | G0 扫描 PR **CI 全绿且已 merge** |

---

## 背景与目标

7× `@deprecated` `.ai.md` 在 export 已改读 YAML 后仅为只读对照。G0 inventory 留档完成后，删除这些文件以完成 **Inform 图源彻底单源**，并消除维护者「双轨仍在」的歧义。

**完成态**：`docs/_tech_graph/` 下 **0 个** `.ai.md` · CI 全绿 · QNA/规约无「仍须维护 ai 轨」表述。

---

## 范围

- [x] **D1** 删除 7 个文件：`00_main.ai.md` … `15_e2e_boundary.ai.md`
- [x] **D2** 全仓 `rg '\.ai\.md' docs/_tech_graph`：规约/QNA 已更新 · 历史 Q&A 节保留
- [x] **D3** 更新 `QNA_graph_wiki_history_upgrade_v1_zh.md`：修订 **v1.3**
- [x] **D4** 更新 `99_spec.md` / `99_mermaid_protocol.md` / `graph_v2_schema.md`
- [x] **D5** pytest `*_ai_md_deprecated` → `*_ai_md_removed` · `dual_track_manifest.json` v3
- [x] **D6** 清理 `RECENT_TASK_SCHEDULE.md` §1.6/§1.7 过时「待 merge」行
- [x] **D7** `bash scripts/verify-tech-graph.sh` + pytest **419 passed**

## 非范围

- **不**改 `graph.json` 拓扑（export `--check` 须仍过）
- **不**改 YAML 节点/边
- **不**做 `external_ref` schema（→ 另 task · backlog）
- **不**改 Sub-graph Struct/Version 死链（→ [`task_engineering_graph_yaml_subgraph_nit_v1.md`](./task_engineering_graph_yaml_subgraph_nit_v1.md) · 建议先 merge）

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | `fp-g0-not-archived` | 无 HG-INVENTORY-ARCHIVED | STOP · 不得删文件 |
| F2 | `fp-export-regress` | 删后 `export --check` 失败 | 回滚 · 查 hidden ai 依赖 |
| F3 | `fp-pytest-ai-md` | deprecated 用例仍期望文件存在 | 更新/删除用例 |

---

## 验收标准

- [x] `find docs/_tech_graph -name '*.ai.md' | wc -l` → **0**
- [x] `python tools/tech_graph_graph_export.py --check` → exit 0
- [x] `python scripts/graph_yaml_compile.py --all --check` → exit 0
- [x] `bash scripts/verify-tech-graph.sh` → 全绿
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` → 419 passed
- [x] QNA v1.3 · RECENT 日志已整理
- [ ] PR **CI 全绿 + merge** · task → `done/`

---

## 依赖与引用

| 依赖项 | 路径 |
| --- | --- |
| G0 扫描 | `docs/harness/tasks/done/task_ontology_inventory_scan_g0_v1.md` |
| inventory | `cyning-harness/docs/methodology/graph/inventory/ONTOLOGY_INVENTORY_*.yaml` |
| export | `tools/tech_graph_graph_export.py` · `tech_graph_graph_v2_yaml.py` |

---

## 实现备忘（30 回填）

| 路径 | 说明 |
| --- | --- |
| `docs/_tech_graph/*.ai.md` | 7 文件已删 |
| `docs/_tech_graph/99_mermaid_protocol.md` | 双轨改 YAML→md→graph.json |
| `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` | v1.3 |
| `docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/dual_track_manifest.json` | v3 · yaml 轨 |
| `tests/test_graph_yaml_p*_*.py` | 6× `*_ai_md_removed` |

### 自检结论

| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `find docs/_tech_graph -name '*.ai.md' \| wc -l` | 0 | 0 |
| 2 | `bash scripts/verify-tech-graph.sh` | 0 | 全绿 |
| 3 | `pytest tests -m "not intent_eval and not intent_benchmark"` | 0 | 419 passed |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-17 | 初稿 · G0 留档后继 · 删 7× ai.md |
