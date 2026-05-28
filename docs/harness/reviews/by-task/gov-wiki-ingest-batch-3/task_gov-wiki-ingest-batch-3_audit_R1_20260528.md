# 22 任务审核 — gov-wiki-ingest-batch-3 · R3

| 项 | 值 |
| --- | --- |
| **task** | `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md` |
| **task_slug** | `gov-wiki-ingest-batch-3` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **round** | R3（单元 A） |
| **audit_profile** | post_close |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **human_gate** | HG-LOOP-BATCH approved · HG-INGEST-BATCH-3-SCOPE approved（母单） |
| **review_date** | 2026-05-28 |

---

## 审查结论摘要

**零阻塞 · 可进入 30 执行帽**

本 task 为 Wiki ingest 批量（5 slug），来源 task 均在 `done/`，test_strategy: not_applicable 合理。R1/R2 已在 `done/`。

---

## 已核对项

| # | 检查项 | 结论 | 说明 |
| --- | --- | --- | --- |
| 1 | human_gate | pass | HG-LOOP-BATCH approved；HG-INGEST-BATCH-3-SCOPE approved |
| 2 | 范围 | pass | 仅改 `docs/coding_wiki/`；不改 api/tests/tools |
| 3 | 前置 R1/R2 | pass | 均已在 `done/` |
| 4 | 来源 task 存在性 | pass | 5 个 task 全部在 `done/` |
| 5 | SPEC | pass | `SPEC-Governance-Wiki-Ingest-Batch-3-v1.md` 存在 |

---

## 签收 / 关闭

**结论：可执行**

---

## 下一棒可复制 Prompt

```text
执行 Wiki Loop 单元 A · R3 · 30→40→50→关账。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only · 禁止 api/tests/tools。

task: docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md
task_slug: gov-wiki-ingest-batch-3
freeze_id: GOV-WIKI-INGEST-BATCH-3@2026-05-28
semi_auto: true

**范围（5 slug ingest · 累计 syntheses ≥25）**

1. 读取 5 个 source task（docs/tasks/done/），各产出 1 篇 synthesis
2. 新 synthesis 优先补 `graph_nodes`（种子 id 或 `[]`）
3. 更新 `docs/coding_wiki/index.md`（分类目录）
4. 更新 `docs/coding_wiki/log.md`（追加时间线）

**5 slug 名单**
- harness-wiki-loop-a1-a4 → `task_harness_wiki_loop_a1_a4_v1`
- harness-wiki-loop-bq3-recheck → `task_harness_wiki_loop_bq3_recheck_v1`
- coding-wiki-ingest-test-strategy → `task_coding_wiki_ingest_test_strategy_v1`
- governance-recent-schedule-wiki-sync → `task_governance_recent_schedule_wiki_sync_v1`
- wiki-ctx-ab-multi-bq3-recheck → `task_wiki_ctx_ab_multi_bq3_recheck_v1`

**执行纪律**
- ingest 仅 done task；禁止复制 review/SPEC 全文
- 每篇 synthesis ≤2 页；pointer + 摘要
- 每帽 commit 后再戴下一帽
```
