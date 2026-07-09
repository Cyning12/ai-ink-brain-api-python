# 40 执行者自检帽 · Invoke 快照

| 字段 | 内容 |
| --- | --- |
| **timestamp** | 20260709_1622 |
| **hat** | 40-self-check |
| **task_slug** | ops-chat-session-sink-p0-p1 |
| **subtask** | P1-1 Artifacts → Supabase |
| **git_branch** | task/ops-chat-session-sink-p0-p1 |
| **worktree_root** | ai-ink-brain-api-python/ |
| **verify_command** | `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` |
| **task_path** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **30_invoke_path** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260709_1622_30_ops_chat_session_sink_p0_p1_P1-1.md` |
| **30_commit** | 待 30 自动 commit 后回填 |

## 用户消息快照（30 → 40 交接 Prompt）

```text
你正在扮演工作区 Harness「40-self-check · 执行者自检帽」，严格遵循 docs/harness/prompts/40-self-check.md。

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

**你必须完成**
1. 独立阅读 30 invoke 快照与 task 正文「### 自检结论（执行者）· P1-1」小节。
2. 独立阅读本轮 P1-1 改动代码：
   - `supabase/sql/ops_desk_p1_artifacts.sql`
   - `supabase/sql/ops_desk_p1_artifacts_rollback.sql`
   - `api/ops/store/artifacts.py`
   - `api/ops/store/runs.py`
   - `api/ops/orchestrator/core.py`
   - `api/ops/react_loop.py`
   - `tests/ops/test_artifacts.py`
3. 在 `ai-ink-brain-api-python/` 内完整执行 30 声明的验证命令；保留命令输出要点。
4. 执行 `git diff origin/main...HEAD --stat`（在 ai-ink-brain-api-python 内）核对全量变更路径，确认未扩 scope 到 P1-2/3/4、Session 生产图、Agently lab、前端。
5. 按 40-self-check.md 将复核结论回填至 task 正文「### 自检结论（40 复核）· P1-1」小节（不要覆盖 P0 或 30 已有结论）。
6. 与 30 结论逐项差异核对；若不一致，列出差异项并判断阻塞性。
7. 生成可以完整复制的 Prompt，用于直接交给下一棒 50 独立复检执行。
8. 在输出下一棒 Prompt 且 task 40 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python/ commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
9. 禁止自行 push；由 Lead 合并。

**输出要求**
- 复核方法、命令输出、与 30 结论差异核对表、验收项复核表、阻塞项清单、合并建议、下一棒 50 Prompt。
- Judgment（本帽 · 对话末尾必填）：experience_capture / gate/risk / hat_self
```
