# Task · 图谱 Sub-graph 死链修复（NIT-1 · 可并行）

> **状态**：`active`（**HG-TASK-DRAFT pending** · **与 G0 链并行** · 建议先于删 `.ai.md` merge）  
> **schedule_ref**：RECENT **§1.7 并行 NIT**  
> **前置**：Inform 闭环 **done** · 复查 NIT-1（2026-06-17）  
> **invoke**：（30 启动时创建 `docs/harness/invokes/by-task/graph-yaml-subgraph-nit/`）

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

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | pending | 30 | 范围人签 |
| **HG-REINSPECT** | pending | done | 40 后 · skip 50 |

---

## 背景与目标

Inform P0 将 Sub-graph 链改为「编辑源 `*.graph.yaml`」，但 **`01_struct` / `02_version` 无对应 `.graph.yaml`**（Epic 仅迁移 7 张 flow + `00_main`），导致 `00_main.md` 存在 **死链**。

**完成态**：Sub-graph 中 Struct/Version **不链向不存在的 yaml**；7 张 flow 仍链正确 yaml；pytest 防回归。

---

## 范围

- [ ] **D1** 修改 `generate_sub_graph_links()`：
  - `01_struct` / `02_version`：仅链 `.md`，**或** 标注「手写 · 无 `.graph.yaml`」（二选一 · 30 选最小 diff）
  - 7 张 flow：保持「编辑源 `*.graph.yaml`」
- [ ] **D2** `python scripts/graph_yaml_compile.py --graph-id 00_main` 重生成 `00_main.md`
- [ ] **D3** `tests/test_graph_yaml_compile.py` 扩展：`test_00_main_subgraph_no_dead_yaml_href`（Struct/Version 不指向不存在的 `.graph.yaml`）
- [ ] **D4** `--all --check` · verify-tech-graph 全绿

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

- [ ] `00_main.md` Sub-graph 无指向不存在文件的 `.graph.yaml` 链
- [ ] flow 子图 yaml 链仍正确
- [ ] pytest + verify 全绿
- [ ] PR merge · task → `done/`

---

## 实现备忘（30 回填）

| 路径 | 说明 |
| --- | --- |
| | （30 回填） |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-17 | 初稿 · 复查 NIT-1 |
