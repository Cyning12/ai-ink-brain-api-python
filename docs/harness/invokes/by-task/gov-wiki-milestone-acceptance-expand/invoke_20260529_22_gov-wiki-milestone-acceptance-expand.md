---
hat_id: 22
round: R1
task: gov-wiki-milestone-acceptance-expand
git_branch: task/gov-wiki-milestone-acceptance-expand-v1
freeze_id: GOV-WIKI-MILESTONE-ACCEPT@2026-05-29
author: Agent
---

# Invoke 快照：22 任务审核帽 · R1

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| round | R1 |
| task_slug | gov-wiki-milestone-acceptance-expand |
| task_path | docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md |
| git_branch | task/gov-wiki-milestone-acceptance-expand-v1 |
| freeze_id | GOV-WIKI-MILESTONE-ACCEPT@2026-05-29 |
| audit_profile | post_close |
| test_strategy | not_applicable |
| semi_auto | true |
| human_gate | HG-TASK-DRAFT approved · HG-REINSPECT approved |
| prev_review | 无（首轮） |
| review_path | docs/harness/reviews/task_gov-wiki-milestone-acceptance-expand_audit_R1_20260529.md |

---

## §3 可复制 Prompt 正文（快照）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/reviews/README.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 待审 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md
- 关联 SPEC / 总规路径（无则写「无」）：
无
- 上一轮审查文档路径（首轮写「无」）：
无

落盘文件建议名：
ai-ink-brain-api-python/docs/harness/reviews/task_gov-wiki-milestone-acceptance-expand_audit_R1_20260529.md

你必须完成：
0. Invoke 快照
1. 通读 task 全文及头部元信息
2. 对照 HARNESS_V2_PLAN.md §5 检查验收可观测性
3. 落盘审查文档
4. 文内结构：元信息 → 审查结论摘要 → 阻塞/非阻塞 → 是否建议执行帽开工 → 签收/关闭 → 下一棒可复制 Prompt
5–8. 按 hats/22-task-audit.md 执行
```

---

## §2 占位符替换确认

| 占位符 | 替换值 | 状态 |
|--------|--------|------|
| `{{TASK_PATHS}}` | ai-ink-brain-api-python/docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md | 已替换 |
| `{{SPEC_PATHS_OPTIONAL}}` | 无 | 已替换 |
| `{{PREV_REVIEW_PATH_OR_NONE}}` | 无 | 已替换 |
| `{{AUDIT_ROUND}}` | R1 | 已替换 |
| `{{YYYYMMDD}}` | 20260529 | 已替换 |
| `{{SLUG}}` | gov-wiki-milestone-acceptance-expand | 已替换 |
