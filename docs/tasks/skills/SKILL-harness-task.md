# SKILL：Harness 单 task 帽链（22 → 关账）

> **SKILL ID**：`harness-task`（单 task · 非 Loop）  
> **状态**：`draft` — 蒸馏来源：Harness V2 通则整理（2026-05-27）· 须人审。  
> **适用**：**一个** `docs/tasks/active/task_*.md` 走完整或部分 Harness 帽链。  
> **Loop 勿用本文**：多 round 见 [`SKILL-harness-loop-batch.md`](SKILL-harness-loop-batch.md)。

---

## 何时选用

| 适用 | 不适用 |
|------|--------|
| 单 task · `semi_auto: true` · 22→30→40→50→关账 | 母单 + N 子 task · 单 PR（用 loop-batch） |
| 改 Harness 工件 / prompts / rules（`audit_profile: full`） | 仅改业务代码无 Harness 落盘 |

---

## 帽链真值（读序）

| 序 | 帽 | 入口 |
|----|-----|------|
| 0（可选） | **10** | [`TEMPLATE-requirements-invoke.md`](../../harness/prompts/templates/TEMPLATE-requirements-invoke.md) §3 |
| 1 | **22** | [`22-task-audit.md`](../../harness/prompts/hats/22-task-audit.md) |
| 2 | **30** | [`30-execute-code.md`](../../harness/prompts/hats/30-execute-code.md) |
| 3 | **40** | [`40-self-check.md`](../../harness/prompts/hats/40-self-check.md) |
| 4 | **50** | [`50-independent-reinspect.md`](../../harness/prompts/hats/50-independent-reinspect.md)（按 `test_strategy`） |
| 5 | **关账** | `git mv` → `done/` · [`HANDOFF_CLOSE_TRACE.md`](../../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md) |

**通则（每帽）**：

- [`HANDOFF_SEMI_AUTO.md`](../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md) — semi_auto、人工闸  
- [`HANDOFF_AUTO_COMMIT.md`](../../harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md) — **每帽 commit**  
- [`HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) §5 — task 字段  

**Cursor**：`.cursor/rules/05-harness-semi-auto.mdc` · `.cursor/rules/06-harness-in-repo.mdc`

**非 Cursor Agent**：须 **显式 @ 或粘贴** 上表路径；**无** `.mdc` 自动加载。

---

## task 字段默认值

| 字段 | 单 docs task | 改 Harness 工件 |
|------|--------------|-----------------|
| **test_strategy** | `not_applicable` + note | `not_applicable` 或 `recommended` |
| **semi_auto** | `true` | `true` |
| **audit_profile** | `post_close` | **`full`** |
| **human_gate** | 按场景（`HG-REINSPECT` 等） | 常需 `HG-TASK-DRAFT` / 审 R1 |

任务类型预填（范围/验收）：叠加 [`SKILL-docs-governance.md`](SKILL-docs-governance.md) 等。

---

## `test_strategy` 与 50

| 取值 | 50 | reinspect |
|------|-----|-----------|
| `required` | **必须** | **必须**落盘 `reinspect_results/` |
| `recommended` | **建议** | **建议** |
| `not_applicable` | **可选**（docs 关账常仍做 50） | Loop/docs 子单 **建议** 做 |

---

## 落盘路径

| 帽 | 路径 |
|----|------|
| invoke | `docs/harness/invokes/by-task/<task_slug>/invoke_YYYYMMDD_{22,30,40,50,CLOSE}_*.md` |
| 22 review | `docs/harness/reviews/by-task/<task_slug>/task_*_audit_R1_*.md` |
| 50 | `docs/tasks/reinspect_results/reinspect_<task_slug>_YYYYMMDD_vN.md` |

**invoke 质量**：§3 ≥15 行 · 元信息含 `task_slug`（Loop 同级标准见 loop-batch §C2）。

---

## 关账 checklist

1. §验收 `- [x]` · 头部 `done（日期 · freeze_id）`  
2. `git mv` → `docs/tasks/done/`（与头部 **同一 commit**）  
3. [`_views/done.md`](../_views/done.md) 一行  
4. [`SKILL-docs-governance.md`](SKILL-docs-governance.md) **H1–H5**（PR 前 hygiene）  
5. 对话或 invoke：**HANDOFF_CLOSE_TRACE**（无下一棒时）

---

## 与相关 SKILL

| SKILL | 关系 |
|-------|------|
| [`docs-governance`](SKILL-docs-governance.md) | docs task **内容** + 关账 hygiene |
| [`harness-loop-batch`](SKILL-harness-loop-batch.md) | **N 子 task** · Batch-10 · cross-round |
| [`harness-meta-reinspect`](SKILL-harness-meta-reinspect.md) | 合并后 **流程**元审计 |
| [`pr-post-ci`](SKILL-pr-post-ci.md) | push / 开 PR 后 |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-27 | v1 草案：单 task 帽链索引 + 落盘 + 关账 checklist |

---

## 给 Cursor

`harness-task`、单 task、22、30、40、50、semi_auto、HANDOFF、非 Loop
