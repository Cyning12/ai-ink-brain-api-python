# 30-execute-code Invoke Snapshot · P1-3

| 项 | 内容 |
| --- | --- |
| **hat** | 30-execute-code |
| **task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **phase** | P1-3 Clarify 路由 |
| **branch** | `task/ops-chat-session-sink-p0-p1` |
| **timestamp** | 2026-07-09 19:21 |
| **verify_command** | `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` |

## Input Snapshot

```text
你正在扮演工作区 Harness「30-execute-code · 执行编码帽」，严格遵循 docs/harness/prompts/30-execute-code.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`（已基于 main fast-forward，包含 P1-2 merge）
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 关联任务审核书面结论路径：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md`
- 关联 PLAN / 总规：`docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md`

**本棒目标：P1-3 Clarify 路由：FALLBACK 先澄清 · 减少默认 `#545`**

P1-3 具体要求（来自 PLAN §2、§3.1 D8、task §实现备忘）：
- 新增 `api/ops/orchestrator/clarify.py`：实现 `clarify_if_fallback(query, session_id, transcript, slots)`。
- 当 `classify_intent` 返回 `Intent.FALLBACK` 时，不直接进入 ReAct fallback，而是先调用 clarify 模块。
- Clarify 模块通过 LLM asking 1 轮澄清问题（或基于规则兜底），返回：
  - `needs_clarification=true` + `clarify_question`：Chat 侧展示澄清卡片，等待用户补充；
  - `needs_clarification=false` + 补齐后的 slots/intent：继续走原 deep/ReAct 路由。
- 在 `api/ops/chat_service.py` 中替换现有 `Intent.FALLBACK → run_react_fallback` 的 silent 行为：先 clarify，再根据 clarify 结果路由。
- 减少默认 `#545`：FALLBACK 测例不再默认 issue #545（除非 clarify 后明确指向 #545）。
- 利用 P0-3 transcript 能力（`load_chat_transcript`）为 clarify 提供上下文。

**范围限制**
- 只做 P1-3；不改 P1-4 LLM Router
- 不改 P1-1 artifact、P1-2 checkpoint 已交付行为
- 不改 `harness_runtime` 生产图
- 不改 Agently lab
- 不改前端代码（前端 F1-1 在单独 task，后端仅输出 `needs_clarification` 字段）

**test_strategy: required**
- 先写/调整可失败的自动化测试，再改实现
- 新增/扩展 `tests/ops/test_clarify.py` 与 `tests/ops/test_chat_service.py` 覆盖：
  - FALLBACK 进入 clarify 而不是直接 ReAct
  - clarify 返回需要澄清时，`needs_clarification=true` 且不含默认 #545
  - clarify 返回不需要澄清时，继续走 deep/ReAct 并携带补齐 slots
  - 无 session_id 时 clarify 仍能单轮工作
- 最终验证命令必须绿

**失败路径硬性检查**
- task §失败路径未单独列 clarify，但须保证原有失败路径不被破坏（artifact 写失败、checkpoint 损坏等仍按原逻辑）。
- 新增 clarify LLM 调用失败时：降级为直接 ReAct fallback（保持可用性）。

**你必须完成**
0. **Invoke 快照（开帽起点）**：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_30_ops_chat_session_sink_p0_p1_P1-3.md`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（30）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 通读 task 全文：头部 gates_before_code、audit_profile、orchestration、chain_prompt、test_strategy / test_strategy_note、failure_paths、验收标准、必读列表、非范围。
2. 阅读 PLAN §2、§3.1 与关联 SNAPSHOT/gap matrix。
3. 先读现有代码：`api/ops/intent_router.py`、`api/ops/chat_service.py`、`api/ops/chat_context.py`、`api/ops/orchestrator/core.py`、`api/ops/react_loop.py`。
4. 先写失败可复现的测试（`tests/ops/test_clarify.py`），再实现 `api/ops/orchestrator/clarify.py` 与 `chat_service.py` 路由改造。
5. 执行验证命令，保留可核对输出要点；修复直至通过。
6. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（执行者）· P1-3」小节（不要覆盖 P0、P1-1、P1-2 已有结论）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒 40 自检执行。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python/ commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
9. **禁止**自行 push；由 Lead 合并。

**输出要求**
- 若拒开工：仅 Markdown 阻塞清单
- 若执行：diff 摘要、验证命令输出、commit short-hash、下一棒 40 Prompt

**Judgment（本帽 · 对话末尾必填）**：experience_capture / gate/risk / hat_self
```
