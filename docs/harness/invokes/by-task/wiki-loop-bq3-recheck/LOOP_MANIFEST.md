# Loop Manifest · B-Q3 Recheck（R1–R3 + META）

> **git_branch**（各 round 相同）：`task/wiki-loop-bq3-recheck-v1`  
> **母 task**：`docs/tasks/active/task_harness_wiki_loop_bq3_recheck_v1.md`（三轮完成后 META 关账）  
> **全链启动**：[`PROMPT_START_loop_bq3_full_chain_v1.md`](./PROMPT_START_loop_bq3_full_chain_v1.md)（【授权】cross-round **仅**在此）  
> **前置**：Loop A1–A4 **done** · synthesis 已含 `test_strategy: recommended`（`query-rewrite-observability`）

| round | task_path（active → done） | task_slug | freeze_id | 上一轮回填 | 关账后须回填 |
|-------|---------------------------|-----------|-----------|------------|--------------|
| **R1** | `docs/tasks/active/task_wiki_ctx_ab_multi_bq3_recheck_v1.md` | `wiki-bq3-r1-payload-scorecard` | `WIKI-BQ3-R1-PAYLOAD@2026-05-26` | — | R2：`<!-- PLACEHOLDER:R1_OUTCOME -->` |
| **R2** | `docs/tasks/active/task_wiki_ctx_ab_multi_conclusion_bq3_sync_v1.md` | `wiki-bq3-r2-conclusion` | `WIKI-BQ3-R2-CONCLUSION@2026-05-26` | `R1_OUTCOME` | R3：`<!-- PLACEHOLDER:R2_OUTCOME -->`（可选） |
| **R3** | `docs/tasks/active/task_governance_wiki_bq3_spec_schedule_sync_v1.md` | `wiki-bq3-r3-gov-sync` | `GOV-WIKI-BQ3-SYNC@2026-05-26` | — | — |
| **META** | `docs/tasks/active/task_harness_wiki_loop_bq3_recheck_v1.md` | `wiki-loop-bq3-recheck` | `WIKI-LOOP-BQ3-RECHECK@2026-05-26` | 三轮均 `done/` | — |

**依赖**：`docs/coding_wiki/syntheses/query-rewrite-observability.md` 含 `test_strategy`；Multi 原 scorecard **不删改主表**，R1 增 **§Recheck** addendum。
