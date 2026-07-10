---
hat: "40-self-check"
task: "ops-chat-session-sink-p0-p1"
phase: "P1-4"
subproject: "ai-ink-brain-api-python"
branch: "task/ops-chat-session-sink-p0-p1"
worktree_root: "ai-ink-brain-api-python/"
date: "2026-07-10"
time: "09:30"
---

| 字段 | 值 |
| --- | --- |
| **hat** | 40-self-check |
| **task** | ops-chat-session-sink-p0-p1 |
| **phase** | P1-4 LLM Router |
| **subproject** | ai-ink-brain-api-python |
| **branch** | task/ops-chat-session-sink-p0-p1 |
| **worktree_root** | ai-ink-brain-api-python/ |
| **date** | 2026-07-10 |
| **time** | 09:30 |

## 用户消息快照

```text
你正在扮演工作区 Harness「40-self-check · 执行者自检帽」，严格遵循 docs/harness/prompts/40-self-check.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`（已基于 main fast-forward，包含 P1-3 merge）
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 失败路径验证命令：
  ```bash
  pytest tests/ops/test_intent_router.py -k fallback -q
  ```
- 上一棒 30 commit：待本 Prompt 落盘后从 30 输出获取
- 关联任务审核书面结论路径：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md`
- 关联 PLAN / 总规：`docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md`
- 关联结构化输出缺口矩阵：`docs/harness/guides/RUNTIME_structured_output_gap_matrix_v0_zh.md`

**本棒目标：P1-4 自检复核**

你必须完成：
0. **Invoke 快照（开帽起点）**：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_40_ops_chat_session_sink_p0_p1_P1-4.md`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（40）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 独立阅读 task 正文「### 自检结论（执行者）· P1-4」小节与上一棒 30 invoke 快照 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260710_0929_30_ops_chat_session_sink_p0_p1_P1-4.md`。
2. 独立阅读本轮 P1-4 改动代码：
   - `api/ops/intent_router.py`
   - `api/ops/orchestrator/core.py`（`classify_intent` / `_rule_classify_intent`）
   - `tests/ops/test_intent_router.py`
3. 在 `ai-ink-brain-api-python/` 内完整执行 30 声明的验证命令：
   ```bash
   pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
   ```
   并单独执行失败路径验证命令：
   ```bash
   pytest tests/ops/test_intent_router.py -k fallback -q
   ```
4. 通过 `git diff origin/main...HEAD --stat`（在 `ai-ink-brain-api-python` 内）核对全量变更路径，确认未扩 scope 到 P1-1 artifact、P1-2 checkpoint、P1-3 clarify、`harness_runtime` 生产图、Agently lab、前端代码。
5. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（40 复核）· P1-4」小节（不要覆盖 P0、P1-1、P1-2、P1-3 或 30 已有结论）。
6. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒 50 独立复检执行。
7. 自动 commit：在输出下一棒 Prompt 且本轮 task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 `ai-ink-brain-api-python/` commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
8. **禁止**自行 push；由 Lead 合并。

**输出要求**
- 若拒开工：仅 Markdown 阻塞清单
- 若执行：diff 摘要、验证命令输出、commit short-hash、下一棒 50 Prompt

**Judgment（本帽 · 对话末尾必填）**：experience_capture / gate/risk / hat_self
```
