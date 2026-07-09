# 30 执行编码帽 · Invoke 快照

| 字段 | 内容 |
| --- | --- |
| **timestamp** | 20260709_1622 |
| **hat** | 30-execute-code |
| **task_slug** | ops-chat-session-sink-p0-p1 |
| **subtask** | P1-1 Artifacts → Supabase |
| **git_branch** | task/ops-chat-session-sink-p0-p1 |
| **worktree_root** | ai-ink-brain-api-python/ |
| **verify_command** | `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` |
| **task_path** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **audit_review_path** | `ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md` |
| **plan_path** | `docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md` |

## 用户消息快照

```text
你正在扮演工作区 Harness「30-execute-code · 执行编码帽」，严格遵循 docs/harness/prompts/30-execute-code.md。

**输入（已替换占位符）**
- 主 task 路径（相对 Projects/）：`docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md`
- 逻辑子仓（相对 Projects/）：`ai-ink-brain-api-python`
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd）：`ai-ink-brain-api-python`
- 当前分支：`task/ops-chat-session-sink-p0-p1`（已基于 main fast-forward）
- 合并前须跑通的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 关联任务审核书面结论路径：`ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md`
- 关联 PLAN / 总规：`docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md`

**本棒目标：P1-1 Artifacts → Supabase**

P1-1 具体要求（来自 PLAN §2、§3.1 D6、task §失败路径、§实现备忘）：
- 新建 Supabase 表 `ops_run_artifacts`：至少含 `run_id` (uuid, FK ops_runs)、`kind` (text)、`payload` (jsonb)、`created_at`；与现有 `ops_run_events` 风格保持一致。
- 新增 `supabase_sql/` migration 文件（可回滚），按本仓 migration 命名与编号惯例落盘。
- 新增 `api/ops/store/artifacts.py`：实现 `save_artifact(run_id, kind, payload)`，幂等写入 `ops_run_artifacts`；失败时抛出自说明异常。
- 在 `api/ops/orchestrator/core.py` 的 deep 路径与 `api/ops/react_loop.py` 的 ReAct 路径中，于关键结果产出处调用 `save_artifact`，将 deep/ReAct 结果写入 DB artifact（kind 建议如 `deep.final_answer`、`react.final_answer`，或按 task 失败路径约定）。
- 与 P0-2 events 集成：artifact 写失败时，须记录 `ops_run_events` 事件 `kind=artifact.write_failed`，并仍返回答案（见 task §失败路径）。

**范围限制**
- 只做 P1-1；不改 P1-2 checkpoint、P1-3 clarify、P1-4 LLM router
- 不改 `harness_runtime` 生产图
- 不改 Agently lab
- 不改前端代码

**test_strategy: required**
- 先写/调整可失败的自动化测试，再改实现
- 新增 `tests/ops/test_artifacts.py` 覆盖：
  - `save_artifact` 成功写入并可按 run_id 读取
  - schema 字段（run_id / kind / payload / created_at）存在
  - 写失败时生成 `artifact.write_failed` event（可 mock Supabase 失败）
  - deep / ReAct 路径在运行时调用 save_artifact（可 mock 或集成）
- 最终验证命令必须绿

**失败路径硬性检查**
- task §失败路径已列 `Supabase artifact 写失败`：行为 = 记录 event `artifact.write_failed` + 仍返回答案；可观测 = `ops_run_events` 行 `kind=artifact.write_failed`；可重试 = 幂等重试 N 次后仍失败则记录；验证命令 = `pytest tests/ops/test_artifacts.py -k write_failed`

**你必须完成**
0. **Invoke 快照（开帽起点）**：将本用户消息全文落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_30_ops_chat_session_sink_p0_p1_P1-1.md`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（30）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 通读 task 全文：头部 gates_before_code、audit_profile、orchestration、chain_prompt、test_strategy / test_strategy_note、failure_paths、验收标准、必读列表、非范围。
2. 阅读 PLAN §2、§3.1 与关联 SNAPSHOT/gap matrix。
3. 先读现有代码：`api/ops/store/runs.py`、`api/ops/events_schema.py`、`api/ops/orchestrator/core.py`、`api/ops/react_loop.py`、`api/ops/review/rules.py`。
4. 先写失败可复现的测试（`tests/ops/test_artifacts.py`），再实现 migration、`api/ops/store/artifacts.py` 与写入点。
5. 在 deep/ReAct 路径中合适位置调用 `save_artifact`，并保证失败时记录 `artifact.write_failed` event。
6. 执行验证命令，保留可核对输出要点；修复直至通过。
7. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（执行者）」小节（在 P1-1 区域新增；不要覆盖 P0 已有结论）。
8. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒 40 自检执行。
9. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python/ commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
10. **禁止**自行 push；由 Lead 合并。

**输出要求**
- 若拒开工：仅 Markdown 阻塞清单
- 若执行：diff 摘要、验证命令输出、commit short-hash、下一棒 40 Prompt

**Judgment（本帽 · 对话末尾必填）**：experience_capture / gate/risk / hat_self
```
