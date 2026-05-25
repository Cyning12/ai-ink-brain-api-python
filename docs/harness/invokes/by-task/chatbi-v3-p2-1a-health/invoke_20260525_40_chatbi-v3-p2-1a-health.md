## Invoke 快照（40 自检帽 · P2-1a health/ready）

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md` |
| git_branch | `task/chatbi-v3-p2-1a-health` |
| worktree_root | `ai-ink-brain-api-python` |
| semi_auto | `true` |
| audit_profile | `post_close` |
| human_gate | `task 未显式表；按 kickoff 人工授权继续本棒` |
| 验证命令 | `pytest tests -m "not intent_eval and not intent_benchmark"` |

### 自检执行要点

1. 对照 task 验收项逐条确认 pass/fail。  
2. 附命令证据（命令、退出码、通过统计）。  
3. 回填 task `### 自检结论（执行者）`。  
4. 若通过，给出 50 复检棒 invoke 摘要或下一棒可复制 Prompt。  
