# Harness invoke snapshot

| 字段 | 值 |
| --- | --- |
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_paths | docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md |
| related_plan | docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md |
| git_branch | task/ops-chat-session-sink-p0-p1 |
| worktree_root | ai-ink-brain-api-python |
| parallel_with | ai-ink-brain-api-python-wt-agently-lab（Agently 学习） |
| created_utc_or_local | 2026-07-08 13:27 CST |
| notes | 人签 HG-TASK-DRAFT + HG-AUDIT-R1 approved；执行帽目标 P0-1 共享 Review 模块 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- 子仓 AGENTS.md、task 必读列表、根 AGENTS.md §8

输入：
- 主 task 路径（相对工作区根 Projects/）：
docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md
- 逻辑子仓（相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
- 关联任务审核书面结论路径：
ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md
- 关联 SPEC / 总规：
docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md

人工闸状态：维护者已全部签收，HG-TASK-DRAFT + HG-AUDIT-R1 approved。

你必须完成：
0. Invoke 快照：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/`。
1. 通读 task 全文及 PLAN §3.1/§4.1。
2. 缺 failure_paths / 验收命令 → 输出阻塞清单。
3. test_strategy: required 时先写可失败测试再改实现。
4. 在 ai-ink-brain-api-python/ 内按 task 范围改代码；禁止跨 worktree；禁止静默扩 scope；P2 不在范围。
5. 执行验证命令并保留输出；修复直至通过。
6. 回填 task「### 自检结论（执行者）」。
7. 生成下一棒 40 自检 Prompt。
8. 自动 commit：仅本轮路径，禁止 git add -A。
9. 链式下一棒：不自动换帽；交还 00 或输出下一棒。

禁止：未读 failure_paths 改路由/契约；删除无关重构；口头宣称「已测过」而无命令输出。

本帽目标：P0-1 共享 Review 模块 · `api/ops/review/rules.py` · deep/ReAct 共用 V1–V4 · pytest 绿。
```
