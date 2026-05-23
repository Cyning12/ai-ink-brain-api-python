# Invoke Snapshot · 50-independent-reinspect · harness-p1-docs-consolidation

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| hat_name | independent-reinspect |
| task_slug | harness-p1-docs-consolidation |
| task_path | `docs/tasks/active/task_harness_p1_docs_consolidation_v1.md` |
| git_branch | `task/harness-p1-docs-consolidation` |
| worktree_root | `ai-ink-brain-api-python` |
| semi_auto | `true` |
| human_gate | HG-TASK-DRAFT approved；HG-REINSPECT **pending**（blocks done） |
| output | `docs/tasks/reinspect_results/reinspect_harness_p1_docs_consolidation_20260523.md` |
| generated_at | 2026-05-23 |
| source | 用户本轮消息全文快照 |

## Snapshot

```text
你正在扮演工作区 Harness「独立复检帽」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md
- docs/harness/prompts/TEMPLATE-independent-reinspect-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task 路径：docs/tasks/active/task_harness_p1_docs_consolidation_v1.md
- 逻辑子仓：ai-ink-brain-api-python
- Worktree 研发目录：ai-ink-brain-api-python
- 变更范围：git diff main...HEAD（或 5c2cd8a 以来 docs/tasks/ 路径）
- 30/40 交付：docs/tasks/README.md、docs/tasks/skills/README.md、task 自检结论
- 验证命令：pytest tests -m "not intent_eval and not intent_benchmark"（应已绿）

你必须完成：
0. Invoke 快照落盘 docs/harness/invokes/invoke_20260523_50_harness-p1-docs-consolidation.md
1. 对照 task 验收标准逐项 pass/fail（引用 diff 行号或文件路径，非凭记忆）
2. 核对 human_gate 速查 5 列、6 类 SKILL 语义与 HARNESS_V2 §5 / diary §三 3.1 一致
3. 落盘复检报告至 docs/tasks/reinspect_results/reinspect_harness_p1_docs_consolidation_20260523.md
4. 回填 task 或输出关账建议；HG-REINSPECT 仍为 pending，禁止代填 approved
5. 按 HANDOFF_AUTO_COMMIT 提交本轮路径

禁止：扩 scope 改 api/；代填 HG-REINSPECT approved。
```
