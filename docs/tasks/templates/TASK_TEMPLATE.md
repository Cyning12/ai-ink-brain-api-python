# Task：<动词 + 范围>

> **状态**：draft / pending / in_progress / done  
> **关联图谱**：`docs/_tech_graph/xx_flow_xxx.md`  
> **关联 Issue/PR**：#xxx  
> **前端依赖**：`<前端任务文件名>`（如 API 变更需前端配合，否则填 "无"）

> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/*.md` 索引。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**；链式常模：[`docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md`](../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md) + [`docs/harness/prompts/PROMPT_*_chain_serial_*`](../harness/prompts/README.md)。**`semi_auto` 已 deprecated**（历史见 [`HANDOFF_SEMI_AUTO.md`](../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)）。  
> **行为变更 Delta / Scenario**（写法参考 · 非 OpenSpec 目录）：见下文 **§行为变更**、**§失败路径**；TDD 与分层测试决策见 [`docs/tasks/README.md`](../README.md) **§test_strategy** 及 diary [`2026-05-30-backend-TDD-architecture-assessment.md`](../../diary/tmp/2026-05-30-backend-TDD-architecture-assessment.md)。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` / `recommended` / `not_applicable` |
| **test_strategy_note** | （仅 `not_applicable` 时 **必填** 一行理由；禁止滥用） |
| **freeze_id** | （可选）实现基准契约 ID，如 `SPEC-xxx@2026-05-22` 或 commit 短哈希 |
| **gates_before_code** | （可选）显式门闸列表；默认隐式：`failure_paths` + 验收命令 + 必读路径已齐 |
| **semi_auto** | **`deprecated`** — 历史兼容 `true`/`false`；**新 task 填 `false`** + **`orchestration`** + 链 PROMPT（见 [`SPEC-Governance-Harness-Chain-Orchestration-v1.md`](../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md)） |
| **orchestration** | `Cursor Task 链` / `Claude Code` / `Kimi Code` / `MANIFEST 仅` — 链式执行器 |
| **chain_prompt** | `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_<slug>_zh.md`（或 `PROMPT_cursor_*` / `PROMPT_kimi_*` 实例路径） |
| **audit_profile** | `full` / `post_close` / `human_only` — 审核节奏（见 HARNESS_V2 §5.5） |
| **git_branch** | `task/<slug>` — 链式执行与实现 **禁止** 在 `main` 上连续提交 |
| **experience_capture** | `required` / `recommended` / `not_applicable` — 关账经验摘要档位（见 HARNESS_V2 §5.7） |
| **experience_capture_note** | （仅 `not_applicable` 时 **必填** 一行理由） |
| **kpi_rubric** | **`KPI_RUBRIC_v1_2`（2026-05-31 起新建 task 必填）** |
| **kpi_aggregator** | `CLOSE`（默认，可省略）\| `00` \| `50` \| `human` — 谁汇总 `### KPI（00）`（见 HARNESS_V2 §5.8） |

### 人工闸 `human_gate`

> **仅人** 可将 `pending` 改为 `approved`；Agent 遇阻塞帽 **拒执行** 所列 `blocks_hats`。

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1,30 | 初稿 task / SPEC 人扫 |
| HG-AUDIT-R1 | pending | 30 | 22 R1 落盘 `docs/harness/reviews/` 后人签 |
| HG-REINSPECT | pending | done | （可选）50 复检后人签、合并 PR 前 |

**`audit_profile` 速查**：

| 取值 | 适用 | 人工闸建议 |
|------|------|------------|
| `full` | 架构 / 跨仓 / 高风险 | 多轮 22（R1/R2…） |
| `post_close` | 工程流水线 task（**推荐**） | 闸 1：HG-TASK-DRAFT、HG-AUDIT-R1；闸 2：关账签收 |
| `human_only` | 纯文档 / 产品决策 | 关键步均 `pending`，不自动戴帽 |

---

## 背景与目标

<短段落，描述完成态行为。>

---

## 范围

- [ ] <具体事项 1>
- [ ] <具体事项 2>

## 非范围

- <明确排除的事项，减少越界>

---

## 行为变更（Delta · 可选）

> **相对** `docs/spec/` 或现网行为的增量描述（OpenSpec delta 语义；**不**建 `openspec/` 目录）。  
> 无对外行为变更时填 **`无`**；关账时可合并进主 SPEC（见 task README）。

### ADDED

- **Requirement**：<新行为摘要，SHALL/MUST 可选>
  - **Scenario**：<场景名> — GIVEN … WHEN … THEN …

### MODIFIED

- **Requirement**：<变更后行为>（Previously: <原行为>）
  - **Scenario**：<场景名> — GIVEN … WHEN … THEN …

### REMOVED

- **Requirement**：<废弃行为>（理由：…）

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| **编码规范 L1** | 工作区 `docs/standards/CODING_BASELINE_L1_v1_zh.md` |
| **编码规范 L2** | `docs/standards/CODING_BACKEND_L2_v1_zh.md`（P-01～P-15） |
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| API 契约 | `POST /api/py/xxx` |
| 数据库表 | `public.xxx` |
| 图谱文件 | `docs/_tech_graph/xx_xxx.md` |
| **写 task 读序** | 通用 `docs/harness/guides/GUIDANCE_task_coding_standards_v1_zh.md` · 后端 `GUIDANCE_backend_task_coding_l2_v1_zh.md` |

---

## 给执行帽的必读列表

- `AGENTS.md`
- `docs/standards/CODING_BACKEND_L2_v1_zh.md`（按本 task 范围勾选 P-xx）
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
- `docs/_tech_graph/`（本 task 关联 flow）

---

## 失败路径

> 每条建议：**触发条件** → **系统行为**（含错误码或 HTTP 状态）→ **是否可重试** → **用户可见类型**。  
> **Scenario ID** 与 pytest / `_test_manifest.json` 互链（OpenSpec Scenario 语义；**不要求** strict TDD red-green，见 diary TDD 分析）。  
> 缺失或不可操作化时，**30 执行帽拒开工**（仅输出缺口清单）。

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 | 测试（可选） |
|---|-------------|----------|----------|--------|----------|--------------|
| F1 | `fp-db-disconnect` | <例：Supabase 不可用> | `500 DATABASE_DISCONNECT` | 是 | 服务暂不可用提示 | `tests/test_*.py::test_*` |
| F2 | `fp-invalid-json` | <例：参数非法> | `422` + 结构化 `detail` | 否 | 字段级错误说明 | — |

> **思考未闭合**：§4 仍有 `（待填）` 且无合法 **思考轮控制** → 22 **退回 10** · 30 **拒开工**（见 [`hats/10-requirements.md`](../harness/prompts/hats/10-requirements.md) §思考轮）。

---

## 思考轮次（高复杂度 / orchestration 含 rethink 时 · 10 帽预置）

> **何时启用**：`audit_profile: full`、触 `api/` 契约、跨仓、或 Agent rethink 链。简单 task **可删本节**。  
> **真值**：[`docs/harness/prompts/hats/10-requirements.md`](../harness/prompts/hats/10-requirements.md) §思考轮 · [`22-task-audit.md`](../harness/prompts/hats/22-task-audit.md)（22 可 **退回 10**）。

### 思考轮控制（Agent 填 · 22 审）

| 字段 | 值 |
|------|-----|
| **actual_last_round** | `R5` / `R3` / … |
| **early_stop** | `no` / `yes` |
| **early_stop_reason** | （`early_stop=yes` **必填**） |
| **residual_risks** | `none` 或逐条（**必填**） |

### R0 · 读 task / SPEC / 非范围

**回填区：** `（待填）`

### R1 · 代码事实

**回填区：** `（待填）`

### R2 · 方案对比

**回填区：** `（待填）`

### R3 · 边界 / 测试 / failure_paths

**回填区：** `（待填）`

### R4 · pytest / PR 策略

**回填区：** `（待填）`

### R5 · 图谱/契约增量 + 关账判断

**回填区：** `（待填）`

---

> **L2 Phase C（设计）**：`Scenario ID` / `F#` 与 `_test_manifest.json` `entries[].id` 对齐规则见 [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) **§4.4**（实现期双向校验 **另 task**）。

## 验收标准

- [ ] <验收项 1>
- [ ] <验收项 2>
- [ ] <验收项 3>
- [ ] PR 上 `pytest` workflow 全绿（本地等价：`pytest tests -m "not intent_eval and not intent_benchmark"`）
- [ ] PR 上 `tech-graph` workflow 全绿（本地等价：`bash scripts/verify-tech-graph.sh` 与 `python tools/tech_graph_contract_check.py`）
- [ ] 若新增/修改 **SQL 表、RPC、端点、env**，同步更新 `docs/_tech_graph/_manifest.json`（`_contract_manifest.json` 若涉 SSE/契约）
- [ ] **L2**：无新增无注解万能 dict；路由/模块边界符合 P-01
- [ ] **L1 B-07/B-10**：diff 限于 scope；与 `test_strategy` 一致

**测试 / TDD（与 `test_strategy` 对齐）**：

| test_strategy | 自检须含 |
|---------------|----------|
| `required` | 先失败可复现测试再实现；命令 + 通过证明 |
| `recommended` | 鼓励补测；以命令 + 人工为主 |
| `not_applicable` | `test_strategy_note` 一行理由 |

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见 `AGENTS.md`）。

---

## 规划 artifact（大 task · 可选）

> Epic 级 task 可拆分「规划 / 设计 / 实施清单」，仍保持 **单文件** task 真源（OpenSpec 四件套语义）。

### 规划摘要（proposal 等价）

- **Intent**：<解决什么问题>
- **Scope / 非范围**：见上文或摘要
- **Approach**：<高层方案一句话>

### 技术方案（design 等价）

- <架构决策、数据流、涉及模块；**实现细节不进** `docs/spec/` 行为 SPEC>

### 实施清单（tasks 等价）

- [ ] 1.1 <子步骤>
- [ ] 1.2 <子步骤>
- [ ] 2.1 <子步骤>

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `<文件列表>` |
| 关键 env | `<新增/变更的环境变量>` |
| SQL 执行顺序 | `<init.sql → migration.sql>` |
| 接口变更 | `<新增/修改的端点>` |
| 图谱变更点 | `<_tech_graph/ 中更新的文件>` |

---

## 自检结论（执行者 · 40 帽回填）

> **40 自检帽** 运行 task 所列命令后，将 **原始输出要点** 与 pass/fail 结论写入本节。

| 项 | 结果 |
|----|------|
| 命令 | `<例：pytest …>` |
| 结论 | pass / fail |
| 要点 | `<日志摘要或失败原因>` |

---

## 给 Cursor

`<task_slug>`、`test_strategy`、`failure_paths`、`行为变更 Delta`、`Scenario ID`、`semi_auto`、`human_gate`、`audit_profile`、`git_branch`、`Harness`、`RECENT_TASK_SCHEDULE`
