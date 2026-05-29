---
hat_id: 30
round: R1
task: gov-wiki-milestone-acceptance-expand
git_branch: task/gov-wiki-milestone-acceptance-expand-v1
freeze_id: GOV-WIKI-MILESTONE-ACCEPT@2026-05-29
author: Agent
---

# Invoke 快照：30 执行编码帽 · R1

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| round | R1 |
| task_slug | gov-wiki-milestone-acceptance-expand |
| task_path | docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md |
| git_branch | task/gov-wiki-milestone-acceptance-expand-v1 |
| freeze_id | GOV-WIKI-MILESTONE-ACCEPT@2026-05-29 |
| audit_profile | post_close |
| test_strategy | not_applicable |
| semi_auto | true |
| human_gate | HG-TASK-DRAFT approved · HG-REINSPECT approved |
| audit_review | docs/harness/reviews/task_gov-wiki-milestone-acceptance-expand_audit_R1_20260529.md |
| verify_command | python tools/coding_wiki_graph_nodes_lint.py |
| scope_lock | 仅 docs/diary/2026-05-29-wiki-milestone-acceptance.md |

---

## §3 可复制 Prompt 正文（快照）

```text
你正在扮演本仓 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task 路径：ai-ink-brain-api-python/docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md
- 逻辑子仓：ai-ink-brain-api-python
- Worktree：ai-ink-brain-api-python-wt-wiki-accept
- 验证命令：python tools/coding_wiki_graph_nodes_lint.py
- 关联审查：ai-ink-brain-api-python/docs/harness/reviews/task_gov-wiki-milestone-acceptance-expand_audit_R1_20260529.md
- 关联 SPEC：无

范围锁（硬）：仅 docs/diary/2026-05-29-wiki-milestone-acceptance.md

你必须完成：
0. Invoke 快照
0b. 人工闸：HG-TASK-DRAFT approved；HG-REINSPECT approved
1. 通读 task + 22 R1 审查
2. 按 10 帽扩充计划表编辑 diary
3. 执行验证命令
4. 回填 task「### 自检结论（执行者）」
5. 对话回复：diary diff 摘要 + §8.2 进度表
6. 自动 commit
7. 半自动下一棒：若 semi_auto=true 且无阻塞，可自动切 40
```
