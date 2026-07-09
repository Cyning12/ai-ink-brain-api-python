# Invoke · 30-execute-code · ops-chat-session-sink-p0-p1 · P0-4 Tracing

| 项 | 内容 |
| --- | --- |
| **hat** | 30-execute-code |
| **task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **git_branch** | `task/ops-chat-session-sink-p0-p1` |
| **phase** | P0-4 Tracing |
| **timestamp** | 2026-07-09T13:55:00+08:00 |
| **human_gate** | `HG-TASK-DRAFT` approved · `HG-AUDIT-R1` approved |

## 用户输入快照

```markdown
你正在扮演工作区 Harness「30-execute-code · 执行编码帽」，严格遵循 docs/harness/prompts/30-execute-code.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`（已 rebase 到最新 main，含 P0-1/P0-2/P0-3）
- 合并方式：本阶段完成后 **push 分支并开 PR**，不直接 merge
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 关联任务审核书面结论路径：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md`
- 关联 PLAN / 总规：`docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md`

**本棒目标：P0-4 Tracing**

P0-4 具体要求（来自 PLAN §2、§3.1 D4）：
- 新增 `api/ops/tracing.py`：封装 Langfuse/LangSmith trace span 创建，通过环境变量 `OPS_CHAT_TRACER`（可选值 `langfuse` / `langsmith`）启用；未设置或未知值时无操作
- 修改 `api/ops/orchestrator/core.py` 的 `run_deep` 与 `api/ops/react_loop.py` 的 `run_react_fallback`：在热路径（入口、LLM 调用、review、handoff）上加 `@trace_span` 或上下文管理器，生成可选 trace
- 保持默认无 env 时零成本、不报错、不引入新依赖（使用可选 import / lazy client）
- 记录 trace 元数据：`run_id`, `session_id`, `agent_role`（deep/react），便于后续按 run/session 查询

**范围限制**
- 只做 P0-4；不改 P1 artifacts/checkpoint/clarify/router
- 不改 `harness_runtime` 生产图
- 不改 Agently lab
- 不改前端代码
- 不新建数据库表

**test_strategy: required**
- 先写/调整可失败的自动化测试，再改实现
- 新增 `tests/ops/test_tracing.py` 覆盖：
  - 未设置 env 时 tracer 为空操作
  - 设置 `OPS_CHAT_TRACER=langfuse` / `langsmith` 时能创建 span（mock client，不依赖真实密钥）
  - `run_deep` / `run_react_fallback` 调用后产生 trace span（mock）
  - trace 元数据含 run_id / session_id / agent_role
- 最终验证命令必须绿

**你必须完成**
0. **Invoke 快照（开帽起点）**：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_30_ops_chat_session_sink_p0_p1_P0-4.md`（含元数据表 + 快照 fenced code）。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（30）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 通读 task 全文：头部 gates_before_code、audit_profile、orchestration、chain_prompt、test_strategy / test_strategy_note、failure_paths、验收标准、必读列表、非范围。
2. 阅读 PLAN §2、§3.1 与关联 gap matrix。
3. 先读现有代码：`api/ops/orchestrator/core.py`、`api/ops/react_loop.py`、`api/ops/events_schema.py`、`api/ops/chat_context.py`。
4. 先写失败可复现的测试（`tests/ops/test_tracing.py`），再实现 `api/ops/tracing.py` 与 span 接入。
5. 执行验证命令，保留可核对输出要点；修复直至通过。
6. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（执行者）· P0-4」小节（新增）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒 40 自检执行。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python/ commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
9. **不要 push**：本阶段完成后由 Lead push 分支并提醒用户开 PR。

**输出要求**
- 若拒开工：仅 Markdown 阻塞清单
- 若执行：diff 摘要、验证命令输出、commit short-hash、下一棒 40 Prompt

**Judgment（本帽 · 对话末尾必填）**：experience_capture / gate/risk / hat_self
```
