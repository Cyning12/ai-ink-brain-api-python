---
hat_id: 40
round: R1
task: gov-wiki-milestone-acceptance-expand
git_branch: task/gov-wiki-milestone-acceptance-expand-v1
freeze_id: GOV-WIKI-MILESTONE-ACCEPT@2026-05-29
author: Agent
---

# Invoke 快照：40 自检帽 · R1

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| round | R1 |
| task_slug | gov-wiki-milestone-acceptance-expand |
| task_path | docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md |
| git_branch | task/gov-wiki-milestone-acceptance-expand-v1 |
| freeze_id | GOV-WIKI-MILESTONE-ACCEPT@2026-05-29 |
| test_strategy | not_applicable |
| semi_auto | true |
| human_gate | HG-TASK-DRAFT approved · HG-REINSPECT approved |
| verify_command | python tools/coding_wiki_graph_nodes_lint.py |
| prev_hat | 30 执行 |

---

## §3 可复制 Prompt 正文（快照）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task 路径：ai-ink-brain-api-python/docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md
- 逻辑子仓：ai-ink-brain-api-python
- Worktree：ai-ink-brain-api-python-wt-wiki-accept
- 主验证命令：python tools/coding_wiki_graph_nodes_lint.py
- 变更范围说明：30 已改 diary（§1/§3/§6/§7 可签字小结 + §8.2 6/8 勾选 + §9 修订记录）

你必须完成：
0. Invoke 快照
1. 通读 task 验收标准
2. 独立重跑验证命令
3. 输出验收表（pass/fail + 证据）
4. 将结论写入/更新 task「### 自检结论（执行者）」
5. 自动 commit
```
