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

**Claude Code 全链入口（单 task · 范例）**：

| task_slug | 目录 |
|-----------|------|
| `gov-wiki-t4-expand` | `docs/harness/invokes/by-task/gov-wiki-t4-expand/PROMPT_START_full_chain_v1.md` |
| `gov-l2-manifest-ci` | `docs/harness/invokes/by-task/gov-l2-manifest-ci/PROMPT_START_full_chain_v1.md` |
| `gov-wiki-agent-readorder` | `docs/harness/invokes/by-task/gov-wiki-agent-readorder/PROMPT_START_full_chain_v1.md` |
| `gov-wiki-ingest-batch` | `docs/harness/invokes/by-task/gov-wiki-ingest-batch/PROMPT_START_full_chain_v1.md` |

**已执行后 hygiene / 复盘**（非 START）：

| task_slug | 文件 |
|-----------|------|
| `gov-wiki-t4-expand` | `docs/harness/invokes/by-task/gov-wiki-t4-expand/PROMPT_RETRO_hygiene_bc_v1.md` |

模式：`PROMPT_START_full_chain_v1.md`（一次粘贴）+ `PROMPT_TASK_22_to_CLOSE_v1.md`（§3 逐步帽链）；**非** Loop 的 `PROMPT_LOOP` / `HG-LOOP-BATCH`。

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

## 单 task 合规自检（ST1–ST6 · 关账前必过）

> **蒸馏来源**：gov-wiki-t4-expand 复盘（2026-05-27）。**缺任一项 = 不得关账**（与 loop-batch C2 同级精神，非 C1–C7 全表）。

| # | 检查 | pass 条件 |
|---|------|-----------|
| **ST1** | **22** | `reviews/by-task/<slug>/` 有 R1 audit；`invoke_*_22_*` 存在 · §3 ≥15 行 |
| **ST2** | **30** | `invoke_*_30_*` 存在 · 与 git 业务 commit 可对应 |
| **ST3** | **40** | `invoke_*_40_*` + task §自检结论已回填 |
| **ST4** | **50** | `reinspect_<slug>_YYYYMMDD_vN.md` + `invoke_*_50_*` |
| **ST5** | **关账** | task 头部 `done（…）` · `git mv` done/ · `_views/done.md` · `invoke_*_CLOSE_*` |
| **ST6** | **索引** | RECENT §6.6/§8 · docs-governance H1–H5；invoke **无** `round: R1` 等 Loop 字段 |

**禁止跳帽**：不得在未落盘当前帽 invoke + commit 的情况下进入下一帽（即使 semi_auto）。

**Claude Code**：关账前须显式勾选 ST1–ST6；见各 task `PROMPT_START` §关账前自检。

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
| 2026-05-27 | v1.1：Claude Code 范例 · PROMPT_START + PROMPT_TASK_22_to_CLOSE（gov-wiki-t4-expand / gov-l2-manifest-ci） |
| 2026-05-27 | v1.2：§ST1–ST6 单 task 合规自检 · PROMPT_RETRO 与 START 分工 · gov-wiki-t4-expand 复盘 |

---

## 给 Cursor

`harness-task`、单 task、22、30、40、50、semi_auto、HANDOFF、非 Loop
