## Invoke 快照（50 复检帽 · P2-1a health/ready）

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md` |
| git_branch | `task/chatbi-v3-p2-1a-health` |
| worktree_root | `ai-ink-brain-api-python` |
| semi_auto | `true` |
| audit_profile | `post_close` |
| 前置帽结论 | `30 已实现并通过 pytest；40 已回填自检结论` |
| 复检输入 | `git diff HEAD~1..HEAD` + task 验收项 + pytest 证据 |

### 下一棒（50）执行提示

1. 以独立复检视角核对 `/api/py/live` 与 `/api/py/ready` 契约、状态码与失败路径一致性。  
2. 复核 `test_strategy: required` 是否满足（先测后改、命令证据齐全）。  
3. 若通过，落盘复检结论至 `docs/tasks/reinspect_results/` 对应文件；若失败，给出阻塞项与修复建议。  
