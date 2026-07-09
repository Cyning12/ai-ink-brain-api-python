# 50 独立复检 + 全局验收帽 · Invoke 快照

| 字段 | 内容 |
| --- | --- |
| **timestamp** | 20260709_1650 |
| **hat** | 50-reinspect |
| **task_slug** | ops-chat-session-sink-p0-p1 |
| **subtask** | P1-1 Artifacts → Supabase |
| **git_branch** | task/ops-chat-session-sink-p0-p1 |
| **worktree_root** | ai-ink-brain-api-python/ |
| **verify_command** | `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` |
| **task_path** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **30_invoke_path** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260709_1622_30_ops_chat_session_sink_p0_p1_P1-1.md` |
| **30_commit** | `api-python@13eb0524` |
| **40_commit** | 待 40 自动 commit 后回填（见 task 正文「### 自检结论（40 复核）· P1-1」） |
| **audit_review_path** | `ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md` |

## 用户消息快照（40 → 50 交接 Prompt）

```text
你正在扮演工作区 Harness「50-reinspect · 独立复检 + 全局验收帽」，严格遵循 docs/harness/prompts/50-reinspect.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 本棒校验范围：**P1-1 Artifacts → Supabase**
- 30 执行者已声明的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 30 invoke 快照：`ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260709_1622_30_ops_chat_session_sink_p0_p1_P1-1.md`
- 30 commit：`api-python@13eb0524`
- 40 commit：见 task 正文「### 自检结论（40 复核）· P1-1」小节末尾

**你必须完成**
1. 独立阅读 task 正文「### 自检结论（执行者）· P1-1」与「### 自检结论（40 复核）· P1-1」小节。
2. 独立阅读本轮 P1-1 改动代码：
   - `supabase/sql/ops_desk_p1_artifacts.sql`
   - `supabase/sql/ops_desk_p1_artifacts_rollback.sql`
   - `api/ops/store/artifacts.py`
   - `api/ops/store/runs.py`
   - `api/ops/orchestrator/core.py`
   - `api/ops/react_loop.py`
   - `tests/ops/test_artifacts.py`
3. 在 `ai-ink-brain-api-python/` 内完整执行 30 声明的验证命令；保留命令输出要点。
4. 额外执行 task §失败路径所列的 `pytest tests/ops/test_artifacts.py -k write_failed -q`。
5. 执行 `git diff origin/main...HEAD --stat`（在 ai-ink-brain-api-python 内）核对全量变更路径，确认未扩 scope 到 P1-2/3/4、Session 生产图、Agently lab、前端。
6. 与 30 commit `13eb0524`、40 commit、R2 任务审核书面结论逐条核对。
7. 将 50 复检书面结论落盘至 `ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R1_20260709_50_P1-1.md`。
8. 按 50-reinspect.md 将全局验收结论回填至 task 正文「### 自检结论（50 复检）· P1-1」小节（不要覆盖 P0 或 30/40 已有结论）。
9. 输出：复核方法、命令输出、与 30/40 结论差异核对表、验收项复核表、阻塞项清单、合并建议、Judgment。
10. 在输出结论且 task 50 复检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 `ai-ink-brain-api-python/` 与 `Projects/` 分仓 commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
11. 禁止自行 push；由 Lead 合并。

**输出要求**
- 复核方法、命令输出、与 30/40 结论差异核对表、验收项复核表、阻塞项清单、合并建议。
- Judgment（本帽 · 对话末尾必填）：experience_capture / gate/risk / hat_self
```
