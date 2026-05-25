# Wiki-CTX-AB v1 — Gold 题集（P1 · 锁定）

| 项 | 值 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **phase** | **P1 only**（H-full vs H-lean） |
| **task_slug** | `harness-p1-docs-consolidation` |
| **done task** | `docs/tasks/done/task_harness_p1_docs_consolidation_v1.md` |
| **invoke 目录** | `docs/harness/invokes/by-task/harness-p1-docs-consolidation/` |
| **review 目录** | `docs/harness/reviews/by-task/`（本 Epic **无** 独立 review 子目录时，H-full 仅含 invoke + done task） |

> **跑法**：每题对 **H-full**、**H-lean** 各答一次；载荷仅允许对应 `payloads/H-*_harness-p1-docs-consolidation.md` 内列出的文件（或该文件已内联的全文）。记录答案与 `payload_char_count` 填入 `scorecard.md`。

---

## Q1 — 本 Epic 两项交付物

**提问（原文，勿改）**

> 本 Epic（`task_harness_p1_docs_consolidation_v1`）在 **范围** 内必须完成的两项文档交付是什么？请各用一句话说明路径。

**标准答案要点（人工勾选 pass/fail）**

| # | 要点 |
| --- | --- |
| 1 | **P1-3**：更新 `docs/tasks/README.md`，含 **`human_gate` 场景速查表**（含 `gate_id`、`status`、`blocks_hats` 等字段） |
| 2 | **P1-2**：新增 `docs/tasks/skills/README.md`，定义 **6 类 SKILL**（关账蒸馏 + 人审口径） |
| 3 | （加分）`docs/tasks/README.md` 有链到 `docs/tasks/skills/README.md` 的入口 |

**拒答**：若答案出现未在载荷中出现的其他 Epic 名称或路径，记 **幻觉**。

---

## Q2 — 本 task 的 test_strategy

**提问**

> 该 done task 头部 `test_strategy` 取值是什么？`test_strategy_note` 用一句话说明原因。

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | `test_strategy` = **`not_applicable`** |
| 2 | 理由含：**纯文档治理** / 不涉及运行时代码、API、CI 行为变更（表述不必逐字） |

---

## Q3 — freeze_id 与关账日期

**提问**

> 该 task 的 `freeze_id` 是什么？状态行显示的关账日期（YYYY-MM-DD）？

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | `freeze_id` = **`HARNESS-P1-DOCS@2026-05-23`** |
| 2 | 关账：**2026-05-23**（验收通过 / done） |

---

## Q4 — P1-1 是否在本 Epic 范围（陷阱题）

**提问**

> `RECENT_TASK_SCHEDULE` §0.4 中的 **P1-1**（工作区 reviews pointer）是否在本 task 的 **范围** 内？为什么？

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | **不在** 本 Epic 范围内 |
| 2 | 依据：task **非范围** 写明 P1-1 属工作区 `Projects/docs/harness/reviews/`（或等价表述） |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | v1：P1 四题；slug `harness-p1-docs-consolidation` |
