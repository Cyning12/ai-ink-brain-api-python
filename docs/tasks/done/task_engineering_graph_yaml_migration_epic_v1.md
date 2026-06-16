# Epic：图谱 YAML 图源迁移

> **状态**：done
> **关联**：`docs/_tech_graph/*.graph.yaml` 全量图源迁移
> **Issue/PR**：PR #166～#171

---

## 背景与目标

以 P0 `00_main` YAML 图源试点成功为基础，将剩余 6 个 graph 的 `.ai.md` 双轨维护模式迁为 `.graph.yaml` 单一编辑源，统一由 `scripts/graph_yaml_compile.py` 生成人类可读版 `.md`。

---

## 子任务（全部完成）

| 阶段 | Graph | PR | Task 文件 |
|------|-------|-----|-----------|
| P0 | `00_main` | #163 / #164 | `docs/tasks/done/task_engineering_graph_yaml_p0_00_main_v1.md` |
| P1 | `10_flow_rag` | #166 | `docs/tasks/done/task_engineering_graph_yaml_p1_10_flow_rag_v1.md` |
| P2 | `11_flow_text2sql` | #167 | `docs/tasks/done/task_engineering_graph_yaml_p2_11_flow_text2sql_v1.md` |
| P3a | `12_flow_fts` | #168 | `docs/tasks/done/task_engineering_graph_yaml_p3a_12_flow_fts_v1.md` |
| P3b | `13_flow_supabase_rpc` | #169 | `docs/tasks/done/task_engineering_graph_yaml_p3b_13_flow_supabase_rpc_v1.md` |
| P4 | `14_runtime_observability` | #170 | `docs/tasks/done/task_engineering_graph_yaml_p4_14_runtime_observability_v1.md` |
| P5 | `15_e2e_boundary` | #171 | `docs/tasks/done/task_engineering_graph_yaml_p5_15_e2e_boundary_v1.md` |

---

## 公共工具改造

- `scripts/graph_yaml_compile.py`：P1 完成 `--graph-id` / `--all` / `--check` / `--output` 参数化
- `scripts/graph_yaml_compile.py`：P2 新增 `notes` 字段渲染，用于保留历史 `.md` 中的运维入口/env 字面量等文档覆盖

---

## 验收标准（全部达成）

- [x] 7 个 graph 均有 `.graph.yaml` 唯一编辑源
- [x] 7 个 `.md` 均由脚本生成
- [x] 7 个 `.ai.md` 顶部含 `@deprecated · 源迁 YAML`
- [x] 每个子流程新增 ≥9 用例 pytest，全部通过
- [x] 每个 PR 上 `pytest` / `tech-graph` / `verify-fast` 全绿
- [x] `graph.json` 切片与 YAML 节点/边/锚点完全一致

---

## 残余风险

- 无

---

## 给 Cursor

`graph-yaml-migration-epic`、`test_strategy: required`、`semi_auto: false`、`human_gate`、`audit_profile: post_close`、`Harness`、`RECENT_TASK_SCHEDULE`
