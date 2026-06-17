# Task · 图谱 YAML · 删除 deprecated `.ai.md`（Post-G0）

> **状态**：`active`（**HG-TASK-DRAFT pending** · 串行链 **#2/3** · **blocked_by G0 留档**）  
> **schedule_ref**：RECENT **§1.7 G0 链 #2**  
> **blocked_by**：[`task_ontology_inventory_scan_g0_v1.md`](../../../docs/harness/tasks/active/task_ontology_inventory_scan_g0_v1.md) · **HG-INVENTORY-ARCHIVED signed** + inventory **已 merge 留档**  
> **前置 Inform**：[`task_engineering_graph_yaml_export_from_yaml_p1_v1.md`](../done/task_engineering_graph_yaml_export_from_yaml_p1_v1.md) · **done**  
> **invoke**：（30 启动时创建 `docs/harness/invokes/by-task/graph-yaml-remove-ai-md/`）

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
| **HG-TASK-DRAFT** | pending | 30 | 范围与非范围人签 |
| **HG-INVENTORY-ARCHIVED** | pending | 30 | **须 G0 task 已签** · inventory 已留档 |
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

- [ ] **D1** 删除 7 个文件：`00_main.ai.md` … `15_e2e_boundary.ai.md`
- [ ] **D2** 全仓 `rg '\.ai\.md' docs/_tech_graph`：除 QNA **历史讨论节**外，无「编辑源 / 机器轨 = ai.md」类表述 · 必要处改 pointer 到 `.graph.yaml` / `.md`
- [ ] **D3** 更新 `QNA_graph_wiki_history_upgrade_v1_zh.md`：修订 **v1.3**（P1 export YAML 单源 · `.ai.md` 已物理删除 · 历史节保留）
- [ ] **D4** 更新 `99_spec.md` / `99_mermaid_protocol.md` / `graph_v2_schema.md`（若仍提 ai 轨为并存编辑源）
- [ ] **D5** 移除或更新仍引用 `.ai.md` 的 pytest（如 `test_*_ai_md_deprecated`）→ 改为「文件不存在」或删用例
- [ ] **D6** 清理 `RECENT_TASK_SCHEDULE.md` §1.6 续 变更日志中 **「待 merge」** 过时行（与 Inform/G0 链一致）
- [ ] **D7** `bash scripts/verify-tech-graph.sh` + 全量 pytest 绿

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

- [ ] `find docs/_tech_graph -name '*.ai.md' | wc -l` → **0**
- [ ] `python tools/tech_graph_graph_export.py --check` → exit 0
- [ ] `python scripts/graph_yaml_compile.py --all --check` → exit 0
- [ ] `bash scripts/verify-tech-graph.sh` → 全绿
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` → 全绿
- [ ] QNA v1.3 · RECENT 日志已整理
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
| | （30 回填） |

### 自检结论

| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| | | | |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-17 | 初稿 · G0 留档后继 · 删 7× ai.md |
