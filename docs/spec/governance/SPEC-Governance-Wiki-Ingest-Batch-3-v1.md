# SPEC — 治理：Coding Wiki 批量 Ingest 第三批（5 slug · v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **前置** | Batch-1/2 **done**（syntheses **20**） |
| **单元** | [`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](./SPEC-Governance-Wiki-Unit-AB-Plan-v1.md) · Loop **R3** |
| **Schema** | [`docs/coding_wiki/CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) §4.1 · §4.3 |

---

## 0. 完成态（一句话）

新增 **5** 篇 synthesis，累计 **≥25**；同步 `index.md` · `log.md`；遵守 pointer 纪律（不复制 L1 全文）。

---

## 1. 锁定 ingest 名单（5 · R3 硬交付）

> R3 启动前母单 `HG-INGEST-BATCH-3-SCOPE` 须 **approved**；允许 **±1** 替换须在 invoke 写明理由。

| # | done task | slug | 主题 |
| --- | --- | --- | --- |
| 1 | `docs/tasks/done/task_harness_wiki_loop_a1_a4_v1.md` | `harness-wiki-loop-a1-a4` | Wiki Loop A1–A4 · test_strategy ingest |
| 2 | `docs/tasks/done/task_harness_wiki_loop_bq3_recheck_v1.md` | `harness-wiki-loop-bq3-recheck` | B-Q3 Recheck Loop |
| 3 | `docs/tasks/done/task_coding_wiki_ingest_test_strategy_v1.md` | `coding-wiki-ingest-test-strategy` | A2 test_strategy 规则 ingest |
| 4 | `docs/tasks/done/task_governance_recent_schedule_wiki_sync_v1.md` | `governance-recent-schedule-wiki-sync` | RECENT §6.6 治理同步 |
| 5 | `docs/tasks/done/task_wiki_ctx_ab_multi_bq3_recheck_v1.md` | `wiki-ctx-ab-multi-bq3-recheck` | Multi-slug B-Q3 子 round |

### 1.1 与 Batch-1/2 去重

**禁止** 重复 ingest 已有 20 slug（见 [`docs/coding_wiki/index.md`](../../coding_wiki/index.md) syntheses 表）。

---

## 2. Lint（手工 · 无新脚本）

按 `CODING_WIKI.md` §4.3：frontmatter 完整 · 无 invoke/review 全文 · `source_task` 指向 `done/`。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-28 | v1：Batch-3 五 slug 锁定 |
