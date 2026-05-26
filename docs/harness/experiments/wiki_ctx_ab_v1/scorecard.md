# Wiki-CTX-AB v1 — Scorecard

| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **model** | `claude-opus-4-7` |
| **date** | 2026-05-25 |

---

## P1 · H-full vs H-lean

**slug**：`harness-p1-docs-consolidation`

| 题 | 臂 | payload_char_count | 正确性 (pass/fail) | 幻觉/漏读 | 备注 |
| --- | --- | --- | --- | --- | --- |
| Q1 | H-full | 15928 | **pass** | 无 | 命中 P1-3（human_gate 速查）+ P1-2（6 类 SKILL） |
| Q1 | H-lean | 9896 | **pass** | 无 | 命中 P1-3 + P1-2（done task 全文提供足够信息） |
| Q2 | H-full | — | **pass** | 无 | `not_applicable` + 纯文档治理理由 |
| Q2 | H-lean | — | **pass** | 无 | 同上 |
| Q3 | H-full | — | **pass** | 无 | `HARNESS-P1-DOCS@2026-05-23` + `2026-05-23` |
| Q3 | H-lean | — | **pass** | 无 | 同上 |
| Q4 | H-full | — | **pass** | 无 | 答「不在范围」+ 依据为非范围/工作区 pointer |
| Q4 | H-lean | — | **pass** | 无 | 答「不在范围」+ 依据为非范围/工作区 pointer |

**P1 汇总**

| 指标 | H-full | H-lean | 降幅 |
| --- | --- | --- | --- |
| 总 char（四题载荷之和或均值） | 15928 | 9896 | **37.9%** |
| 正确题数 / 4 | 4/4 | 4/4 | 0（持平） |

**结论草稿**：T7（37.9% ≥ 30%）+ T8（4/4 = 4/4）同时满足 → 推荐推进 Harness taxonomy 全仓推广（T3）

---

## 逐题回答原文（三方 Agent 交付物）

### Q1 · H-full

> 本 Epic（`task_harness_p1_docs_consolidation_v1`）在 **范围** 内必须完成的两项文档交付是什么？请各用一句话说明路径。

1. **P1-3**：更新 `docs/tasks/README.md`，新增 `human_gate` 场景速查表（含 `gate_id`、`status`、`blocks_hats`、`典型场景`、`谁改 approved` 五列）。
2. **P1-2**：新增目录 `docs/tasks/skills/` 与 `docs/tasks/skills/README.md`，定义 6 类 SKILL（含关账蒸馏与人审口径）。

（加分项：`docs/tasks/README.md` 已补充到 `docs/tasks/skills/README.md` 的入口链接。）

---

### Q1 · H-lean

> 本 Epic（`task_harness_p1_docs_consolidation_v1`）在 **范围** 内必须完成的两项文档交付是什么？请各用一句话说明路径。

1. **P1-3**：更新 `docs/tasks/README.md`，新增 `human_gate` 场景速查表（含 `gate_id`、`status`、`blocks_hats`、`典型场景`、`谁改 approved` 五列）。
2. **P1-2**：新增目录 `docs/tasks/skills/` 与 `docs/tasks/skills/README.md`，定义 6 类 SKILL（含关账蒸馏与人审口径）。

（加分项：`docs/tasks/README.md` 已补充到 `docs/tasks/skills/README.md` 的入口链接。）

---

### Q2 · H-full

> 该 done task 头部 `test_strategy` 取值是什么？`test_strategy_note` 用一句话说明原因。

- `test_strategy` = **`not_applicable`**
- 原因：纯文档治理改动（`docs/tasks/` 下 README 与 skills 目录），不涉及运行时代码、API、SQL、CI 行为变更。

---

### Q2 · H-lean

> 该 done task 头部 `test_strategy` 取值是什么？`test_strategy_note` 用一句话说明原因。

- `test_strategy` = **`not_applicable`**
- 原因：纯文档治理改动（`docs/tasks/` 下 README 与 skills 目录），不涉及运行时代码、API、SQL、CI 行为变更。

---

### Q3 · H-full

> 该 task 的 `freeze_id` 是什么？状态行显示的关账日期（YYYY-MM-DD）？

- `freeze_id` = **`HARNESS-P1-DOCS@2026-05-23`**
- 关账日期：**`2026-05-23`**（状态行：`done（2026-05-23 验收通过 · HG-REINSPECT 人签）`）

---

### Q3 · H-lean

> 该 task 的 `freeze_id` 是什么？状态行显示的关账日期（YYYY-MM-DD）？

- `freeze_id` = **`HARNESS-P1-DOCS@2026-05-23`**
- 关账日期：**`2026-05-23`**（状态行：`done（2026-05-23 验收通过 · HG-REINSPECT 人签）`）

---

### Q4 · H-full

> `RECENT_TASK_SCHEDULE` §0.4 中的 **P1-1**（工作区 reviews pointer）是否在本 task 的 **范围** 内？为什么？

**不在**本 task 范围内。

依据：task **非范围** 明确列出「`Projects/docs/harness/reviews/` pointer 调整（P1-1，工作区仓）」；此外 `RECENT_TASK_SCHEDULE` §0.4 中 P1-1 的说明也指向工作区 `Projects/docs/harness/reviews/`，不在本后端仓 `ai-ink-brain-api-python` 的交付范围内。

---

### Q4 · H-lean

> `RECENT_TASK_SCHEDULE` §0.4 中的 **P1-1**（工作区 reviews pointer）是否在本 task 的 **范围** 内？为什么？

**不在**本 task 范围内。

依据：task **非范围** 明确列出「`Projects/docs/harness/reviews/` pointer 调整（P1-1，工作区仓）」；此外 `RECENT_TASK_SCHEDULE` §0.4 中 P1-1 的说明也指向工作区 `Projects/docs/harness/reviews/`，不在本后端仓 `ai-ink-brain-api-python` 的交付范围内。

---

## P2 · H-lean vs W（T1b 后填）

| 题 | 臂 | payload_char_count | 正确性 | 备注 |
| --- | --- | --- | --- | --- |
| Q1 | H-lean | | | |
| Q1 | W | | | |
| … | | | | |

**结论草稿**：（链 `conclusion_p2_zh.md`）
