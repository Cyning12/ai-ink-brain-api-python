# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md |
| related_review_or_none | 无 |
| git_branch | task/engineering-tech-graph-gate-d-v2-tasks-v1 |
| worktree_root | ai-ink-brain-api-python-wt-gate-d-v2 |
| created_utc_or_local | 2026-05-21 CST |
| notes | semi_auto 链式；30 帽已回填自检结论 |

## 可复制 Prompt 快照（semi_auto 下一棒）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task：ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md
- 逻辑子仓：ai-ink-brain-api-python
- Worktree cwd：ai-ink-brain-api-python-wt-gate-d-v2
- 主验证：pytest tests -m "not intent_eval and not intent_benchmark"
- 变更范围：task/engineering-tech-graph-gate-d-v2-tasks-v1 相对 main 的 gate D PR-1 diff

须复读 task「### 自检结论（执行者）」是否已与本轮命令一致；若 PR-3 已补跑 batch，更新 PR-3 验收行与结论文。
下一棒：50 独立复检（post_close）或回 30 补 SILICONFLOW batch。
```
