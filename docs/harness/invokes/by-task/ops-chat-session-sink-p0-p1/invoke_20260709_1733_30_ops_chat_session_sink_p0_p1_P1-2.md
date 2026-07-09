---
hat: "30-execute-code"
task: "ops-chat-session-sink-p0-p1"
phase: "P1-2"
subproject: "ai-ink-brain-api-python"
branch: "task/ops-chat-session-sink-p0-p1"
worktree_root: "ai-ink-brain-api-python/"
date: "2026-07-09"
time: "17:33"
---

| 字段 | 值 |
| --- | --- |
| **hat** | 30-execute-code |
| **task** | ops-chat-session-sink-p0-p1 |
| **phase** | P1-2 Checkpoint |
| **subproject** | ai-ink-brain-api-python |
| **branch** | task/ops-chat-session-sink-p0-p1 |
| **worktree_root** | ai-ink-brain-api-python/ |
| **date** | 2026-07-09 |
| **time** | 17:33 |

## 用户消息快照

```text
你正在扮演工作区 Harness「30-execute-code · 执行编码帽」，严格遵循 docs/harness/prompts/30-execute-code.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`（已基于 main fast-forward，包含 P1-1 merge）
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 关联任务审核书面结论路径：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md`
- 关联 PLAN / 总规：`docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md`

**本棒目标：P1-2 Checkpoint 续跑 · `ops_run_checkpoints` 适配**

P1-2 具体要求（来自 PLAN §2、§3.1 D7、task §失败路径、§实现备忘）：
- 复用已有 `ops_run_checkpoints` 表（见 `supabase/sql/ops_desk_p1_run_schema.sql`）。
- 新增 `api/ops/store/checkpoints.py` 或扩展 `api/ops/store/runs.py`：实现 `save_checkpoint(run_id, thread_id, state_json)` 与 `load_checkpoint(run_id, thread_id)`。
- 在 `api/ops/react_loop.py` 的 ReAct 路径中：
  - 每步（或关键超步）后保存 checkpoint；
  - 同 session 续问时，若存在有效 checkpoint，隐式恢复并续跑；
  - 损坏的 checkpoint 按 task §失败路径处理：新 run 冷启动、不 500、记录 `checkpoint.corrupted` event。
- 优先保证 ReAct 续跑完成；deep 路径可暂不支持 checkpoint（按 PLAN 范围）。

**范围限制**
- 只做 P1-2；不改 P1-3 clarify、P1-4 LLM router
- 不改 P1-1 artifact 已交付行为
- 不改 `harness_runtime` 生产图
- 不改 Agently lab
- 不改前端代码

**test_strategy: required**
- 先写/调整可失败的自动化测试，再改实现
- 新增/扩展 `tests/ops/test_checkpoint.py` 覆盖：
  - save/load checkpoint 成功
  - checkpoint 损坏时冷启动且不 500
  - 同 session 续跑完成（可 mock 超步中断）
  - `checkpoint.corrupted` event 被记录
- 最终验证命令必须绿

**失败路径硬性检查**
- task §失败路径已列 `Checkpoint 损坏`：行为 = 新 run 冷启动 · 不 500；可观测 = `checkpoint.corrupted` 日志 / `ops_run_events.kind=checkpoint.corrupted`；可重试 = 否；验证命令 = `pytest tests/ops/test_checkpoint.py -k corrupted`

**你必须完成**
0. **Invoke 快照（开帽起点）**：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_30_ops_chat_session_sink_p0_p1_P1-2.md`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（30）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 通读 task 全文：头部 gates_before_code、audit_profile、orchestration、chain_prompt、test_strategy / test_strategy_note、failure_paths、验收标准、必读列表、非范围。
2. 阅读 PLAN §2、§3.1 与关联 SNAPSHOT/gap matrix。
3. 先读现有代码：`api/ops/store/runs.py`、`api/ops/react_loop.py`、`api/ops/events_schema.py`、`api/ops/chat_service.py`，以及 `supabase/sql/ops_desk_p1_run_schema.sql` 中 `ops_run_checkpoints` 表结构。
4. 先写失败可复现的测试（`tests/ops/test_checkpoint.py`），再实现 checkpoint save/load/resume/corrupted 处理。
5. 在 ReAct 路径中合适位置集成 checkpoint。
6. 执行验证命令，保留可核对输出要点；修复直至通过。
7. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（执行者）· P1-2」小节（不要覆盖 P0 或 P1-1 已有结论）。
8. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒 40 自检执行。
9. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python/ commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
10. **禁止**自行 push；由 Lead 合并。

**输出要求**
- 若拒开工：仅 Markdown 阻塞清单
- 若执行：diff 摘要、验证命令输出、commit short-hash、下一棒 40 Prompt

**Judgment（本帽 · 对话末尾必填）**：experience_capture / gate/risk / hat_self
```
