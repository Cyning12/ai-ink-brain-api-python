# Invoke · gov-wiki-t4-rollout · CLOSE · R2

| 项 | 值 |
| --- | --- |
| **round** | R2 |
| **hat** | CLOSE（关账） |
| **task** | `docs/tasks/done/task_governance_wiki_t4_rollout_v1.md` |
| **task_slug** | `gov-wiki-t4-rollout` |
| **freeze_id** | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |

---

## 执行路线与 Commit 回溯（HANDOFF_CLOSE_TRACE）

```text
Wiki Loop 单元 A · R2 · gov-wiki-t4-rollout · 关账
分支: task/wiki-unit-ab-plan-v1
Freeze: GOV-WIKI-T4-ROLLOUT@2026-05-28

执行路线:
  22 审核 → 30 执行 → 40 自检 → 50 复检 → 关账

Commit 回溯:
  e14a08b docs(harness): 22 R2 审核落盘 + invoke
          └─ review: docs/harness/reviews/by-task/gov-wiki-t4-rollout/
          └─ invoke: invoke_gov-wiki-t4-rollout_22_20260528.md

  a500b96 docs(wiki): 30 T4 graph_nodes 铺量 · 14 篇 synthesis
          └─ 14 篇 frontmatter 修改
          └─ invoke: invoke_gov-wiki-t4-rollout_30_20260528.md

  a5a86a4 docs(harness): 40 R2 自检落盘 + task 回填
          └─ invoke: invoke_gov-wiki-t4-rollout_40_20260528.md
          └─ task: 自检结论回填

  a838c65 docs(harness): 50 R2 复检落盘
          └─ reinspect: docs/tasks/reinspect_results/reinspect_gov-wiki-t4-rollout_20260528_v1.md
          └─ invoke: invoke_gov-wiki-t4-rollout_50_20260528.md

  [当前] 关账 commit
          └─ git mv: task_governance_wiki_t4_rollout_v1.md → done/
          └─ _views/done.md 追加
          └─ task 头部: pending → done(2026-05-28)

关账后状态:
  - task: docs/tasks/done/task_governance_wiki_t4_rollout_v1.md
  - review: docs/harness/reviews/by-task/gov-wiki-t4-rollout/
  - reinspect: docs/tasks/reinspect_results/reinspect_gov-wiki-t4-rollout_20260528_v1.md
  - invokes: docs/harness/invokes/by-task/wiki-loop-unit-a/invoke_gov-wiki-t4-rollout_{22,30,40,50,CLOSE}_20260528.md
```

---

## 下一 round

按 LOOP_MANIFEST：R2 关账后继续 **R3**（`gov-wiki-ingest-batch-3`）。
- task: `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md`
- slug: `gov-wiki-ingest-batch-3`
- freeze_id: `GOV-WIKI-INGEST-BATCH-3@2026-05-28`
- **注意**：R3 启动前母单 `HG-INGEST-BATCH-3-SCOPE` 须 approved（母单当前 = approved）
