# Invoke Snapshot · 30-execute-code · ops-chat-session-sink-p0-p1 · P1-4

| 字段 | 值 |
| --- | --- |
| **hat** | 30-execute-code |
| **task** | docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md |
| **subproject** | ai-ink-brain-api-python |
| **branch** | task/ops-chat-session-sink-p0-p1 |
| **scope** | P1-4 LLM Router：`OPS_CHAT_LLM_ROUTER` · JSON intent · 规则 fallback |
| **timestamp** | 2026-07-10 09:29 |
| **verify_command** | `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` |
| **human_gate** | `HG-TASK-DRAFT`: approved (task §行为变更 · human_gate) · `HG-AUDIT-R1`: approved (task §行为变更 · human_gate) |

## 用户消息快照

```text
你正在扮演工作区 Harness「30-execute-code · 执行编码帽」，严格遵循 docs/harness/prompts/30-execute-code.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`（已基于 main fast-forward，包含 P1-3 merge）
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 关联任务审核书面结论路径：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md`
- 关联 PLAN / 总规：`docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md`
- 关联结构化输出缺口矩阵：`docs/harness/guides/RUNTIME_structured_output_gap_matrix_v0_zh.md`

**本棒目标：P1-4 LLM Router：`OPS_CHAT_LLM_ROUTER` · JSON intent · 规则 fallback**

P1-4 具体要求（来自 PLAN §2、§3.1 D9、task §失败路径、§实现备忘）：
- 新增 `api/ops/intent_router.py`：实现基于 LLM 的轻量 JSON intent 路由器。
- 当环境变量 `OPS_CHAT_LLM_ROUTER=1` 时，`api/ops/orchestrator/core.py` 中的 `classify_intent` 优先调用 LLM router。
- LLM router 输出 JSON：至少含 `intent`（字符串）、`slots`（对象）、`confidence`（float，0~1）。
- 低置信度或非法 JSON 时降级为原有规则 `classify_intent`（即 task §失败路径的 `intent_router.fallback` event / `router.latency` 日志）。
- 默认 `OPS_CHAT_LLM_ROUTER` 未开启或未设置时，行为与之前完全一致（向后兼容）。
- 记录 `intent_router.fallback` event 到 `ops_run_events`（可复用 P0-2 `append_event`）。

**范围限制**
- 只做 P1-4；不改 P1-1 artifact、P1-2 checkpoint、P1-3 clarify 已交付行为
- 不改 `harness_runtime` 生产图
- 不改 Agently lab
- 不改前端代码

**test_strategy: required**
- 先写/调整可失败的自动化测试，再改实现
- 新增 `tests/ops/test_intent_router.py` 覆盖：
  - `OPS_CHAT_LLM_ROUTER=1` 时 LLM router 返回合法 JSON intent
  - 低置信度时降级规则 fallback
  - LLM 超时/非法 JSON 时降级规则 fallback（对应 task §失败路径）
  - 默认未开启时走原有规则
  - 1 个集成测：通过 `classify_intent` 走 LLM router
- 最终验证命令必须绿

**失败路径硬性检查**
- task §失败路径已列 `LLM router 超时/非法 JSON`：行为 = 降级 `classify_intent` 规则；可观测 = `intent_router.fallback` event / `router.latency` 日志；可重试 = 否；验证命令 = `pytest tests/ops/test_intent_router.py -k fallback`

**你必须完成**
0. **Invoke 快照（开帽起点）**：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_30_ops_chat_session_sink_p0_p1_P1-4.md`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（30）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 通读 task 全文：头部 gates_before_code、audit_profile、orchestration、chain_prompt、test_strategy / test_strategy_note、failure_paths、验收标准、必读列表、非范围。
2. 阅读 PLAN §2、§3.1、`RUNTIME_structured_output_gap_matrix_v0_zh.md` 与关联 SNAPSHOT。
3. 先读现有代码：`api/ops/orchestrator/core.py`（`classify_intent` 与 `Intent` 枚举）、`api/ops/events_schema.py`、`api/ops/chat_service.py`。
4. 先写失败可复现的测试（`tests/ops/test_intent_router.py`），再实现 `api/ops/intent_router.py` 与 `classify_intent` 改造。
5. 执行验证命令，保留可核对输出要点；修复直至通过。
6. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（执行者）· P1-4」小节（不要覆盖 P0、P1-1、P1-2、P1-3 已有结论）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒 40 自检执行。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python/ commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
9. **禁止**自行 push；由 Lead 合并。

**输出要求**
- 若拒开工：仅 Markdown 阻塞清单
- 若执行：diff 摘要、验证命令输出、commit short-hash、下一棒 40 Prompt

**Judgment（本帽 · 对话末尾必填）**：experience_capture / gate/risk / hat_self
```
