# Invoke · 40-self-check · ops-chat-session-sink-p0-p1 · P0-4 Tracing

| 项 | 内容 |
| --- | --- |
| **hat** | 40-self-check |
| **task** | `Projects/docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **git_branch** | `task/ops-chat-session-sink-p0-p1` |
| **phase** | P0-4 Tracing |
| **timestamp** | 2026-07-09T14:00:00+08:00 |
| **上游 30 invoke** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260709_1355_30_ops_chat_session_sink_p0_p1_P0-4.md` |

## 自检范围

仅复核 P0-4 Tracing 改动：
- `api/ops/tracing.py`
- `api/ops/orchestrator/core.py`（入口 metadata、handoff/review trace_span）
- `api/ops/react_loop.py`（入口 metadata、handoff/review trace_span）
- `tests/ops/test_tracing.py`
- task 正文「### 自检结论（执行者）· P0-4」

## 上游 30 结论摘要

- `api/ops/tracing.py` 新增 `OPS_CHAT_TRACER` 主控开关（`langfuse` / `langsmith`），未知值/未设置时 `none`；保留旧 `LANGFUSE_TRACING` / `LANGSMITH_TRACING` 兼容。
- 新增 `trace_span(...)` 上下文管理器；`traceable` / `update_current_span_metadata` 保持可用。
- `run_deep` / `run_react_fallback` 入口 metadata 加 `run_id` / `session_id` / `agent_role`（deep / react）。
- handoff / review 热路径包 `with trace_span(...)`。
- 新增 `tests/ops/test_tracing.py` 12 测例；最终验证命令 `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q` 282 passed / 10 skipped，`ruff check api/ops` 全绿。

## 你必须完成

1. **独立阅读**上游 30 invoke、task P0-4 开工记录与自检结论、以及上述代码文件。
2. **独立执行**验证命令并记录输出：
   ```bash
   cd ai-ink-brain-api-python
   pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
   ```
3. **差异核对**：逐条核对 30 结论中的验收项，确认与代码/测试一致。
4. **范围检查**：执行 `git diff origin/main...HEAD --stat`，确认未扩 scope 到 P1、Session 生产图、Agently lab、前端。
5. **回填 task**：在 `Projects/docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` 新增「### 自检结论（40 复核）· P0-4」小节，包含：
   - 复核方法
   - 命令输出（完整）
   - 与 30 结论差异核对表
   - 验收项复核表
   - 阻塞项清单
   - 合并建议
   - Judgment（experience_capture / gate/risk / hat_self）
6. **生成 50 Prompt**：输出可直接交给下一棒 50 独立复检的 Prompt，并落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_50_ops_chat_session_sink_p0_p1_P0-4.md`。
7. **自动 commit**：在代码/测试/task/50 Prompt 落盘后，按 HANDOFF_AUTO_COMMIT.md 在 `ai-ink-brain-api-python/` commit（仅本轮路径；禁止 `git add -A`），对话报 short-hash。
8. **不要 push**：本阶段完成后由 Lead push 分支并提醒用户开 PR。

## 输出要求

- 若发现阻塞：Markdown 阻塞清单（gate_id / 路径 / 原因）。
- 若通过：diff 摘要、验证命令输出、commit short-hash、下一棒 50 Prompt。

## 强制约束

- **禁止代签人工闸**；若遇 task / review 中任何 human_gate 对 40 为 `pending`，仅输出须人改的 gate_id 与路径，拒继续。
- 仅复核 P0-4，不要替 30 修改实现。
