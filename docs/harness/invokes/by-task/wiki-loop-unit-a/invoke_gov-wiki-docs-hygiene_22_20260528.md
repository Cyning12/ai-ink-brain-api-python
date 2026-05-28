# Invoke · gov-wiki-docs-hygiene · 22 · R1

| 项 | 值 |
| --- | --- |
| **round** | R1 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md` |
| **task_slug** | `gov-wiki-docs-hygiene` |
| **freeze_id** | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **cross_round_semi_auto** | true |
| **audit_profile** | post_close |
| **human_gate** | HG-LOOP-BATCH approved |
| **review** | `docs/harness/reviews/by-task/gov-wiki-docs-hygiene/task_gov-wiki-docs-hygiene_audit_R1_20260528.md` |

---

## §3 可复制 Prompt

```text
执行 Wiki Loop 单元 A · R1 · 22→关账。分支 task/wiki-unit-ab-plan-v1。
task: docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md
task_slug: gov-wiki-docs-hygiene
freeze_id: GOV-WIKI-DOCS-HYGIENE@2026-05-28
semi_auto: true · PR-A docs-only · 禁止 api/tests/tools。

帽子：22→30→40→50；落盘 invoke + commit；关账 HANDOFF_CLOSE_TRACE。
R3 额外：Batch-3 五 slug 见 SPEC-Governance-Wiki-Ingest-Batch-3-v1.md §1。

**执行步骤（hard rules · 每帽换前须落盘 + commit）**

1. **Gate 验证**：打开 `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md`，扫描 `human_gate` 表；若写「继承母闸」，**同时**打开 `docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md`（**以母单 status 为准**）。子单或母单任一 relevant gate 为 `pending` 且阻塞当前帽 → **硬停**，输出 `📋 Harness 状态栏（版本 B）`（阻塞版），不写 review / 不改代码 / 不落盘 invoke。真值：`HANDOFF_SEMI_AUTO.md` §2.3 · `SKILL-harness-loop-batch.md` §执行铁律。
2. **22 审核**：读 task + 关联 SPEC / 前置 task，产出 `docs/harness/reviews/by-task/gov-wiki-docs-hygiene/task_*_audit_R1_*.md`。post_close 轻闸；无阻塞则写「零阻塞·可执行」+ 下一棒 30 Prompt。
3. **30 执行**：按 task 范围改文档；遵守「范围 / 非范围」；每文件改动后自核链接、状态、freeze_id 一致性。
4. **40 自检**：逐条对照 task 验收标准，运行 VERIFY 命令，粘贴输出要点；回填 task 内 `### 自检结论（执行者）`。
5. **50 复检**：独立 diff 审查（非复读 40），产出 `docs/tasks/reinspect_results/reinspect_gov-wiki-docs-hygiene_*.md`；含 human_gate diff 审查与 author 追溯。
6. **关账**：`git mv` task → `docs/tasks/done/`；更新 `_views/done.md`；输出 `HANDOFF_CLOSE_TRACE`（执行路线 + commit 回溯）。
7. **invoke 质量（C2）**：每帽落盘 `docs/harness/invokes/by-task/wiki-loop-unit-a/invoke_*`，§3 ≥15 行，元信息表完整（round/hat/task/task_slug/freeze_id/git_branch）。按 `HANDOFF_AUTO_COMMIT` 仅 add 本轮路径后 commit。
```
