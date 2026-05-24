## Invoke 快照（40 自检帽）

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_v1.md` |
| git_branch | `task/chatbi-v3-p2-resilience-spec` |
| semiauto | `true` |
| 验证命令 | `pytest tests -m "not intent_eval and not intent_benchmark"` |

### 执行目标

1. 运行仓库合并前验证命令。  
2. 回填 task `### 自检结论（执行者）`（命令、退出码、通过统计、docs-only 说明）。  
3. 仅暂存本轮路径并提交（禁止 `git add -A`）。
