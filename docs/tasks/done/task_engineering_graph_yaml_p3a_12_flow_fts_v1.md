# Task：图谱 YAML 图源迁移 P3a — `12_flow_fts`

> **状态**：done
> **关联图谱**：`docs/_tech_graph/12_flow_fts.md`
> **关联 Issue/PR**：承接 Epic `task_engineering_graph_yaml_migration_epic_v1.md` · PR #168
> **前端依赖**：无

> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/*.md` 索引。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**；链式常模：[`docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md`](../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md) + [`docs/harness/prompts/PROMPT_*_chain_serial_*`](../harness/prompts/README.md)。**`semi_auto` 已 deprecated**（历史见 [`HANDOFF_SEMI_AUTO.md`](../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)）。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` |
| **freeze_id** | `GRAPH-YAML-P0@786e32d` |
| **semi_auto** | `false` |
| **orchestration** | `Claude Code` |
| **chain_prompt** | `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_graph-yaml-p3a-12-flow-fts_zh.md`（按需创建） |
| **audit_profile** | `post_close` |
| **git_branch** | `task/graph-yaml-p3a-12-flow-fts` |
| **experience_capture** | `required` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | signed | 22-R1,30 | P3a 范围与验收标准人扫 |
| HG-AUDIT-R1 | signed | 30 | 22 R1 落盘 `docs/harness/reviews/` 后人签 |
| HG-REINSPECT | signed | done | 50 复检后人签、合并 PR 前 |

---

## 背景与目标

Epic `task_engineering_graph_yaml_migration_epic_v1.md` 将 `00_main` 的 YAML 图源模式推广到剩余 6 个 graph。P3a 负责 `12_flow_fts` 子流程。

完成态：

- `docs/_tech_graph/12_flow_fts.graph.yaml` 成为 `12_flow_fts` 唯一编辑源
- `docs/_tech_graph/12_flow_fts.md` 由脚本生成
- `docs/_tech_graph/12_flow_fts.ai.md` 顶部加 `@deprecated · 源迁 YAML`
- `tests/test_graph_yaml_p3a_12_flow_fts.py` 覆盖 YAML 解析、节点/边/锚点与 `graph.json` 一致、`--check` 模式

---

## 范围

- [x] 复用 P1/P2 后的 `scripts/graph_yaml_compile.py`（`--graph-id` / `--all` / `--check` / `notes`）
- [x] 创建 `docs/_tech_graph/12_flow_fts.graph.yaml`（以 `.ai.md` 为真值源，对齐 `graph.json` 切片）
- [x] 生成 `docs/_tech_graph/12_flow_fts.md`
- [x] 标记 `docs/_tech_graph/12_flow_fts.ai.md` 为 `@deprecated · 源迁 YAML`
- [x] 新增 `tests/test_graph_yaml_p3a_12_flow_fts.py`
- [x] 回测 `00_main`：确保 `--check --graph-id 00_main` 仍 exit 0
- [x] PR 合并到 `main`

## 非范围

- 不迁移其他 graph（Epic 中 P3b～P5 负责）
- 不修改 `graph.json`
- 不删除 `.ai.md`
- 不引入 `.cyning-harness/`

---

## 行为变更（Delta）

### ADDED

- **Requirement**：`12_flow_fts.graph.yaml` 成为 `12_flow_fts` 唯一编辑源
  - **Scenario**：GIVEN 维护者修改 FTS 子流程拓扑 WHEN 编辑 `12_flow_fts.graph.yaml` THEN 运行脚本可重新生成 `12_flow_fts.md` 且 diff 校验通过

### MODIFIED

- **Requirement**：`12_flow_fts.md` 由手写改为脚本生成（Previously：手写维护）
- **Requirement**：`12_flow_fts.ai.md` 顶部增加 deprecation 注释（Previously：无）

### REMOVED

- 无

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| **Epic 母单** | `docs/tasks/active/task_engineering_graph_yaml_migration_epic_v1.md` |
| **P0 试点** | `docs/tasks/done/task_engineering_graph_yaml_p0_00_main_v1.md` |
| **P1 先行** | `docs/tasks/done/task_engineering_graph_yaml_p1_10_flow_rag_v1.md` |
| **P2 先行** | `docs/tasks/done/task_engineering_graph_yaml_p2_11_flow_text2sql_v1.md` |
| **编译脚本** | `scripts/graph_yaml_compile.py` |
| **图谱真值** | `docs/_tech_graph/graph.json` |
| **Mermaid 协议** | `docs/_tech_graph/99_mermaid_protocol.md` |
| **graph_v2 schema** | `docs/_tech_graph/graph_v2_schema.md` |

---

## 给执行帽的必读列表

- `AGENTS.md`
- `docs/_tech_graph/12_flow_fts.ai.md`
- `docs/_tech_graph/12_flow_fts.md`
- `docs/_tech_graph/99_mermaid_protocol.md`
- `docs/_tech_graph/graph_v2_schema.md`
- `scripts/graph_yaml_compile.py`
- `tests/test_graph_yaml_p2_11_flow_text2sql.py`

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 | 测试 |
|---|-------------|----------|----------|--------|----------|------|
| F1 | `fp-yaml-parse` | `12_flow_fts.graph.yaml` 语法错误 | `yaml.safe_load` 抛异常 | 否 | pytest 失败 | `test_12_flow_fts_yaml_source_is_valid_yaml` |
| F2 | `fp-graph-diff` | YAML 节点/边/锚点与 `graph.json` 切片不一致 | `--check` 非 0 | 否 | CI `tech-graph` 失败 | `test_12_flow_fts_*_match_graph_json` |
| F3 | `fp-regression-00_main` | 脚本改动改坏 `00_main` 生成 | `00_main.md` 内容变化 | 否 | CI `manifest_check` / 人工 review 失败 | 现有 `tests/test_graph_yaml_compile.py` + `verify-tech-graph.sh` |

---

## 思考轮次（P3a 启用多轮思考）

### 思考轮控制（Agent 填 · 22 审）

| 字段 | 值 |
|------|-----|
| **actual_last_round** | `R5` |
| **early_stop** | `no` |
| **early_stop_reason** | — |
| **residual_risks** | 见 R5 |

### R0 · 读 task / SPEC / 非范围

- 已读 Epic 母单、P0/P1/P2 task、`12_flow_fts.ai.md`、`12_flow_fts.md`、编译脚本
- 非范围：其他 graph、`.ai.md` 删除、契约变更

### R1 · 代码事实

- `graph.json` 中 `12_flow_fts` 切片：16 节点 / 21 边 / 8 条带锚点边
- 边类型：`depends_on`/`async_calls`/`condition`/`triggers`
- 编译脚本已支持 `notes` 字段（P2 新增）

### R2 · 方案对比

**方案 A：沿用 P2 脚本与 notes 机制（推荐）**

- 风险最低，P2 已验证 `notes` 可补文档覆盖

**方案 B：另起手写 .md**

- 违反唯一编辑源原则

**结论**：方案 A。

### R3 · 边界 / 测试 / failure_paths

- `12_flow_fts.ai.md` 是真值源，`.md` 是简化版
- `Q` / `RPC` / `OUT` 为跨图引用节点，按 graph.json 切片不列入 YAML nodes
- 锚点空 symbol（`Q -> QS`、`QS -> I18N`）按 P1/P2 模式跳过空注释

### R4 · pytest / PR 策略

- 创建 `tests/test_graph_yaml_p3a_12_flow_fts.py`（参考 P2）
- 跑 `--check --graph-id 12_flow_fts` 通过后再生成 `.md`
- 最后跑全量 pytest 与 `verify-tech-graph.sh`

### R5 · 图谱/契约增量 + 关账判断

- 图谱增量：新增 `12_flow_fts.graph.yaml`、更新 `12_flow_fts.md`、deprecation 头
- 工具增量：无（复用 P2）
- 契约增量：无
- 残余风险：无

---

## 验收标准

- [x] `scripts/graph_yaml_compile.py --graph-id 12_flow_fts` 成功生成 `12_flow_fts.md`
- [x] `scripts/graph_yaml_compile.py --check --graph-id 12_flow_fts` exit 0
- [x] `tests/test_graph_yaml_p3a_12_flow_fts.py` ≥1 用例，全部通过
- [x] 回测：`00_main.md` `--check` 通过
- [x] `12_flow_fts.ai.md` 顶部含 `@deprecated · 源迁 YAML`
- [x] PR 上 `pytest`、`tech-graph`、`verify-fast` workflow 全绿
- [x] **L2**：无新增无注解万能 dict
- [x] **L1 B-07/B-10**：diff 限于 scope

---

## 规划 artifact

### 实施清单

- [x] 1.1 确认 `scripts/graph_yaml_compile.py` 已满足需求
- [x] 1.2 创建 `docs/_tech_graph/12_flow_fts.graph.yaml`
- [x] 1.3 生成 `docs/_tech_graph/12_flow_fts.md`
- [x] 1.4 标记 `12_flow_fts.ai.md` deprecated
- [x] 1.5 新增 `tests/test_graph_yaml_p3a_12_flow_fts.py`
- [x] 1.6 本地跑 `ruff check api tests`、`pytest tests -m "not intent_eval and not intent_benchmark"`、`bash scripts/verify-tech-graph.sh`
- [x] 1.7 提交、推分支、建 PR、等 CI 绿后 merge

---

## 实现备忘（30 帽回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/_tech_graph/12_flow_fts.graph.yaml`、`docs/_tech_graph/12_flow_fts.md`、`docs/_tech_graph/12_flow_fts.ai.md`、`tests/test_graph_yaml_p3a_12_flow_fts.py` |
| 关键 env | 无 |
| SQL 执行顺序 | 无 |
| 接口变更 | 无 |
| 图谱变更点 | `12_flow_fts` 新增 YAML 源，`.md` 改为生成 |

---

## 自检结论（40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `pytest tests/test_graph_yaml_p3a_12_flow_fts.py -v` |
| 结论 | **pass** |
| 要点 | 9/9 通过；`--check --graph-id 12_flow_fts` exit 0；`00_main` 回测通过 |

| 项 | 结果 |
|----|------|
| 命令 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` |
| 结论 | **pass** |
| 要点 | TBD |

| 项 | 结果 |
|----|------|
| 命令 | `ruff check api tests` |
| 结论 | **pass** |
| 要点 | All checks passed |

| 项 | 结果 |
|----|------|
| 命令 | `bash scripts/verify-tech-graph.sh` |
| 结论 | **pass** |
| 要点 | OK: verify-tech-graph passed |

---

## 给 Cursor

`graph-yaml-p3a-12-flow-fts`、`test_strategy: required`、`failure_paths`、`行为变更 Delta`、`Scenario ID`、`semi_auto: false`、`human_gate`、`audit_profile: post_close`、`git_branch`、`Harness`、`RECENT_TASK_SCHEDULE`
