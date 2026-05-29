# Task Schedule Read Smoke — 题集与 gold 要点

> **freeze_id**：`TASK-SCHEDULE-READ-SMOKE@2026-05-29`  
> **快照**：`GOV-TASK-SCHEDULE-WIKI@2026-05-29` 合入后

---

## Q1 · 当前后端实现优先棒

**题面**：见 PROMPT §3 Q1。

**gold 要点**（命中 ≥2 项即 pass）

| # | 要点 |
| --- | --- |
| G1 | 指向 **`task_chatbi_v3_p2_resilience_rate_limit_v1`**（P2-1b 限流）或同义「ChatBI V3 P2-1b 限流」 |
| G2 | 依据来自 **RECENT** 和/或 **task-schedule hub** 和/或 P2-1b task 头 `schedule_ref` /「当前棒」类表述 |
| G3 | **非** Wiki 治理 / T4 ops / Batch-4 作为「下一实现项」（可提及已 done，但不作为当前实现棒） |

**fail 例**：答 GraphRAG 探索、低置信 backlog、或「Wiki lint CI」为下一实现优先。

---

## Q2 · P2-1b vs P2-1c 先后

**gold 要点**

| # | 要点 |
| --- | --- |
| G1 | **限流（P2-1b）先于熔断（P2-1c）** |
| G2 | 依据：`blocked_by` P2-1a done · 或 RECENT §1.1 顺序 · 或 P2-1b 头 `blocks: P2-1c` |
| G3 | 未声称「可并行无依赖」且无文档依据 |

---

## Q3 · L1 vs L2 排期分工

**gold 要点**

| # | 要点 |
| --- | --- |
| G1 | **排期真值 = L1**：`docs/tasks/RECENT_TASK_SCHEDULE.md`（或等价表述「RECENT 排期表」） |
| G2 | **Wiki / coding_wiki = L2 导航/摘要**，不替代 RECENT（可提 `task-schedule-ink-backend` concept 为 hub） |
| G3 | 未把 `syntheses/` 单页或 `CODING_WIKI.md` 标为排期唯一真值 |

---

## Q4 · 陷阱：Wiki 治理是否仍为当前棒

**gold 要点**

| # | 要点 |
| --- | --- |
| G1 | Wiki 治理 / T4 ops **已收口 done**（#83 或 milestone 类表述均可） |
| G2 | **业务当前棒 = V3 P2-1b**（或 RECENT §0 同义） |
| G3 | 未答「Wiki 仍是当前棒」或「应先做 Batch-4/P3 lint」作为 **唯一** 下一棒（提可选后续可以，但须区分优先级） |

---

## 观测项（可选 · 不作 pass 硬门禁）

| 项 | 记录 |
| --- | --- |
| 首读路径 | |
| 是否打开 task-schedule concept | 是 / 否 |
| 是否打开 RECENT | 是 / 否 |
| 是否误读 Roadmap SPEC 为当前棒 | 是 / 否 |
