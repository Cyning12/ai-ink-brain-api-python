# Epic：图谱 YAML 图源迁移

> **状态**：done
> **关联**：`docs/_tech_graph/*.graph.yaml` 全量图源迁移
> **Issue/PR**：PR #166～#171

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` |
| **freeze_id** | `GRAPH-YAML-P0@786e32d` |
| **semi_auto** | `false` |
| **orchestration** | `Claude Code` |
| **chain_prompt** | `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_graph-yaml-epic-closeout_zh.md`（按需创建） |
| **audit_profile** | `post_close` |
| **git_branch** | `task/graph-yaml-epic-closeout` |
| **experience_capture** | `required` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | signed | 22-R1,30 | Epic 关账范围与验收标准人扫 |
| HG-AUDIT-R1 | signed | 30 | 22 R1 落盘 `docs/harness/reviews/` 后人签 |
| HG-REINSPECT | signed | done | 50 复检后人签、合并 PR 前 |

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

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 | 测试 |
|---|-------------|----------|----------|--------|----------|------|
| F1 | `fp-epic-meta-missing` | Epic task 文件未填写 Harness 元信息 | `task_validate` 报错 | 否 | CI `tech-graph` 失败 | `tools/harness_task_validate.py` |
| F2 | `fp-epic-view-stale` | `done.md` / `done_by_domain.md` 未同步关账 | 索引与 done 目录不一致 | 否 | PR review 不通过 | 人工检查 |

---

## 验收标准

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
