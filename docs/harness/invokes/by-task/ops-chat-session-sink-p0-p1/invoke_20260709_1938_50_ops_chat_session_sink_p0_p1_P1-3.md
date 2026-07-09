# 50-self-check Invoke Snapshot · P1-3

| 项 | 内容 |
| --- | --- |
| **hat** | 50-self-check |
| **task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **phase** | P1-3 Clarify 路由 |
| **branch** | `task/ops-chat-session-sink-p0-p1` |
| **timestamp** | 2026-07-09 19:38 |
| **verify_command** | `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` |

## Input Snapshot

```text
你正在扮演工作区 Harness「50-self-check · 独立复检 + 全局验收帽」，严格遵循 docs/harness/prompts/50-self-check.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`（已基于 main fast-forward，包含 P1-2 merge）
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 上一棒 30 commit：`ai-ink-brain-api-python @ 8f90cb5a`
- 上一棒 40 commit：`ai-ink-brain-api-python @ ea31eae8`
- 关联任务审核书面结论路径：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md`
- 关联 PLAN / 总规：`docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md`

**本棒目标：P1-3 独立复检 + 全局验收**

你必须完成：
0. **Invoke 快照（开帽起点）**：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_50_ops_chat_session_sink_p0_p1_P1-3.md`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（50）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 独立阅读 task 正文「### 自检结论（执行者）· P1-3」与「### 自检结论（40 复核）· P1-3」小节。
2. 独立阅读本轮 P1-3 改动代码：
   - `api/ops/orchestrator/clarify.py`
   - `api/ops/orchestrator/__init__.py`
   - `api/ops/chat_service.py`
   - `tests/ops/test_clarify.py`
   - `tests/ops/test_chat_service.py`
   - `tests/ops_desk/test_react_fallback.py`（clarify 旁路适配）
3. 在 `ai-ink-brain-api-python/` 内完整执行验证命令：
   ```bash
   pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
   ```
4. 执行 `git diff origin/main...HEAD --stat`（在 `ai-ink-brain-api-python` 内）核对全量变更路径，确认未扩 scope 到 P1-4 LLM Router、P1-1 artifact、P1-2 checkpoint、Session 生产图、Agently lab、前端。
5. 与 30 commit `8f90cb5a`、40 commit（待回填）、R2 任务审核书面结论逐条核对。
6. 50 复检书面结论落盘：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R1_20260709_50_P1-3.md`。
7. 按 50-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（50 复检）· P1-3」小节（不要覆盖 P0、P1-1、P1-2、30、40 已有结论）。
8. 对话回复：给出是否建议合并、阻塞项清单、全局验收结论。
9. 自动 commit：在输出最终结论且本轮 reviews/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 `ai-ink-brain-api-python/` commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
10. **禁止**自行 push；由 Lead 合并。

**输出要求**
- 若拒开工：仅 Markdown 阻塞清单
- 若执行：diff 摘要、验证命令输出、commit short-hash、合并建议、全局验收表

**Judgment（本帽 · 对话末尾必填）**：experience_capture / gate/risk / hat_self
```
