# Invoke Snapshot · 40-self-check · P0-3

| 项 | 内容 |
| --- | --- |
| **task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **hat** | `40-self-check` |
| **phase** | `P0-3` |
| **date** | `2026-07-09` |
| **timestamp** | `20260709_1216` |
| **branch** | `task/ops-chat-session-sink-p0-p1` |
| **prior_30_invoke** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260709_1216_30_ops_chat_session_sink_p0_p1_P0-3.md` |

## 原始 Prompt 快照

```text
你正在扮演工作区 Harness「40-self-check · 执行者自检帽」，严格遵循 docs/harness/prompts/40-self-check.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 上一棒 30 invoke 快照：`ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260709_1216_30_ops_chat_session_sink_p0_p1_P0-3.md`
- 本阶段范围：P0-3 多轮 Transcript（仅 P0-3；不改 P0-4 / P1 / Session 生产图 / Agently lab / 前端）

**你必须完成**
1. 独立阅读 30 改动：
   - `api/ops/chat_context.py`
   - `api/ops/chat_service.py`
   - `api/ops/orchestrator/core.py`
   - `api/ops/react_loop.py`
   - `api/ops/agents/issue_analyst.py`
   - `api/ops/agents/graph_analyst.py`
   - `api/ops/agents/scan_analyst.py`
   - `api/ops/llm/__init__.py`
   - `tests/ops/test_chat_context.py`
   - `tests/ops_desk/test_llm_usage_metrics.py`
2. 在 `ai-ink-brain-api-python/` 内完整执行验证命令，保留输出。
3. 核对 task 内「### 自检结论（执行者）· P0-3」的声称项，在 task 正文追加「### 自检结论（40 复核）· P0-3」小节，含：
   - 复核方法
   - 命令输出（与 30 独立运行）
   - 与 30 结论差异核对表
   - 验收项复核表
   - 阻塞项清单
   - 合并建议
   - Judgment（experience_capture / gate/risk / hat_self）
4. 生成 50 复检 Prompt 并落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_50_ops_chat_session_sink_p0_p1_P0-3.md`。
5. 自动 commit：仅本轮新增/修改路径（禁止 git add -A），对话报 short-hash。
6. 禁止自行 push；由 Lead 合并。

**输出要求**
- diff 摘要
- 验证命令输出
- commit short-hash
- 50 复检 Prompt

**重点核验**
- `load_chat_transcript(session_id, n=6)` 是否从 `ops_runs` + `ops_run_events` 读取最近 N 轮完整 user/assistant 对。
- 无 `session_id` 时是否返回空列表且不抛异常，并有 `chat_context.no_session_id` debug 日志。
- `chat_service.py` 是否将 `session_id` 透传给 `run_deep` / `run_react_fallback`。
- `run_deep` / `run_react_fallback` 是否在调用 LLM 前将 transcript 注入 messages / prompt 上下文。
- 是否未改 P0-4 / P1 / `harness_runtime` 生产图 / Agently lab / 前端代码。
- P0-2 events schema 实现是否未被破坏。
```
