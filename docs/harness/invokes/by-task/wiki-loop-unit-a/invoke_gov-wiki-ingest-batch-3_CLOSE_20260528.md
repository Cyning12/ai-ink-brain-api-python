# Invoke · gov-wiki-ingest-batch-3 · CLOSE · R3

| 项 | 值 |
| --- | --- |
| **round** | R3 |
| **hat** | CLOSE（关账） |
| **task** | `docs/tasks/done/task_governance_wiki_ingest_batch_3_v1.md` |
| **task_slug** | `gov-wiki-ingest-batch-3` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |

---

## 执行路线与 Commit 回溯（HANDOFF_CLOSE_TRACE）

```text
Wiki Loop 单元 A · R3 · gov-wiki-ingest-batch-3 · 关账
分支: task/wiki-unit-ab-plan-v1
Freeze: GOV-WIKI-INGEST-BATCH-3@2026-05-28

执行路线:
  22 审核 → 30 执行 → 40 自检 → 50 复检 → 关账

Commit 回溯:
  c933f5d docs(harness): 22 R3 审核落盘 + invoke
  965d834 docs(wiki): 30 Batch-3 ingest · 5 slug · syntheses 25
  c32ff5d docs(harness): 40 R3 自检落盘 + task 回填
  d04e9a7 docs(harness): 50 R3 复检落盘
  [当前] 关账 commit
          └─ git mv: task_governance_wiki_ingest_batch_3_v1.md → done/
          └─ _views/done.md 追加
          └─ task 头部: pending → done(2026-05-28)

关账后状态:
  - task: docs/tasks/done/task_governance_wiki_ingest_batch_3_v1.md
  - review: docs/harness/reviews/by-task/gov-wiki-ingest-batch-3/
  - reinspect: docs/tasks/reinspect_results/reinspect_gov-wiki-ingest-batch-3_20260528_v1.md
  - invokes: docs/harness/invokes/by-task/wiki-loop-unit-a/invoke_gov-wiki-ingest-batch-3_{22,30,40,50,CLOSE}_20260528.md
```

---

## 下一 round

按 LOOP_MANIFEST：R3 关账后继续 **META**（母单 `wiki-loop-unit-a`）。
- task: `docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md`
- slug: `wiki-loop-unit-a`
- freeze_id: `WIKI-LOOP-UNIT-A@2026-05-28`
