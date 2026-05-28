# Invoke · gov-wiki-docs-hygiene · 50 · R1

| 项 | 值 |
| --- | --- |
| **round** | R1 |
| **hat** | 50 |
| **task** | `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md` |
| **task_slug** | `gov-wiki-docs-hygiene` |
| **freeze_id** | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 40（自检已 commit @ 0081e5e） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 40 已结束；本帽为 50 独立复检帽，只按下文执行。

执行 Wiki Loop 单元 A · R1 · 50 复检。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only。
task: docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md
task_slug: gov-wiki-docs-hygiene
freeze_id: GOV-WIKI-DOCS-HYGIENE@2026-05-28

**复检步骤**
1. 独立 diff 审查（`git diff HEAD~3`），非复读 40 结论
2. 逐文件核对：改动与 done/ 实际状态是否一致
3. 链接有效性抽查
4. human_gate 追溯（确认 Agent 未代填）
5. 范围审查（确认无 api/tests/tools 改动）
6. 产出 `docs/tasks/reinspect_results/reinspect_gov-wiki-docs-hygiene_*.md`
7. 落盘 50 invoke + commit
8. 无阻塞则关账（git mv → done/ + _views/done.md + HANDOFF_CLOSE_TRACE）

**产出路径**
- reinspect: `docs/tasks/reinspect_results/reinspect_gov-wiki-docs-hygiene_20260528_v1.md`
```

---

## 复检执行摘要

- diff_range: `HEAD~3..HEAD`（bf15688 → 0081e5e）
- 9 文件改动，+294/-10
- 全部 docs-only，无越界
- human_gate：HG-LOOP-BATCH approved（人改），HG-INGEST-BATCH-3-SCOPE approved（人改）
- 结论：**复检通过 · 可关账**
