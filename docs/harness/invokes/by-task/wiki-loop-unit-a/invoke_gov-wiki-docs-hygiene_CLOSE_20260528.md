# Invoke · gov-wiki-docs-hygiene · CLOSE · R1

| 项 | 值 |
| --- | --- |
| **round** | R1 |
| **hat** | CLOSE（关账） |
| **task** | `docs/tasks/done/task_governance_wiki_docs_hygiene_v1.md` |
| **task_slug** | `gov-wiki-docs-hygiene` |
| **freeze_id** | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |

---

## 执行路线与 Commit 回溯（HANDOFF_CLOSE_TRACE）

```text
Wiki Loop 单元 A · R1 · gov-wiki-docs-hygiene · 关账
分支: task/wiki-unit-ab-plan-v1
Freeze: GOV-WIKI-DOCS-HYGIENE@2026-05-28

执行路线:
  22 审核 → 30 执行 → 40 自检 → 50 复检 → 关账

Commit 回溯:
  bf15688 docs(harness): 22 R1 审核落盘 + invoke
          └─ review: docs/harness/reviews/by-task/gov-wiki-docs-hygiene/
          └─ invoke: invoke_gov-wiki-docs-hygiene_22_20260528.md

  9a58509 docs(wiki): 30 文档 hygiene 同步
          └─ WIKI_REQUIREMENTS_COMPARISON_v1_zh.md (v1.4)
          └─ SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md (done/ 链接)
          └─ RECENT_TASK_SCHEDULE.md (Unit A in_progress)
          └─ SPEC-Governance-Wiki-Harness-Roadmap-v1.md (A/B 双 PR)
          └─ invoke: invoke_gov-wiki-docs-hygiene_30_20260528.md

  0081e5e docs(harness): 40 R1 自检落盘 + task 回填
          └─ invoke: invoke_gov-wiki-docs-hygiene_40_20260528.md
          └─ task: 自检结论回填

  e33f726 docs(harness): 50 R1 复检落盘
          └─ reinspect: docs/tasks/reinspect_results/reinspect_gov-wiki-docs-hygiene_20260528_v1.md
          └─ invoke: invoke_gov-wiki-docs-hygiene_50_20260528.md

  [当前] 关账 commit
          └─ git mv: task_governance_wiki_docs_hygiene_v1.md → done/
          └─ _views/done.md 追加
          └─ task 头部: pending → done(2026-05-28)

关账后状态:
  - task: docs/tasks/done/task_governance_wiki_docs_hygiene_v1.md
  - review: docs/harness/reviews/by-task/gov-wiki-docs-hygiene/
  - reinspect: docs/tasks/reinspect_results/reinspect_gov-wiki-docs-hygiene_20260528_v1.md
  - invokes: docs/harness/invokes/by-task/wiki-loop-unit-a/invoke_gov-wiki-docs-hygiene_{22,30,40,50,CLOSE}_20260528.md
```

---

## 下一 round

按 LOOP_MANIFEST：R1 关账后继续 **R2**（`gov-wiki-t4-rollout`）。
- task: `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md`
- slug: `gov-wiki-t4-rollout`
- freeze_id: `GOV-WIKI-T4-ROLLOUT@2026-05-28`
