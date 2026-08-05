# Task：Harness KPI v1.2 试点 — 00 编排 + 帽链验证（docs）

> **状态**：`done`（2026-05-31 · `KPI-RUBRIC-PILOT@2026-05-31` · Task_KPI% **100** · **pass**）  
> **schedule_ref**：RECENT §1.1（新增 · 待同步排期表）  
> **登记日期**：2026-05-31  
> **路线**：**B** — 与 `KPI_RUBRIC_v1_2` 分支 **同 PR** 交付（基建 + 试点关账）  
> **SKILL**：[`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) · [`KPI_RUBRIC_v1_2.md`](../../harness/guides/KPI_RUBRIC_v1_2.md)

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |
| **task_slug** | `harness-kpi-v1-2-pilot` |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 Harness 文档与索引；不触达 `api/` / 行为变更 |
| **freeze_id** | `KPI-RUBRIC-PILOT@2026-05-31` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **experience_capture** | `required` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | **`00`**（00 逐帽 HatInstance + 关账写 `### KPI（00）`） |
| **git_branch** | `KPI_RUBRIC_v1_2` |

### 人工闸 `human_gate`

> **预批说明**：HG-TASK-DRAFT / HG-AUDIT-R1 预批于 `c2b73d8`；HG-REINSPECT 人签 `a496d9b`（50 通过后）。

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | 试点 task 草案 · 预批 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后人签 · 预批 |
| HG-REINSPECT | approved | done | **50 通过后** 人签再 merge（关账硬闸） |

### 开帽约定（已锁定）

| 项 | 决定 |
|----|------|
| **第一棒** | **00 总调度**（`TEMPLATE-orchestrator-invoke` §3） |
| **KPI 汇总** | **`kpi_aggregator: 00`** |
| **帽链** | 00 → 22 R1 → 30 → 40 → 50 → 00/CLOSE |
| **semi_auto** | 同会话戴帽（不强制 Task 子代理） |
| **50** | **新会话** Fresh Context（推荐） |
| **分支** | 在 **`KPI_RUBRIC_v1_2`** 上续跑（路线 B） |

**法定 SDD 顺序不变**：10 →（22）→ 30 → 40 → 50 → CLOSE。**00 在链外编排**（见 [`00-orchestrator.md`](../../harness/prompts/hats/00-orchestrator.md)）。

---

## 1. 背景与目标

KPI v1.2、00 总调度帽、CLOSE/50 模板已落在分支 `KPI_RUBRIC_v1_2`，尚未经 **完整帽链 + 落盘 + KPI 表** 实战验证。

**完成态**：

- 一条 **docs-only** 变更经 **00 编排 → 22→30→40→50→CLOSE** 跑通；
- **00** 维护 HatInstance 并写入 **`### KPI（00）`**（Task_KPI%）；
- invoke / review / reinspect 落盘齐全；
- 索引与规划正文与 KPI 文档对齐。

---

## 2. 范围

- [x] [`docs/harness/README.md`](../../harness/README.md) §1 增 **KPI_RUBRIC_v1_2**、**00-orchestrator** 索引  
- [x] [`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) 补 **§5.7** `experience_capture`、**§5.8** `kpi_rubric` / `kpi_aggregator` / `### KPI（00）`  
- [x] [`docs/tasks/templates/TASK_TEMPLATE.md`](../templates/TASK_TEMPLATE.md) 增 `experience_capture`、`kpi_rubric`、`kpi_aggregator`  
- [x] Harness 帽链落盘：`invokes/by-task/harness-kpi-v1-2-pilot/`（含 **`invoke_*_00_*`**）、`reviews/…`、`reinspect_results/reinspect_harness-kpi-v1-2-pilot_20260531_v1.md`  
- [x] 本 task **`### KPI（00）`** 由 **00** 关账轮填写（非空）  
- [x] **`experience_capture: required`** → CLOSE 含经验摘要（§12）  
- [x] 关账：`done/` + `_views/done.md` + CLOSE_TRACE

## 3. 非范围

- `api/`、`tests/`、`.github/workflows/`  
- ChatBI 业务 task  
- 新增 **60 帽**

---

## 4. 行为变更（Delta）

**无**（纯文档 / Harness 索引；无对外 HTTP/SSE 契约变更）

---

## 5. 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| KPI 真值 | [`docs/harness/guides/KPI_RUBRIC_v1_2.md`](../../harness/guides/KPI_RUBRIC_v1_2.md) |
| 00 帽 | [`docs/harness/prompts/hats/00-orchestrator.md`](../../harness/prompts/hats/00-orchestrator.md) |
| 00 invoke | [`TEMPLATE-orchestrator-invoke.md`](../../harness/prompts/templates/TEMPLATE-orchestrator-invoke.md) |
| 单 task SKILL | [`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) |
| 关账 | [`HANDOFF_CLOSE_TRACE.md`](../../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md) §4 步骤 6–7 |

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-kpi-blocked-d2` | 任帽 D2 **fail** 或 KPI **blocked** | **不得关账**；回 30 或打回 22 | 是 | CLOSE 阻塞清单 |
| F2 | `fp-kpi-missing-table` | 关账无 `### KPI（00）` | CLOSE **fail** | 00 补表 | 缺口路径 |
| F3 | `fp-exp-required-missing` | `experience_capture: required` 无摘要 | CLOSE **fail** | 补 diary/摘要 | 同上 |
| F4 | `fp-invoke-stub` | invoke §3 &lt;15 行 | **不得 commit** invoke | 补全 | HANDOFF_AUTO_COMMIT |
| F5 | `fp-scope-api` | diff 含 `api/` | 50 **fail** · 拒 scope | revert | 非范围 |

---

## 7. 验收标准

- [x] 范围 §2 docs 变更已提交  
- [x] **00** / 22 / 30 / 40 / 50 invoke 落盘且 §3 ≥15 行  
- [x] `reviews/by-task/harness-kpi-v1-2-pilot/` 有 R1 audit  
- [x] `reinspect_results/reinspect_harness-kpi-v1-2-pilot_20260531_v1.md` 建议合并  
- [x] task **`### KPI（00）`** 完整（§6 演算级：HatInstance + Task_KPI% + blocked 判定）  
- [x] CLOSE_TRACE 含 experience + KPI 核对（对话 · invoke_CLOSE）  
- [x] **HG-REINSPECT** → `approved` 后 merge PR（`a496d9b` 人签）  
- [x] 本地 `pytest tests -m "not intent_eval and not intent_benchmark"` 绿（269 passed · 50 复检）

---

## 8. 计划帽链

```text
00（开帽 + 编排）→ 22 R1 → 30 → 40 → 50（新会话）→ 00/CLOSE（KPI 汇总 + 关账）
```

| 帽 | 落盘 | KPI 动作 |
|----|------|----------|
| **00** | `invoke_*_00_*` **必须** | 阶段状态表；逐帽 HatInstance；关账写 ### KPI（00） |
| 22 | `reviews/…/audit_R1_*` | HatInstance + Judgment |
| 30 | `invoke_*_30_*` | HatInstance + Judgment |
| 40 | `invoke_*_40_*` + 自检表 | HatInstance + Judgment |
| 50 | `reinspect_*` + `invoke_*_50_*` | HatInstance + Judgment（**新会话**） |
| CLOSE | `invoke_*_CLOSE_*` + CLOSE_TRACE | experience 核对；HG-REINSPECT 仍 pending 则停 |

---

## 9. 执行前确认（已拍板 · 2026-05-31）

| # | 项 | 决定 |
|---|-----|------|
| C1 | 第一棒 | **00** |
| C2 | 50 | **新会话** |
| C3 | 子代理 | **同会话 semi_auto** |
| C4 | 分支 | **`KPI_RUBRIC_v1_2`** |
| C5 | RECENT | 关账时同步（非阻塞开跑） |
| C6 | HG-REINSPECT | **人** 在 50 通过后签 `approved` |

**新会话开跑**：粘贴 [`TEMPLATE-orchestrator-invoke.md`](../../harness/prompts/templates/TEMPLATE-orchestrator-invoke.md) 定制 §3（`kpi_aggregator: 00`）；Open Folder = **本仓根**；确认 `git branch` = `KPI_RUBRIC_v1_2`。

---

## 10. ### KPI（00）

**rubric**: KPI_RUBRIC_v1_2 · **汇总**: **100%** · **状态**: **pass** · **帽**: 00→22→30→40→50→CLOSE

| hat_code | round | agent_mode | D1 | D2 | D3 | D4 | D5 | judgment_notes |
|----------|-------|------------|----|----|----|----|-----|----------------|
| 00 | open | main_chat | 100 | 100 | 100 | 100 | — | — |
| 22 | R1 | main_chat | 100 | 100 | 100 | 100 | — | R1 时 gate_check HG-REINSPECT FAIL 为预期 |
| 30 | R1 | main_chat | 100 | 100 | 100 | 100 | — | — |
| 40 | R1 | main_chat | 100 | 100 | 100 | 100 | — | — |
| 50 | v1 | main_chat | 100 | 100 | 100 | 100 | 100 | Fresh Context；建议条件合并；见 reinspect §9 |

**Task 维聚合**（KPI_RUBRIC §4.1–§4.2）：

| 大维 | 聚合 | 得分 |
|------|------|------|
| D1 | avg(五帽) | 100 |
| D2 | min | 100 |
| D3 | avg | 100 |
| D4 | min | 100 |
| D5 | min(50) | 100 |

```text
Task_KPI% = 100×20% + 100×30% + 100×15% + 100×15% + 100×20% = 100%
blocked：无（无帽 D2/D5 fail）
状态：pass（100 ≥ 80）
```

**blocked 原因**：（无）

---

## 11. ### 自检结论（执行者）

> **40 帽 · 2026-05-31** · 分支 `KPI_RUBRIC_v1_2`

### 命令与退出码

| 命令 | cwd | 退出码 | 要点 |
|------|-----|--------|------|
| `pytest tests -m "not intent_eval and not intent_benchmark"` | 仓根 | 0 | 269 passed, 1 skipped |
| `python tools/harness_task_validate.py docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md` | 仓根 | 0 | OK |
| `python tools/harness_human_gate_check.py --task docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md` | 仓根 | 1 | **预期**：HG-REINSPECT pending（不阻塞 50；阻塞 merge） |

### 验收表（§7 摘要）

| 验收项 | 结果 | 证据 |
|--------|------|------|
| §2 docs 变更 | pass | README / HARNESS_V2_PLAN §5.7–5.8 / TASK_TEMPLATE diff |
| invoke §3 ≥15 行 | pass | `invokes/by-task/harness-kpi-v1-2-pilot/invoke_*` |
| reviews R1 | pass | `reviews/by-task/.../task_*_audit_R1_20260531.md` |
| reinspect | pass | `reinspect_harness-kpi-v1-2-pilot_20260531_v1.md` · commit `4df8add` |
| ### KPI（00） | pass | §10 · Task_KPI% 100 · pass |
| pytest 回归 | pass | 见上表 |
| HG-REINSPECT | approved | 人签 `a496d9b` |

### OpenSpec × TDD 三维

| 维度 | 结论 |
|------|------|
| Completeness | pass — failure_paths F1–F5 + Scenario ID |
| Correctness | pass — 纯 docs，Delta=无 |
| Coherence | pass — 与 KPI_RUBRIC_v1_2 / 00 帽链一致 |

**已知未测项**：RECENT 排期同步（C5 非阻塞）。

---

## 12. 经验摘要（experience_capture · required）

> **00/CLOSE · 2026-05-31** · 试点 `kpi_aggregator: 00` 可复用决策

1. **帽链**：docs-only 试点可在 **同会话 semi_auto** 跑 00→22→30→40；**50 须新会话** Fresh Context（50 独立 VERIFY 与 reinspect 落盘已验证）。
2. **KPI 汇总**：`kpi_aggregator: 00` 时 HatInstance 由 00 逐帽维护，**`### KPI（00）` 仅 CLOSE 轮填写**；50 只写本帽行 + Judgment，不代填 Task 表。
3. **人工闸**：HG-REINSPECT **单独 commit 人签**（`a496d9b`）再 merge；Agent 不得代签；关账前 `harness_human_gate_check` 须 OK。
4. **validate**：task 小节标题须精确 **`## 失败路径`**（非 `## 6. 失败路径`），否则 `harness_task_validate` FAIL。
5. **路线 B**：KPI 基建与试点 task **同分支同 PR** 交付可行；invoke/review/reinspect 按 `by-task/harness-kpi-v1-2-pilot/` taxonomy 落盘齐全。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-31 | v0.1 草案：路线 B · gate 预批 · 暂不执行 |
| 2026-05-31 | v0.2：`kpi_aggregator: 00` · §9 拍板 · `pending` 待新会话 00 开帽 |
| 2026-05-31 | v1.0 关账：00→50 帽链 · KPI 100% pass · HG-REINSPECT `a496d9b` · experience §12 |

---

## 给 Cursor

`harness-kpi-v1-2-pilot`、`KPI_RUBRIC_v1_2`、`kpi_aggregator:00`、`00-orchestrator`、路线 B、非 Loop
