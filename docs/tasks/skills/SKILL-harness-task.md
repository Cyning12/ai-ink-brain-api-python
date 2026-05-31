# SKILL：Harness 单 task 帽链（22 → 关账 · 子仓指针）

> **SKILL ID**：`harness-task`  
> **状态**：`active`（2026-05-31）  
> **适用阶段**：**22 起 · 单 task**（非 Loop）；Open **本子仓**执行。  
> **非替代**：[`../../harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) §5 · 各帽 `hats/*.md` 正文 · **Loop** 见 [`SKILL-harness-loop-batch.md`](SKILL-harness-loop-batch.md)

---

## 何时选用

| 适用 | 不适用 |
|------|--------|
| 单 task · `semi_auto: true` · 22→30→40→50→关账 | 母单 + N 子 task · 单 PR（用 loop-batch） |
| 本子仓 `docs/tasks/active/task_*.md` | 工作区 `Projects/docs/harness/tasks/`（跨仓 Harness task） |
| 改 Harness 工件 / prompts / rules | 仅改业务代码且无 Harness 落盘约定 |

---

## Agent 读序

1. **本 task 正文**：`human_gate` · `semi_auto` · `experience_capture` · `test_strategy` · `kpi_rubric`（若有）  
2. **本子仓 Harness 入口**：[`../../harness/README.md`](../../harness/README.md) §1  
3. **帽链顺序**：[`../../harness/SDD_HAT_FLOW.md`](../../harness/SDD_HAT_FLOW.md)  
4. **总则与字段**：[`../../harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) §5  
5. **KPI v1.2**：[`../../harness/guides/KPI_RUBRIC_v1_2.md`](../../harness/guides/KPI_RUBRIC_v1_2.md)  
6. **总调度 00**（编排层 · 可选）：[`../../harness/prompts/hats/00-orchestrator.md`](../../harness/prompts/hats/00-orchestrator.md)

**半自动 / commit / 关账**：

- [`HANDOFF_SEMI_AUTO.md`](../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)  
- [`HANDOFF_AUTO_COMMIT.md`](../../harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md)  
- [`HANDOFF_CLOSE_TRACE.md`](../../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md)

**Cursor 规则**：`.cursor/rules/05-harness-semi-auto.mdc` · `.cursor/rules/06-harness-in-repo.mdc`

---

## Task 扩展字段（摘要 · KPI v1.2）

> 字段语义真值：[`HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) §5；KPI / 00 细则以 [`KPI_RUBRIC_v1_2.md`](../../harness/guides/KPI_RUBRIC_v1_2.md) 为准。

### `experience_capture`（三档 · 无 60 帽）

| 取值 | 含义 | 关账时 |
|------|------|--------|
| `required` | 跨 task 可复用决策/排障/流程教训 | CLOSE 须有 **经验摘要** 或链 `docs/diary/` |
| `recommended` | 建议短摘要 | 关闭回溯 ≥3 bullet |
| `not_applicable` | 无复用经验 | **须** `experience_capture_note` 一行 |

- 各帽 **Judgment** 可建议升/降档位；**22 或人** 改 task 元信息。  
- 判定矩阵：KPI_RUBRIC §6；关账核对：CLOSE_TRACE §4 步骤 6。

### `kpi_rubric` / `### KPI（00）`

- task 可写 **`kpi_rubric: KPI_RUBRIC_v1_2`**（v1.2 起默认口径）。  
- **00 总调度** 或关账轮维护 task **`### KPI（00）`** 表；公式与 D1–D5 **仅以** KPI_RUBRIC 为准。  
- **00** 为编排层，**不**替代 10–50 业务帽。

---

## 帽链真值（索引）

| 序 | 帽 | 入口 |
|----|-----|------|
| 0（可选） | **10** | [`TEMPLATE-requirements-invoke.md`](../../harness/prompts/templates/TEMPLATE-requirements-invoke.md) §3 |
| 1 | **22** | [`22-task-audit.md`](../../harness/prompts/hats/22-task-audit.md) |
| 2 | **30** | [`30-execute-code.md`](../../harness/prompts/hats/30-execute-code.md) |
| 3 | **40** | [`40-self-check.md`](../../harness/prompts/hats/40-self-check.md) |
| 4 | **50** | [`50-independent-reinspect.md`](../../harness/prompts/hats/50-independent-reinspect.md) |
| — | **00** | [`00-orchestrator.md`](../../harness/prompts/hats/00-orchestrator.md)（链外编排 · 可选） |
| 5 | **关账** | `git mv` → `done/` · [`HANDOFF_CLOSE_TRACE.md`](../../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md) |

**通则（每帽）**：下一棒 invoke 落盘 + commit（见 HANDOFF_SEMI_AUTO §3）；`human_gate: pending` **阻塞**对应帽。

---

## Harness 默认值（task 预填）

| 字段 | 单 docs / 轻 task | 改 Harness 工件 / 高风险 |
|------|-------------------|---------------------------|
| **test_strategy** | `not_applicable` + note | `not_applicable` 或 `recommended` |
| **semi_auto** | `true` | `true` |
| **audit_profile** | `post_close` | **`full`** |
| **experience_capture** | `recommended` 或 `not_applicable` | 常 `required` |
| **kpi_rubric** | 可选 `KPI_RUBRIC_v1_2` | 建议显式 |

业务类型预填叠加：[`SKILL-docs-governance.md`](SKILL-docs-governance.md) 等。

---

## `test_strategy` 与 50

| 取值 | 50 | reinspect 落盘 |
|------|-----|----------------|
| `required` | **必须** | **必须** `docs/tasks/reinspect_results/` |
| `recommended` | **建议** | **建议** |
| `not_applicable` | **可选**（docs 关账常仍做 50） | 建议 |

---

## 落盘路径

| 帽 | 路径 |
|----|------|
| invoke | `docs/harness/invokes/by-task/<task_slug>/invoke_YYYYMMDD_{22,30,40,50,CLOSE}_*.md` |
| 22 review | `docs/harness/reviews/by-task/<task_slug>/task_*_audit_R1_*.md` |
| 50 | `docs/tasks/reinspect_results/reinspect_<task_slug>_YYYYMMDD_vN.md` |
| KPI | task 正文 **`### KPI（00）`**（00 或关账轮维护） |

**invoke 质量**：§3 ≥15 行 · 元信息含 `task_slug` / `git_branch`（与 loop-batch C2 同级精神）。

---

## 关账 checklist（最小）

1. §验收 `- [x]` · 头部 `done（日期 · freeze_id）`  
2. `git mv` → `docs/tasks/done/`（与头部 **同一 commit**）  
3. [`_views/done.md`](../_views/done.md) 一行  
4. docs task：[`SKILL-docs-governance.md`](SKILL-docs-governance.md) **H1–H5**  
5. **`experience_capture`** / **`kpi_rubric`**：CLOSE_TRACE §4 步骤 6–7 核对  
6. 对话或 invoke：**HANDOFF_CLOSE_TRACE**（无下一棒时）

---

## 与相关 SKILL

| SKILL | 关系 |
|-------|------|
| [`docs-governance`](SKILL-docs-governance.md) | docs task 内容 + 关账 hygiene |
| [`harness-loop-batch`](SKILL-harness-loop-batch.md) | **N 子 task** · Batch-10 · 勿用本文 |
| [`harness-meta-reinspect`](SKILL-harness-meta-reinspect.md) | 合并后 **流程** 元审计 |
| [`pr-post-ci`](SKILL-pr-post-ci.md) | push / 开 PR 后 |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-27 | v1 草案：单 task 帽链索引 + 落盘 + 关账（蒸馏） |
| 2026-05-31 | v1.1：格式对齐六类 SKILL；KPI v1.2 / 00 / experience_capture 摘要；本仓相对路径 |

---

## 给 Cursor

`harness-task`、单 task、22、30、40、50、00、KPI_RUBRIC_v1_2、semi_auto、experience_capture、非 Loop
