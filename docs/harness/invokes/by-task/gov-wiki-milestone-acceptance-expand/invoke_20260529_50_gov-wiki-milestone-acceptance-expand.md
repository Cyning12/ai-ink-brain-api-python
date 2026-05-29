---
hat_id: 50
round: R1
task: gov-wiki-milestone-acceptance-expand
git_branch: task/gov-wiki-milestone-acceptance-expand-v1
freeze_id: GOV-WIKI-MILESTONE-ACCEPT@2026-05-29
author: Agent
---

# Invoke 快照：50 独立复检 · R1

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| round | R1 |
| task_slug | gov-wiki-milestone-acceptance-expand |
| task_path | docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md |
| git_branch | task/gov-wiki-milestone-acceptance-expand-v1 |
| freeze_id | GOV-WIKI-MILESTONE-ACCEPT@2026-05-29 |
| test_strategy | not_applicable |
| semi_auto | true |
| human_gate | HG-TASK-DRAFT approved · HG-REINSPECT approved |
| reinspect_mode | 独立复检 |
| prev_hat | 40 自检 |
| reinspect_output | docs/tasks/reinspect_results/reinspect_gov-wiki-milestone-acceptance-expand_20260529_v1.md |

---

## §3 可复制 Prompt 正文（快照）

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task 路径：ai-ink-brain-api-python/docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md
- 子仓根：ai-ink-brain-api-python
- 模式：独立复检
- diff 范围：task/gov-wiki-milestone-acceptance-expand-v1 分支上 10→30→40 链全部 commit
- 任务审核书面结论：ai-ink-brain-api-python/docs/harness/reviews/task_gov-wiki-milestone-acceptance-expand_audit_R1_20260529.md

你必须完成：
0. Invoke 快照
1. 读取 task「### 自检结论（执行者）」
2. human_gate diff 审查
3. 独立重跑验证
4. 逐项验收 pass/fail
5. 落盘复检报告至 docs/tasks/reinspect_results/
6. commit
7. 输出 CLOSE_TRACE 或下一棒 Prompt
```
