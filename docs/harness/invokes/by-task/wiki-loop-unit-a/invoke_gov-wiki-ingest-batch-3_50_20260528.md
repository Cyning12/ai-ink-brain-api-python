# Invoke · gov-wiki-ingest-batch-3 · 50 · R3

| 项 | 值 |
| --- | --- |
| **round** | R3 |
| **hat** | 50 |
| **task** | `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md` |
| **task_slug** | `gov-wiki-ingest-batch-3` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 40（自检已 commit @ c32ff5d） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 40 已结束；本帽为 50 独立复检帽，只按下文执行。

执行 Wiki Loop 单元 A · R3 · 50 复检。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only。
task: docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md
task_slug: gov-wiki-ingest-batch-3
freeze_id: GOV-WIKI-INGEST-BATCH-3@2026-05-28

**复检步骤**
1. 独立 diff 审查（git diff HEAD~3），非复读 40 结论
2. 逐文件核对 5 篇 synthesis frontmatter 格式
3. 范围审查（确认无 api/tests/tools 改动）
4. 产出 docs/tasks/reinspect_results/reinspect_gov-wiki-ingest-batch-3_*.md
5. 落盘 50 invoke + commit
6. 无阻塞则关账

**产出路径**
- reinspect: docs/tasks/reinspect_results/reinspect_gov-wiki-ingest-batch-3_20260528_v1.md
```

---

## 复检执行摘要

- diff_range: HEAD~3..HEAD（c933f5d → c32ff5d）
- 12 文件改动，+400/-3
- 5 篇新 synthesis + index/log 更新
- 结论：复检通过 · 可关账
