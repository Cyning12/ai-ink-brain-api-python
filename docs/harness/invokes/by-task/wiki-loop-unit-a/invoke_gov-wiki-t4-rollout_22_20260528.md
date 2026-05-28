# Invoke · gov-wiki-t4-rollout · 22 · R2

| 项 | 值 |
| --- | --- |
| **round** | R2 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md` |
| **task_slug** | `gov-wiki-t4-rollout` |
| **freeze_id** | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **human_gate** | HG-LOOP-BATCH approved（母单） |
| **review** | `docs/harness/reviews/by-task/gov-wiki-t4-rollout/task_gov-wiki-t4-rollout_audit_R1_20260528.md` |

---

## §3 可复制 Prompt

```text
执行 Wiki Loop 单元 A · R2 · 22→关账。分支 task/wiki-unit-ab-plan-v1。
task: docs/tasks/active/task_governance_wiki_t4_rollout_v1.md
task_slug: gov-wiki-t4-rollout
freeze_id: GOV-WIKI-T4-ROLLOUT@2026-05-28
semi_auto: true · PR-A docs-only · 禁止 api/tests/tools。

帽子：22→30→40→50；落盘 invoke + commit；关账 HANDOFF_CLOSE_TRACE。

**执行步骤（hard rules · 每帽换前须落盘 + commit）**

1. **Gate 验证**：打开 `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md`，扫描 `human_gate` 表；继承母闸 → 同时打开母单 `docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md`（以母单 status 为准）。pending 且阻塞当前帽 → 硬停。
2. **22 审核**：读 task + T4 Bridge SPEC，产出 `docs/harness/reviews/by-task/gov-wiki-t4-rollout/task_*_audit_R*_*.md`。post_close 轻闸；无阻塞则写「零阻塞·可执行」+ 下一棒 30 Prompt。
3. **30 执行**：按 task 铺量清单为 14 篇 synthesis 补 `graph_nodes` frontmatter；id 须 graph_query 验证；relation 用 §3.1 枚举。
4. **40 自检**：逐条对照 task 验收标准，运行 VERIFY 命令，粘贴输出要点；回填 task 内 `### 自检结论（执行者）`。
5. **50 复检**：独立 diff 审查，产出 `docs/tasks/reinspect_results/reinspect_gov-wiki-t4-rollout_*.md`。
6. **关账**：`git mv` task → `docs/tasks/done/`；更新 `_views/done.md`；输出 `HANDOFF_CLOSE_TRACE`。
7. **invoke 质量（C2）**：每帽落盘 `docs/harness/invokes/by-task/wiki-loop-unit-a/invoke_*`，§3 ≥15 行，元信息表完整。按 `HANDOFF_AUTO_COMMIT` 仅 add 本轮路径后 commit。
```
