# Invoke · gov-wiki-ingest-batch-3 · 22 · R3

| 项 | 值 |
| --- | --- |
| **round** | R3 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md` |
| **task_slug** | `gov-wiki-ingest-batch-3` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **human_gate** | HG-LOOP-BATCH approved · HG-INGEST-BATCH-3-SCOPE approved |
| **review** | `docs/harness/reviews/by-task/gov-wiki-ingest-batch-3/task_gov-wiki-ingest-batch-3_audit_R1_20260528.md` |

---

## §3 可复制 Prompt

```text
执行 Wiki Loop 单元 A · R3 · 22→关账。分支 task/wiki-unit-ab-plan-v1。
task: docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md
task_slug: gov-wiki-ingest-batch-3
freeze_id: GOV-WIKI-INGEST-BATCH-3@2026-05-28
semi_auto: true · PR-A docs-only · 禁止 api/tests/tools。

帽子：22→30→40→50；落盘 invoke + commit；关账 HANDOFF_CLOSE_TRACE。

**执行步骤**
1. Gate 验证（HG-INGEST-BATCH-3-SCOPE approved）
2. 22 审核 → review 落盘
3. 30 执行：5 slug ingest + index/log 更新
4. 40 自检：syntheses 计数 ≥25
5. 50 复检
6. 关账：git mv → done/ + _views/done.md
```
