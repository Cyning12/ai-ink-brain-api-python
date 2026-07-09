# Invoke Snapshot · 30-execute-code · P0-3

| 项 | 内容 |
| --- | --- |
| **task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **hat** | `30-execute-code` |
| **phase** | `P0-3` |
| **date** | `2026-07-09` |
| **timestamp** | `20260709_1216` |
| **branch** | `task/ops-chat-session-sink-p0-p1` |
| **human_gate** | `HG-TASK-DRAFT: approved`, `HG-AUDIT-R1: approved` |

## 原始 Prompt 快照

```text
你正在扮演工作区 Harness「30-execute-code · 执行编码帽」，严格遵循 docs/harness/prompts/30-execute-code.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`（已 rebase 到 main）
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 关联任务审核书面结论路径：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md`
- 关联 PLAN / 总规：`docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md`

**本棒目标：P0-3 多轮 Transcript**

P0-3 具体要求（来自 PLAN §2、§3.1 D3）：
- 新增 `api/ops/chat_context.py`：实现 `load_chat_transcript(session_id, n=6)`，从已有 `ops_runs` + `ops_run_events` 读取最近 N 轮用户/助手消息
- 修改 `api/ops/chat_service.py`：确保入口能接收并透传 `session_id` 到 deep/ReAct 调用
- 修改 `api/ops/orchestrator/core.py` 的 `run_deep` 与 `api/ops/react_loop.py` 的 `run_react_fallback`：在调用 LLM 前将 transcript（最近 N 轮）注入 prompt / messages 上下文
- 保持无 `session_id` 时单轮兼容（P0-3 失败路径 F2）
- 复用 P0-2 的 events schema 记录 handoff/review 事件（不改 P0-2 实现）

**范围限制**
- 只做 P0-3；不改 P0-4 tracing、P1 artifacts/checkpoint/clarify/router
- 不改 `harness_runtime` 生产图
- 不改 Agently lab
- 不改前端代码
- 不新建数据库表（使用已有 `ops_runs` / `ops_run_events`）

**test_strategy: required**
- 先写/调整可失败的自动化测试，再改实现
- 新增 `tests/ops/test_chat_context.py` 覆盖：`load_chat_transcript` 返回最近 N 轮、空 session 兼容、无 session_id 时返回空列表
- 新增/更新集成测：同一 session_id 第二轮问题能继承第一轮 issue 号（可用 mock store）
- 最终验证命令必须绿

**失败路径关注（task 中 F2）**
- 无 `session_id` 时 transcript 为空 · 单轮兼容 · 不抛异常
- 可观测：`chat_context.no_session_id` debug 日志

**你必须完成**
0. **Invoke 快照（开帽起点）**：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_30_ops_chat_session_sink_p0_p1_P0-3.md`（含元数据表 + 快照 fenced code）。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（30）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 通读 task 全文：头部 gates_before_code、audit_profile、orchestration、chain_prompt、test_strategy / test_strategy_note、failure_paths、验收标准、必读列表、非范围。
2. 阅读 PLAN §2、§3.1 与关联 SNAPSHOT/gap matrix。
3. 先读现有代码：`api/ops/chat_service.py`、`api/ops/orchestrator/core.py`、`api/ops/react_loop.py`、`api/ops/store/runs.py`、`api/ops/events_schema.py`。
4. 先写失败可复现的测试（`tests/ops/test_chat_context.py` 与必要集成测），再实现 `api/ops/chat_context.py` 与上下文注入。
5. 执行验证命令，保留可核对输出要点；修复直至通过。
6. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（执行者）· P0-3」小节（新增）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒 40 自检执行。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python/ commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
9. **禁止**自行 push；由 Lead 合并。

**输出要求**
- 若拒开工：仅 Markdown 阻塞清单
- 若执行：diff 摘要、验证命令输出、commit short-hash、下一棒 40 Prompt

**Judgment（本帽 · 对话末尾必填）**：experience_capture / gate/risk / hat_self
```
