# Task · 图谱 Sub-graph 死链修复（NIT-1 · 可并行）

> **状态**：`active`（**30 执行中** · **HG-TASK-DRAFT approved**）  
> **schedule_ref**：RECENT **§1.7 并行 NIT**  
> **前置**：#2 `graph-yaml-remove-ai-md` **done**（PR #179）  
> **invoke**：[`graph-yaml-subgraph-nit/`](../harness/invokes/by-task/graph-yaml-subgraph-nit/)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-subgraph-nit` |
| **test_strategy** | `required` |
| **git_branch** | `task/graph-yaml-subgraph-nit` |
| **freeze_id** | `GRAPH-YAML-SUBGRAPH-NIT` |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | **approved** | 30 | #2 merge 后开 |
| **HG-REINSPECT** | pending | done | 40 后 · skip 50 |

---

## 范围

- [x] **D1** 修改 `generate_sub_graph_links()`：Struct/Version 仅链 `.md`（手写 · 无 yaml）
- [x] **D2** 重生成 `00_main.md`
- [x] **D3** `test_00_main_subgraph_no_dead_yaml_href`
- [x] **D4** `--all --check` · verify-tech-graph 全绿

## 非范围

- **不**为 Struct/Version 新建 `.graph.yaml`（非 Epic 范围）
- **不**删 `.ai.md` · **不**跑 G0 扫描

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | `fp-dead-yaml-link` | Sub-graph 仍链不存在的 `.graph.yaml` | pytest 失败 · 修模板 |
| F2 | `fp-00-main-drift` | 重生成后 `--check` 失败 | 修 YAML 或 compile |

---

## 验收标准

- [x] `00_main.md` Sub-graph 无指向不存在文件的 `.graph.yaml` 链
- [x] flow 子图 yaml 链仍正确
- [x] pytest + verify 全绿
- [ ] PR merge · task → `done/`

---

## 实现备忘（30 回填）

| 路径 | 说明 |
| --- | --- |
| `scripts/graph_yaml_compile.py` | `generate_sub_graph_links()` 去死链 |
| `docs/_tech_graph/00_main.md` | 重生成 |
| `tests/test_graph_yaml_compile.py` | `test_00_main_subgraph_no_dead_yaml_href` |

### 自检结论

| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `pytest tests/test_graph_yaml_compile.py -q` | 0 | 12 passed |
| 2 | `bash scripts/verify-tech-graph.sh` | 0 | 全绿 |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-17 | 初稿 · 复查 NIT-1 |
