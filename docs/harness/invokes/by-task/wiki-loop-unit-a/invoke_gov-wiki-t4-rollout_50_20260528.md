# Invoke · gov-wiki-t4-rollout · 50 · R2

| 项 | 值 |
| --- | --- |
| **round** | R2 |
| **hat** | 50 |
| **task** | `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md` |
| **task_slug** | `gov-wiki-t4-rollout` |
| **freeze_id** | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 40（自检已 commit @ a5a86a4） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 40 已结束；本帽为 50 独立复检帽，只按下文执行。

执行 Wiki Loop 单元 A · R2 · 50 复检。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only。
task: docs/tasks/active/task_governance_wiki_t4_rollout_v1.md
task_slug: gov-wiki-t4-rollout
freeze_id: GOV-WIKI-T4-ROLLOUT@2026-05-28

**复检步骤**
1. 独立 diff 审查（`git diff HEAD~3`），非复读 40 结论
2. 逐文件核对 14 篇 synthesis frontmatter 格式与 id 合理性
3. 运行 YAML 解析验证
4. 范围审查（确认无 api/tests/tools 改动）
5. 产出 `docs/tasks/reinspect_results/reinspect_gov-wiki-t4-rollout_*.md`
6. 落盘 50 invoke + commit
7. 无阻塞则关账

**产出路径**
- reinspect: `docs/tasks/reinspect_results/reinspect_gov-wiki-t4-rollout_20260528_v1.md`
```

---

## 复检执行摘要

- diff_range: `HEAD~3..HEAD`（e14a08b → a5a86a4）
- 19 文件改动，+352/-3
- 14 篇 synthesis frontmatter 修改
- 4 篇 Harness 工件新增
- 结论：**复检通过 · 可关账**
