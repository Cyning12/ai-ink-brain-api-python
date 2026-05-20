# Harness invoke snapshot — 22 帽 · 闸口 D v2 task 审核 R1

| 字段 | 值 |
| --- | --- |
| hat_id | 22 |
| template | `Projects/docs/harness/prompts/TEMPLATE-task-audit-invoke.md` §3 |
| task_paths | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md` |
| related_review_or_none | 无（首轮 R1） |
| git_branch | `task/engineering-tech-graph-gate-d-v2-tasks-v1` |
| worktree_root | `ai-ink-brain-api-python-wt-gate-d-v2` |
| parallel_with | `invoke_20260520_22_chatbi-v3-prompt-injection-closeout-audit.md`（**禁止**共用分支/worktree） |
| invoke_10_snapshot | `docs/harness/invokes/invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md` |
| created | 2026-05-20 |
| task_outcome | 2026-05-20：R1 审查落盘；**零硬阻塞**；待人签 **HG-TASK-DRAFT** / **HG-AUDIT-R1** 后交 **30** |

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-20 | 22 帽开帽 invoke（闸口 D v2 tasks v1） |

---

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「任务审核帽（22）」，严格遵循：
- docs/harness/prompts/22-task-audit.md
- docs/harness/reviews/README.md
- docs/harness/HARNESS_V2_PLAN.md §5

【Git · worktree】
- 仓库：ai-ink-brain-api-python
- cwd：Projects/ai-ink-brain-api-python-wt-gate-d-v2（或分支 task/engineering-tech-graph-gate-d-v2-tasks-v1）
- 禁止共用：task/chatbi-v3-prompt-injection-closeout-v1

【待审 task】
docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md

【对照】
docs/harness/invokes/invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md
docs/tasks/done/task_engineering_tech_graph_gate_c_double_prime_v1.md
ai_coding_governance/methodology/graph/AGENT_GRAPH_CONSUMPTION_METHODOLOGY_v1_zh.md §6.1、§7
ai_coding_governance/methodology/graph/drafts/draft_gate_ctx_ab_v2_expansion_v1.md

【你必须完成】
0. 落盘 invoke_20260520_22_tech-graph-gate-d-v2-tasks-audit-r1.md
1. 产出 reviews/task_engineering_tech_graph_gate_d_v2_tasks_v1_audit_R1_20260520.md（零阻塞亦须记录）
2. 重点审：§7 矛盾裁定、T004/T005 gold 可测性、表1/表2 阈值、NR-1～8、human_gate 表
3. 有硬阻塞 → 回填清单交 10 帽；无阻塞 → 建议 HG-TASK-DRAFT / HG-AUDIT-R1 人签后交 30 执行帽
4. commit invoke + review；用户说不要 commit 则跳过

【禁止】改业务代码；代填 human_gate 为 approved；动 gate_ctx 历史 run 052803/083014/102810
```
