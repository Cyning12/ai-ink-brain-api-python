# Task：Harness KPI v1.2 试点 — 00 编排 + 帽链验证（docs）

> **状态**：`pending`（**已拍板 · 新会话 00 开帽**；首棒执行后改 `in_progress`）  
> **schedule_ref**：RECENT §1.1（新增 · 待同步排期表）  
> **登记日期**：2026-05-31  
> **路线**：**B** — 与 `KPI_RUBRIC_v1_2` 分支 **同 PR** 交付（基建 + 试点关账）  
> **SKILL**：[`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) · [`KPI_RUBRIC_v1_2.md`](../../harness/guides/KPI_RUBRIC_v1_2.md)

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
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

> **预批说明**：用户 **2026-05-31** 授权 HG-TASK-DRAFT / HG-AUDIT-R1 **approved**（路线 B · 暂不代填 HG-REINSPECT）。

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | 试点 task 草案 · 预批 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后人签 · 预批 |
| HG-REINSPECT | pending | done | **50 通过后** 人签再 merge（关账硬闸） |

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

- [ ] [`docs/harness/README.md`](../../harness/README.md) §1 增 **KPI_RUBRIC_v1_2**、**00-orchestrator** 索引  
- [ ] [`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) 补 **§5.7** `experience_capture`、**§5.8** `kpi_rubric` / `kpi_aggregator` / `### KPI（00）`  
- [ ] [`docs/tasks/templates/TASK_TEMPLATE.md`](../templates/TASK_TEMPLATE.md) 增 `experience_capture`、`kpi_rubric`、`kpi_aggregator`  
- [ ] Harness 帽链落盘：`invokes/by-task/harness-kpi-v1-2-pilot/`（含 **`invoke_*_00_*`**）、`reviews/…`、`reinspect_results/reinspect_harness-kpi-v1-2-pilot_*`  
- [ ] 本 task **`### KPI（00）`** 由 **00** 关账轮填写（非空）  
- [ ] **`experience_capture: required`** → CLOSE 含经验摘要或链 `docs/diary/`  
- [ ] 关账：`done/` + `_views/done.md` + CLOSE_TRACE

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

## 6. 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-kpi-blocked-d2` | 任帽 D2 **fail** 或 KPI **blocked** | **不得关账**；回 30 或打回 22 | 是 | CLOSE 阻塞清单 |
| F2 | `fp-kpi-missing-table` | 关账无 `### KPI（00）` | CLOSE **fail** | 00 补表 | 缺口路径 |
| F3 | `fp-exp-required-missing` | `experience_capture: required` 无摘要 | CLOSE **fail** | 补 diary/摘要 | 同上 |
| F4 | `fp-invoke-stub` | invoke §3 &lt;15 行 | **不得 commit** invoke | 补全 | HANDOFF_AUTO_COMMIT |
| F5 | `fp-scope-api` | diff 含 `api/` | 50 **fail** · 拒 scope | revert | 非范围 |

---

## 7. 验收标准

- [ ] 范围 §2 docs 变更已提交  
- [ ] **00** / 22 / 30 / 40 / 50 invoke 落盘且 §3 ≥15 行  
- [ ] `reviews/by-task/harness-kpi-v1-2-pilot/` 有 R1 audit  
- [ ] `reinspect_results/reinspect_harness-kpi-v1-2-pilot_YYYYMMDD_v1.md` 建议合并  
- [ ] task **`### KPI（00）`** 完整（§6 演算级：HatInstance + Task_KPI% + blocked 判定）  
- [ ] CLOSE_TRACE 含 experience + KPI 核对  
- [ ] **HG-REINSPECT** → `approved` 后 merge PR  
- [ ] 本地 `pytest tests -m "not intent_eval and not intent_benchmark"` 绿（回归）

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

> **由 00（`kpi_aggregator: 00`）关账轮填写**；格式见 [`KPI_RUBRIC_v1_2.md`](../../harness/guides/KPI_RUBRIC_v1_2.md) §4.3–§6。

（占位 · 执行后删除本行）

---

## 11. ### 自检结论（执行者）

（40 帽回填）

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-31 | v0.1 草案：路线 B · gate 预批 · 暂不执行 |
| 2026-05-31 | v0.2：`kpi_aggregator: 00` · §9 拍板 · `pending` 待新会话 00 开帽 |

---

## 给 Cursor

`harness-kpi-v1-2-pilot`、`KPI_RUBRIC_v1_2`、`kpi_aggregator:00`、`00-orchestrator`、路线 B、非 Loop
