# 40 Self-Check Invoke Snapshot

**Date:** 2026-07-08 14:00 local
**Hat:** 40-self-check (Harness execution self-check)
**Task:** docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md
**Sub-repo:** ai-ink-brain-api-python
**Previous 30 commit:** d590afd3
**Verify command:** pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops

---

## Input prompt (full user message)

你正在扮演工作区 Harness「执行者自检帽」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/prompts/30-execute-code.md
- docs/harness/HARNESS_V2_PLAN.md §5
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8

输入：
- 主 task 路径（相对工作区根 Projects/）：
docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md
- 逻辑子仓（相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录：
ai-ink-brain-api-python
- 上一棒 30 执行帽 invoke 快照：
ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260708_1327_30_ops_chat_session_sink_p0_p1_v1.md
- 30 已提交 commit（ai-ink-brain-api-python）：
d590afd3
- 合并前须跑通的验证命令：
pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
- 关联任务审核书面结论路径：
ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md
- 关联 SPEC / 总规：
docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md

人工闸状态：HG-TASK-DRAFT approved、HG-AUDIT-R1 approved（维护者 2026-07-08 签收）。

30 已交付内容（须你独立复核，不可照抄）：
- 新增 `api/ops/review/rules.py` + `api/ops/review/__init__.py`，承载共享 Review V1–V4。
- `api/ops/orchestrator/core.py` 删除本地 `review_result`，改从 `api.ops.review.rules` 导入。
- `api/ops/orchestrator/__init__.py` 改从共享模块导入 `review_result`（向后兼容）。
- `api/ops/react_loop.py` 改从共享模块导入 `review_result`。
- 新增 `tests/ops/test_review_rules.py` 17 个测例覆盖 V1/V2/V3/V4、优先级、deep/ReAct 共用、向后兼容。
- task 正文已回填「### 自检结论（执行者）」。

你必须完成：
1. Invoke 快照：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260708_1400_40_ops_chat_session_sink_p0_p1_v1.md`。
2. 通读 task 全文，重点核对「### 自检结论（执行者）」与 30 invoke 快照。
3. 在 `ai-ink-brain-api-python/` 内独立执行验证命令，保留原始输出要点。
4. 对照 task P0-1 验收项逐条打勾/打叉：
   - P0-1 共享 Review 模块存在且被 deep/ReAct 共用。
   - V1–V4 行为与 task / PLAN 一致。
   - `tests/ops/test_review_rules.py` 绿。
   - `ruff check api/ops` 绿。
   - 未静默扩大 scope。
5. 若 30 结论与你不符 → 列出差异项；若一致 → 在 task 正文追加 40 复核意见（新增 `### 自检结论（40 复核）` 小节）。
6. 生成下一棒 50 复检 Prompt（audit_profile=full）。
7. 自动 commit：仅本轮路径，禁止 git add -A；报 short-hash。
8. 链式下一棒：不自动换帽；交还 00 或输出下一棒。

禁止：不跑命令就勾选；复制 30 结论当作 40 结论；口头宣称「已复核」而无命令输出。
