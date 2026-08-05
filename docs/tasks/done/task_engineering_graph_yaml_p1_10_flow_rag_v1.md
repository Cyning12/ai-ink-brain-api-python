# Task：图谱 YAML 图源迁移 P1 — `10_flow_rag`

> **状态**：done
> **关联图谱**：`docs/_tech_graph/10_flow_rag.md`
> **关联 Issue/PR**：承接 Epic `task_engineering_graph_yaml_migration_epic_v1.md` · PR #166
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
| **chain_prompt** | `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_graph-yaml-p1-10-flow-rag_zh.md`（按需创建） |
| **audit_profile** | `post_close` |
| **git_branch** | `task/graph-yaml-p1-10-flow-rag` |
| **experience_capture** | `required` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | signed | 22-R1,30 | P1 范围与验收标准人扫 |
| HG-AUDIT-R1 | signed | 30 | 22 R1 落盘 `docs/harness/reviews/` 后人签 |
| HG-REINSPECT | signed | done | 50 复检后人签、合并 PR 前 |

---

## 背景与目标

Epic `task_engineering_graph_yaml_migration_epic_v1.md` 将 `00_main` 的 YAML 图源模式推广到剩余 6 个 graph。P1 负责首个核心子流程 `10_flow_rag`。

P1 同时承担**公共工具改造**：扩展 `scripts/graph_yaml_compile.py` 支持 `--graph-id` / `--all`，使 P2～P5 能复用同一脚本。

完成态：

- `docs/_tech_graph/10_flow_rag.graph.yaml` 成为 `10_flow_rag` 唯一编辑源
- `docs/_tech_graph/10_flow_rag.md` 由脚本生成
- `docs/_tech_graph/10_flow_rag.ai.md` 顶部加 `@deprecated · 源迁 YAML`
- `scripts/graph_yaml_compile.py` 可指定 graph 编译
- `tests/test_graph_yaml_p1_10_flow_rag.py` 覆盖 YAML 解析、节点/边/锚点与 `graph.json` 一致、`--check` 模式

---

## 范围

- [ ] 扩展 `scripts/graph_yaml_compile.py`：支持 `--graph-id` / `--all` / `--check` 对任意 graph 校验
- [ ] 创建 `docs/_tech_graph/10_flow_rag.graph.yaml`（以 `.ai.md` 为真值源，对齐 `graph.json` 切片）
- [ ] 生成 `docs/_tech_graph/10_flow_rag.md`
- [ ] 标记 `docs/_tech_graph/10_flow_rag.ai.md` 为 `@deprecated · 源迁 YAML`
- [ ] 新增 `tests/test_graph_yaml_p1_10_flow_rag.py`
- [ ] 回测 `00_main`：确保脚本参数化后 `00_main.md` 内容不变
- [ ] PR 合并到 `main`

## 非范围

- 不迁移其他 graph（Epic 中 P2～P5 负责）
- 不修改 `graph.json`
- 不删除 `.ai.md`
- 不引入 `.cyning-harness/`

---

## 行为变更（Delta）

### ADDED

- **Requirement**：`10_flow_rag.graph.yaml` 成为 `10_flow_rag` 唯一编辑源
  - **Scenario**：GIVEN 维护者修改 RAG 子流程拓扑 WHEN 编辑 `10_flow_rag.graph.yaml` THEN 运行脚本可重新生成 `10_flow_rag.md` 且 diff 校验通过
- **Requirement**：`scripts/graph_yaml_compile.py` 支持 `--graph-id`
  - **Scenario**：GIVEN 需要编译指定 graph WHEN 执行 `python scripts/graph_yaml_compile.py --graph-id 10_flow_rag` THEN 输出 `docs/_tech_graph/10_flow_rag.md`

### MODIFIED

- **Requirement**：`10_flow_rag.md` 由手写改为脚本生成（Previously：手写维护）
- **Requirement**：`10_flow_rag.ai.md` 顶部增加 deprecation 注释（Previously：无）

### REMOVED

- 无

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| **Epic 母单** | `docs/tasks/active/task_engineering_graph_yaml_migration_epic_v1.md` |
| **P0 试点** | `docs/tasks/done/task_engineering_graph_yaml_p0_00_main_v1.md` |
| **编译脚本** | `scripts/graph_yaml_compile.py` |
| **图谱真值** | `docs/_tech_graph/graph.json` |
| **Mermaid 协议** | `docs/_tech_graph/99_mermaid_protocol.md` |
| **graph_v2 schema** | `docs/_tech_graph/graph_v2_schema.md` |

---

## 给执行帽的必读列表

- `AGENTS.md`
- `docs/_tech_graph/10_flow_rag.ai.md`
- `docs/_tech_graph/10_flow_rag.md`
- `docs/_tech_graph/99_mermaid_protocol.md`
- `docs/_tech_graph/graph_v2_schema.md`
- `scripts/graph_yaml_compile.py`
- `tests/test_graph_yaml_compile.py`

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 | 测试 |
|---|-------------|----------|----------|--------|----------|------|
| F1 | `fp-yaml-parse` | `10_flow_rag.graph.yaml` 语法错误 | `yaml.safe_load` 抛异常 | 否 | pytest 失败 | `test_10_flow_rag_yaml_source_is_valid_yaml` |
| F2 | `fp-graph-diff` | YAML 节点/边/锚点与 `graph.json` 切片不一致 | `--check` 非 0 | 否 | CI `tech-graph` 失败 | `test_10_flow_rag_*_match_graph_json` |
| F3 | `fp-regression-00_main` | 脚本参数化改坏 `00_main` 生成 | `00_main.md` 内容变化 | 否 | CI `manifest_check` / 人工 review 失败 | 现有 `tests/test_graph_yaml_compile.py` + `verify-tech-graph.sh` |

---

## 思考轮次（P1 启用多轮思考）

### 思考轮控制（Agent 填 · 22 审）

| 字段 | 值 |
|------|-----|
| **actual_last_round** | `R5` |
| **early_stop** | `no` |
| **early_stop_reason** | — |
| **residual_risks** | 见 R5 |

### R0 · 读 task / SPEC / 非范围

- 已读 Epic 母单、P0 task、`10_flow_rag.ai.md`、`10_flow_rag.md`、编译脚本
- 非范围：其他 graph、`.ai.md` 删除、契约变更

### R1 · 代码事实

- `graph.json` 中 `10_flow_rag` 切片：21 节点 / 34 边 / 13 条带锚点边
- 边类型：`depends_on`/`async_calls`/`merges`/`condition`/`yields`/`archives`/`branches`
- 当前编译脚本硬编码 `00_main`；需提取为函数参数 `graph_id`

### R2 · 方案对比

**方案 A：先参数化脚本，再写 YAML（推荐）**

- 脚本 `--graph-id` 一次改好，P2～P5 直接复用
- P1 自己验证脚本可用
- 风险集中但可控

**方案 B：复制脚本为每个 graph 单独版本**

- 避免改坏 P0，但重复代码多
- 不推荐

**结论**：方案 A。

### R3 · 边界 / 测试 / failure_paths

- `10_flow_rag.ai.md` 是真值源，`.md` 是简化版，不要照抄 `.md`
- 锚点注释需匹配 `99_mermaid_protocol.md` §3 格式
- 回测 `00_main` 通过对比生成前后 md5 或 pytest 断言

### R4 · pytest / PR 策略

- 先写 `tests/test_graph_yaml_p1_10_flow_rag.py`（红）
- 再扩展脚本 + 写 YAML（绿）
- 最后跑全量 pytest 与 `verify-tech-graph.sh`

### R5 · 图谱/契约增量 + 关账判断

- 图谱增量：新增 `10_flow_rag.graph.yaml`、更新 `10_flow_rag.md`、deprecation 头
- 工具增量：`scripts/graph_yaml_compile.py` 支持 `--graph-id` / `--all`
- 契约增量：无
- 残余风险：
  - R1：`flowchart LR` 方向需确认生成后是否保留（当前脚本默认 TD）
  - R2：`TEND`/`TEND_KEYS` 节点偏注释性，但 graph.json 已包含，按真值保留

---

## 验收标准

- [ ] `scripts/graph_yaml_compile.py --graph-id 10_flow_rag` 成功生成 `10_flow_rag.md`
- [ ] `scripts/graph_yaml_compile.py --check --graph-id 10_flow_rag` exit 0
- [ ] `tests/test_graph_yaml_p1_10_flow_rag.py` ≥1 用例，全部通过
- [ ] 回测：`00_main.md` 内容无变化（或变化仅来自脚本格式优化且有记录）
- [ ] `10_flow_rag.ai.md` 顶部含 `@deprecated · 源迁 YAML`
- [ ] PR 上 `pytest`、`tech-graph`、`verify-fast` workflow 全绿
- [ ] **L2**：无新增无注解万能 dict
- [ ] **L1 B-07/B-10**：diff 限于 scope

---

## 规划 artifact

### 实施清单

- [x] 1.1 扩展 `scripts/graph_yaml_compile.py`：增加 CLI `--graph-id` / `--all`，内部函数接受 `graph_id` 参数
- [x] 1.2 创建 `docs/_tech_graph/10_flow_rag.graph.yaml`
- [x] 1.3 生成 `docs/_tech_graph/10_flow_rag.md`
- [x] 1.4 标记 `10_flow_rag.ai.md` deprecated
- [x] 1.5 新增 `tests/test_graph_yaml_p1_10_flow_rag.py`
- [x] 1.6 本地跑 `ruff check api tests`、`pytest tests -m "not intent_eval and not intent_benchmark"`、`bash scripts/verify-tech-graph.sh`
- [ ] 1.7 提交、推分支、建 PR、等 CI 绿后 merge

---

## 实现备忘（30 帽回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `scripts/graph_yaml_compile.py`、`docs/_tech_graph/10_flow_rag.graph.yaml`、`docs/_tech_graph/10_flow_rag.md`、`docs/_tech_graph/10_flow_rag.ai.md`、`tests/test_graph_yaml_p1_10_flow_rag.py` |
| 关键 env | 无 |
| SQL 执行顺序 | 无 |
| 接口变更 | 无 |
| 图谱变更点 | `10_flow_rag` 新增 YAML 源，`.md` 改为生成 |

---

## 自检结论（40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `pytest tests/test_graph_yaml_p1_10_flow_rag.py -v` |
| 结论 | **pass** |
| 要点 | 9/9 通过；`--check --graph-id 10_flow_rag` exit 0；`00_main` 回测通过 |

| 项 | 结果 |
|----|------|
| 命令 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` |
| 结论 | **pass** |
| 要点 | 369 passed, 1 skipped, 2 deselected |

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

`graph-yaml-p1-10-flow-rag`、`test_strategy: required`、`failure_paths`、`行为变更 Delta`、`Scenario ID`、`semi_auto: false`、`human_gate`、`audit_profile: post_close`、`git_branch`、`Harness`、`RECENT_TASK_SCHEDULE`
