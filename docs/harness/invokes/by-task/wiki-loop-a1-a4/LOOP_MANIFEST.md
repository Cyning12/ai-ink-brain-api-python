# Loop Manifest · A1–A4（每轮执行前替换 PROMPT_LOOP 占位符）

> **git_branch**（四轮相同）：`task/wiki-loop-a1-a4-v1`  
> **母 task**：`docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md`（四轮完成后关账）

| round | task_path（active → done） | task_slug | freeze_id | 上一轮回填本 task 的占位 | 关账后须回填下一 task |
|-------|---------------------------|-----------|-----------|-------------------------|------------------------|
| **A1** | `docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md` | `wiki-a1-ingest-test-strategy` | `CODING-WIKI-A1-TEST-STRATEGY@2026-05-26` | — | A2：`<!-- PLACEHOLDER:A1_OUTCOME -->` |
| **A2** | `docs/tasks/active/task_coding_wiki_schema_test_strategy_rule_v1.md` | `wiki-a2-schema-test-strategy` | `CODING-WIKI-A2-SCHEMA-RULE@2026-05-26` | `A1_OUTCOME` | —（可选 A3 行「见 A1/A2 done」） |
| **A3** | `docs/tasks/active/task_governance_wiki_spec_comparison_sync_v1.md` | `wiki-a3-spec-comparison` | `GOV-WIKI-A3-SPEC-SYNC@2026-05-26` | — | — |
| **A4** | `docs/tasks/active/task_governance_recent_schedule_wiki_sync_v1.md` | `wiki-a4-recent-schedule` | `GOV-WIKI-A4-SCHEDULE@2026-05-26` | — | — |
| **META** | `docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md` | `wiki-loop-a1-a4` | `WIKI-LOOP-A1-A4@2026-05-26` | 四轮均 `done/` | — |

**依赖**：Multi 已合 `main` 或本分支已含 `task_wiki_ctx_ab_multi_slug_v1` done 与 `conclusion_multi_slug_zh.md`。
