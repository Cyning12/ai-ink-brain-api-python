# Invoke · 22 任务审核 · R1 · wiki-bq3-r1-payload-scorecard

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_wiki_ctx_ab_multi_bq3_recheck_v1.md` |
| **task_slug** | `wiki-bq3-r1-payload-scorecard` |
| **freeze_id** | `WIKI-BQ3-R1-PAYLOAD@2026-05-26` |
| **git_branch** | `task/wiki-loop-bq3-recheck-v1` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop B-Q3 Recheck **R1** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/tasks/skills/SKILL-harness-loop-batch.md
- semi_auto: true

【元信息】
- round: R1
- task: docs/tasks/active/task_wiki_ctx_ab_multi_bq3_recheck_v1.md
- task_slug: wiki-bq3-r1-payload-scorecard
- freeze_id: WIKI-BQ3-R1-PAYLOAD@2026-05-26
- git_branch: task/wiki-loop-bq3-recheck-v1
- 母 task: docs/tasks/active/task_harness_wiki_loop_bq3_recheck_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-bq3-recheck/
- cross_round_semi_auto: true

【授权】semi_auto 跨 round：R1 关账后按 MANIFEST 续 R2→R3→META。每帽 invoke + commit。

【commit 硬纪律】每帽结束 before 下一帽：git add → commit → 回复 `已提交：@ <short-hash>`。

硬约束：单 PR · 不改 api/tests/prompts/CI

步骤 0 跳过（R1 无占位回填）。

步骤 1 · 22：审 task §范围/§非范围/§failure_paths；确认继承 HG-LOOP-BATCH；落盘 review；准许 30。
```
