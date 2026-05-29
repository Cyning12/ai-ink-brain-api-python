# Invoke · 40 自检帽 · ChatBI V3 P2-1b 限流

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| task_slug | `chatbi-v3-p2-1b-rate-limit` |
| task_path | `docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md` |
| git_branch | `task/chatbi-v3-p2-1b-rate-limit` |
| worktree_root | 主仓 `ai-ink-brain-api-python/` |
| 日期 | 2026-05-29 |
| 上一棒 | `invoke_20260529_30_chatbi-v3-p2-1b-rate-limit.md` |

## 快照（开帽 Prompt 全文）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task：ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md
- WORKTREE：ai-ink-brain-api-python
- VERIFY：pytest tests -m "not intent_eval and not intent_benchmark"
- DIFF：30 帽限流实现（api/chatbi_rate_limit.py + tests/test_rate_limit_routes.py）
```
