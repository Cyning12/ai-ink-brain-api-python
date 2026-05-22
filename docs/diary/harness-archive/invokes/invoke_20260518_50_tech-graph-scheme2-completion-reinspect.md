# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| template | docs/harness/prompts/TEMPLATE-independent-reinspect-invoke.md §3 |
| reinspect_mode | 独立复检 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md |
| related_review | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_reinspect_50_20260518.md |
| related_r1 | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md |
| prev_invoke | ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_40_tech-graph-scheme2-completion-self-check.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-scheme2-completion-v1 |
| diff_range | origin/main...HEAD（子仓） |
| notes | 50 独立复检；全文见 reviews 落盘 |

## 可复制 Prompt 快照

```text
你正在扮演工作区 Harness「独立复检帽」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md（§一）
- docs/harness/HARNESS_V2_PLAN.md §5

模式：独立复检

输入：
- 主 task：ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md
- 子仓根：ai-ink-brain-api-python
- diff：git diff origin/main...HEAD（子仓）
- 自检结论：task「### 自检结论（执行者）」
- R1：docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md

你必须完成：
0. 落盘 invoke + reviews 复检报告。
1. 独立复跑 task §3.3 命令；对照 40 帽表。
2. 输出验收 pass/fail 表 + 阻塞合并项 + 是否建议合并。
3. 建议合并且无下一棒时输出 Commit 回溯（HANDOFF_CLOSE_TRACE）。
4. HANDOFF_AUTO_COMMIT 提交；用户要求则 push。
```
