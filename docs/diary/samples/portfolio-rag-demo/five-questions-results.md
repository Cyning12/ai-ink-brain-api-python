# 五问验收记录 · W5（Tranche 1 · UI 终态）

| 项 | 值 |
| --- | --- |
| **task** | `docs/tasks/done/task_portfolio_rag_demo_v1.md` |
| **RUNBOOK** | `docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md` §4–§6 |
| **sync** | ✅ **HG-W5-SYNC** · job `c44158a5-…` · 2026-06-03 |
| **五问闸** | ✅ **HG-W5-FIVE-Q approved**（本表 UI 证据齐 · 已人签 2026-06-03） |
| **Tranche 1 日期** | 2026-06-03 |

> **口径**：RUNBOOK 终态须 **5/5 pass**、sources **≥4/5**、Q1/Q5 **双跑 category 一致**。P1 可选项见 [`w5-retest-backlog.md`](./w5-retest-backlog.md)。

## 汇总

| 指标 | Tranche 1 | RUNBOOK 终态 |
| --- | --- | --- |
| 问句非空切题 | **5/5 pass** | 5/5 |
| sources ≥4/5 | **5/5** | ≥4/5 |
| Q3 evidence-only | ✅ | 必须 |
| Q1/Q5 双跑一致 | ✅ Q1 · ✅ Q5 | 必须 |
| **HG-W5-FIVE-Q** | **已人签 2026-06-03** | approved |

## 逐问记录

| ID | 问句（逐字） | 结果 | 重试 | 主 category / 要点 | 证据 |
| --- | --- | --- | --- | --- | --- |
| **Q1** | 《AI 编程可闭环协作》**卷三**讲什么？Harness 和签收是什么？ | ✅ **pass** | 0 | `methodology` · vol3 | `[q1-sources-run1.json](./q1-sources-run1.json)` · `[q1-sources-run2.json](./q1-sources-run2.json)` · [run1 截图](./screenshots/q1-vol3-harness-run1-execution-trace-20260603.png) |
| **Q2** | **RAG 混合检索**怎么做的？ | ✅ **pass** | 0 | `resume/*` · 混合检索+rerank | `[q2-sources-run1.json](./q2-sources-run1.json)` · [截图](./screenshots/q2-hybrid-rag-success-execution-trace-20260603.png) · run `50f48bd8…` |
| **Q3** | **冷/温/热** 和 **架构三层** 区别？ | ✅ **pass** | 0 | `evidence/*` | `[q3-sources-run1.json](./q3-sources-run1.json)` · [截图](./screenshots/q3-cold-warm-hot-execution-trace-20260603.png) |
| **Q4** | **11 年经历**里 AI Coding 相关成果？ | ✅ **pass** | 0 | `resume/*` | `[q4-sources-run1.json](./q4-sources-run1.json)` |
| **Q5** | 按需读图相对整图灌入 **token/效果**？**边界**？ | ✅ **pass** | 0 | Top `evidence/evidence-card.md` · 答含 **~1/9** + 边界 | `[q5-sources-run1.json](./q5-sources-run1.json)` · `[q5-sources-run2.json](./q5-sources-run2.json)` · run1 `7b456d7f…` / run2 `ded2dec5…` · [run1](./screenshots/q5-evidence-card-run1-execution-trace-20260603.png) · [run2](./screenshots/q5-evidence-card-run2-execution-trace-20260603.png) |

## Sync（G-W5-1 · 已签）

[`sync-job-summary.md`](./sync-job-summary.md) · [`sync-job-final.json`](./sync-job-final.json).

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-03 | Tranche 1 UI 五问落盘 · Q5 对齐 evidence-card 双跑 |
| 2026-06-03 | 修正 Q5 逐问行（原 partial/旧 run 已作废） |
