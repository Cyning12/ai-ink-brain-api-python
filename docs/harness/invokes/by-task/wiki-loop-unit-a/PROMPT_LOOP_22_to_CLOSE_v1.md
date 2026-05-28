# Wiki Loop 单元 A · 单 round 22→关账（cc）

> 每 round 复制 §3 到 invoke `docs/harness/invokes/invoke_<task_slug>_<hat>_<date>.md`（或 `by-task/wiki-loop-unit-a/` 下按 round 命名）。

---

## §3 模板（替换 `<ROUND>` / `<TASK_PATH>` / `<SLUG>` / `<FREEZE>`）

```text
执行 Wiki Loop 单元 A · <ROUND> · 22→关账。分支 task/wiki-unit-ab-plan-v1。
task: <TASK_PATH>
task_slug: <SLUG>
freeze_id: <FREEZE>
semi_auto: true · PR-A docs-only · 禁止 api/tests/tools。

帽子：22→30→40→50；落盘 invoke + commit；关账 HANDOFF_CLOSE_TRACE。
R3 额外：Batch-3 五 slug 见 SPEC-Governance-Wiki-Ingest-Batch-3-v1.md §1。
```

### R1 填表

| 占位 | 值 |
|------|-----|
| ROUND | R1 |
| TASK_PATH | `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md` |
| SLUG | `gov-wiki-docs-hygiene` |
| FREEZE | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |

### R2 填表

| ROUND | R2 |
| TASK_PATH | `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md` |
| SLUG | `gov-wiki-t4-rollout` |
| FREEZE | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |

### R3 填表

| ROUND | R3 |
| TASK_PATH | `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md` |
| SLUG | `gov-wiki-ingest-batch-3` |
| FREEZE | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |

---

## 单元 B（PR-B · 非本 Prompt）

`docs/tasks/active/task_governance_l2_phase_c_impl_v1.md` · `test_strategy: required` · PR-A 合并后继续同分支。
