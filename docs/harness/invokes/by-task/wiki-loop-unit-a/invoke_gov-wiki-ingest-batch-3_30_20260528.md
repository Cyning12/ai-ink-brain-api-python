# Invoke · gov-wiki-ingest-batch-3 · 30 · R3

| 项 | 值 |
| --- | --- |
| **round** | R3 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md` |
| **task_slug** | `gov-wiki-ingest-batch-3` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 22（review 已落盘 @ c933f5d） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 22 已结束；本帽为 30 执行帽，只按下文执行。

执行 Wiki Loop 单元 A · R3 · 30 ingest 批量。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only · 禁止 api/tests/tools。
task: docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md
task_slug: gov-wiki-ingest-batch-3
freeze_id: GOV-WIKI-INGEST-BATCH-3@2026-05-28

**范围（5 slug ingest · 累计 syntheses ≥25）**

1. 从 5 个 source task 产出 synthesis（docs/coding_wiki/syntheses/）
2. 新 synthesis 补 graph_nodes frontmatter
3. 更新 index.md（分类目录）
4. 更新 log.md（追加时间线）

**5 slug 名单与 freeze_id**
- harness-wiki-loop-a1-a4 → WIKI-LOOP-A1-A4@2026-05-26
- harness-wiki-loop-bq3-recheck → WIKI-LOOP-BQ3-RECHECK@2026-05-26
- coding-wiki-ingest-test-strategy → CODING-WIKI-A1-TEST-STRATEGY@2026-05-26
- governance-recent-schedule-wiki-sync → GOV-WIKI-A4-SCHEDULE@2026-05-26
- wiki-ctx-ab-multi-bq3-recheck → WIKI-BQ3-R1-PAYLOAD@2026-05-26

**执行纪律**
- ingest 仅 done task；禁止复制 review/SPEC 全文
- 每篇 synthesis ≤2 页；pointer + 摘要
- 每帽 commit 后再戴下一帽
```

---

## 执行记录

### 已创建 synthesis

| slug | source_task | graph_nodes |
| --- | --- | --- |
| harness-wiki-loop-a1-a4 | task_harness_wiki_loop_a1_a4_v1 | `[{id: E2E_DOC, relation: documents}]` |
| harness-wiki-loop-bq3-recheck | task_harness_wiki_loop_bq3_recheck_v1 | `[{id: CR1, relation: evidence}]` |
| coding-wiki-ingest-test-strategy | task_coding_wiki_ingest_test_strategy_v1 | `[]` |
| governance-recent-schedule-wiki-sync | task_governance_recent_schedule_wiki_sync_v1 | `[]` |
| wiki-ctx-ab-multi-bq3-recheck | task_wiki_ctx_ab_multi_bq3_recheck_v1 | `[{id: CR1, relation: evidence}]` |

### index.md / log.md 更新

- index.md：新增 5 行 syntheses 索引
- log.md：追加 2026-05-28 batch-ingest-3 条目
