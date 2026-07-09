# Invoke Snapshot · 40-self-check · ops-chat-session-sink-p0-p1 · P0-2

| 字段 | 值 |
| --- | --- |
| **hat** | 40-self-check |
| **task** | docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md |
| **subproject** | ai-ink-brain-api-python |
| **branch** | task/ops-chat-session-sink-p0-p1 |
| **scope** | P0-2 结构化 run events（复核 30 执行结论） |
| **timestamp** | 2026-07-09 11:05 |
| **verify_command** | `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` |

## 40 自检 Prompt（可直接复制执行）

```text
你正在扮演工作区 Harness「40-self-check · 执行者自检帽」，严格遵循 docs/harness/prompts/40-self-check.md。

**输入（占位符已替换）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`
- 验证命令：`pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops`
- 本轮 30 执行范围：P0-2 结构化 run events
- 30 invoke 快照：`ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260709_1105_30_ops_chat_session_sink_p0_p1_P0-2.md`

**你必须完成**
1. 独立阅读 task 内「### 自检结论（执行者）· P0-2」30 回填结论。
2. 独立阅读本轮改动代码：
   - `api/ops/events_schema.py`
   - `api/ops/store/runs.py`
   - `api/ops/orchestrator/core.py`
   - `api/ops/react_loop.py`
   - `tests/ops/test_events_schema.py`
3. 在 `ai-ink-brain-api-python/` 内完整执行验证命令，保留可核对输出要点。
4. 按 40-self-check.md 将复核结论回填至 task 正文「### 自检结论（40 复核）」小节（在 P0-2 区域新增；与 P0-1 的 40 复核并列）。
5. 核对项（必须逐条给出 pass/fail）：
   - `api/ops/events_schema.py` 存在且 `SCHEMA_VERSION="v1"`
   - `handoff_payload` / `review_payload` 结构含 `schema_version`
   - `api/ops/store/runs.py` 新增 `append_event(run_id, kind, payload)` 辅助函数，能自动注入 schema_version
   - deep 路径 `api/ops/orchestrator/core.py` 在关键 handoff/review 处调用 `append_event`
   - ReAct 路径 `api/ops/react_loop.py` 在关键 handoff/review 处调用 `append_event`
   - P0-1 Review 共享模块未被破坏（`api/ops/review/rules.py` 未改动；deep/ReAct 仍从共享模块导入 `review_result`）
   - `tests/ops/test_events_schema.py` 覆盖 schema_version、handoff/review payload、`append_event` 写入
   - 验证命令绿：`pytest ...` 退出码 0 + `ruff check api/ops` 退出码 0
   - 未静默扩大 scope（未改 P0-3/4、P1、Session 生产图、Agently lab、前端）
6. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒 50 独立复检执行。
7. 自动 commit：在输出下一棒 Prompt 且 task 40 复核回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 `ai-ink-brain-api-python/` commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
8. 禁止自行 push；由 Lead 合并。

**输出要求**
- 复核方法、命令输出、与 30 结论差异核对表、验收项复核表、阻塞项清单、合并建议。
- 若发现 30 结论与独立复核不一致，必须列出差差异项并判断阻塞性。

**Judgment（本帽 · 对话末尾必填）**
- experience_capture: required（P0-2 事件 schema 与 append_event 模式可复用到 P1-1/2/3/4）
- gate/risk: 无 / 列出阻塞项
- hat_self: pass | pass-with-notes | blocked
```
