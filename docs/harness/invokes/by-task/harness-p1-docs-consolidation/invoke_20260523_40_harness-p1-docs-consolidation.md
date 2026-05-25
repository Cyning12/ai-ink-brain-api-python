# Invoke Snapshot · 40-self-check · harness-p1-docs-consolidation

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| hat_name | self-check |
| task_slug | harness-p1-docs-consolidation |
| task_path | `docs/tasks/active/task_harness_p1_docs_consolidation_v1.md` |
| git_branch | `task/harness-p1-docs-consolidation` |
| worktree_root | `ai-ink-brain-api-python` |
| semi_auto | `true` |
| human_gate | HG-TASK-DRAFT approved；HG-REINSPECT pending（blocks done） |
| generated_at | 2026-05-23 |
| source | semi_auto 链式 · 30 帽完成后自动切换 |

## Snapshot

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task 路径：docs/tasks/active/task_harness_p1_docs_consolidation_v1.md
- 逻辑子仓：ai-ink-brain-api-python
- Worktree 研发目录：ai-ink-brain-api-python
- 主验证命令：pytest tests -m "not intent_eval and not intent_benchmark"
- 变更范围说明：P1-3 docs/tasks/README.md human_gate 速查 + skills 入口；P1-2 docs/tasks/skills/README.md 新建

你必须完成：
1. 逐条对照验收标准，运行 pytest，回填「### 自检结论（执行者）」
2. 输出下一棒 50 复检 Prompt（audit_profile: post_close）
3. 按 HANDOFF_AUTO_COMMIT 提交本轮路径
```

## 本棒结论

**pass**：208 passed；验收项全 pass；自检结论已回填 task。
