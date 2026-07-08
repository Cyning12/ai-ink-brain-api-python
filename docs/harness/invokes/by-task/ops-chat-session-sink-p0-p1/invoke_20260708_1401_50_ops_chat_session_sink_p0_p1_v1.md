# Harness invoke snapshot

| 字段 | 值 |
| --- | --- |
| hat_id | 50 |
| template | docs/harness/prompts/TEMPLATE-independent-reinspect-invoke.md §3 |
| task_paths | docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md |
| related_plan | docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md |
| prior_40_invoke | ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260708_1400_40_ops_chat_session_sink_p0_p1_v1.md |
| prior_30_commit | d590afd3 |
| git_branch | task/ops-chat-session-sink-p0-p1 |
| worktree_root | ai-ink-brain-api-python |
| created_utc_or_local | 2026-07-08 14:01 CST |
| notes | audit_profile=full；本帽为独立复检 + 全局验收 |

## 可复制 Prompt 快照

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md（§一 独立复检；§二 全局验收）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy: required 时关注测试与实现关系）
- 根目录 AGENTS.md §8、docs/harness/HARNESS_V2_P0_ACCEPTANCE.md

输入（占位符已全部替换；若你仍看到 {{…}} 或 REINSPECT_MODE 非三选一字面，须先追问用户，不得开工）：
- 主 task 路径：
docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md
- 子仓根（相对 Projects/；用于理解 diff 与路径）：
ai-ink-brain-api-python
- 模式（必须恰好为以下之一：独立复检 / 全局验收 / 两者）：
两者
- diff 或变更范围说明：
git diff origin/main...HEAD
- 任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列分节实质性结果之前，先将 **本用户消息全文** 按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问不再新增快照文件。

【当模式为「独立复检」或「两者」时 — 对应 hat §一】
1. 读取 task 内「### 自检结论（执行者）」与新增「### 自检结论（40 复核）」；若缺失 → 阻塞首条：要求先跑 40。
2. 输入裁剪：以 diff、命令输出要点、自检验收表为主；避免执行过程长文。
3. 对 task P0-1 验收项输出表格：验收项 | pass/fail | 证据（文件:行 / 测试名 / 日志片段）| 备注；fail 须写复现步骤或缺失证据。
4. 重点核验：
   - `api/ops/review/rules.py` 是否单点承载 V1–V4；
   - `api/ops/orchestrator/core.py` 与 `api/ops/react_loop.py` 是否均从共享模块导入 `review_result`；
   - `tests/ops/test_review_rules.py` 是否覆盖 V1/V2/V3/V4、优先级、deep/ReAct 共用、向后兼容；
   - 验证命令 `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` 是否通过。
5. 汇总阻塞合并项；给出是否建议合并（供维护者决策）。
6. 禁止：替执行者改代码（除非用户明确要求复检提交 patch）；缺口默认退回 30/40。

【当模式为「全局验收」或「两者」时 — 对应 hat §二】
7. 核对本次 PR 变更是否在 P0-1 冻结基准内；未涉及 P0-2/3/4、P1、Session 生产图、Agently lab。
8. 输出 checklist 表（项 / 状态 / 签注栏「待人工」）；不伪造已签核；不跳过 CI 红灯叙事。

对话回复：
- 若建议合并且无返工 → 输出「执行路线与 Commit 回溯」（docs/harness/prompts/HANDOFF_CLOSE_TRACE.md），勿编造下一棒 Prompt。
- 若须打回 → 输出下一棒可复制 Prompt（按 50 打回路由表选最短回路：30 / 40 / 10-task / 20-task-audit 等），含修复要点。

9. **自动 commit**：落盘后按 docs/harness/prompts/HANDOFF_AUTO_COMMIT.md 分仓 commit。仅对话、零文件变更则不必空提交；用户写明「不要 commit」则跳过。

Judgment（本帽 · 对话末尾必填；任一项 warn/fail 须写 judgment_notes）：
- experience_capture: 维持 | 建议升级 required | 建议降 n/a | 维持 n/a（≤1 行理由）
- gate/risk: 无 | 须人审:<HG-id> | 证据不足
- hat_self: pass | pass-with-notes | blocked
```
