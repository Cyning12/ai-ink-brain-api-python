# Invoke Snapshot · 50-independent-reinspect · P0-4

| 项 | 内容 |
| --- | --- |
| **task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **hat** | `50-independent-reinspect` |
| **phase** | `P0-4` |
| **date** | `2026-07-09` |
| **timestamp** | `20260709_1436` |
| **branch** | `task/ops-chat-session-sink-p0-p1` |
| **human_gate** | `HG-TASK-DRAFT: approved`, `HG-AUDIT-R1: approved` |

## 原始 Prompt 快照

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md（§一 独立复检；§二 全局验收）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy: required 时关注测试与实现关系）
- 根目录 AGENTS.md §8、docs/harness/HARNESS_V2_P0_ACCEPTANCE.md（若本次变更触及合并前必绿子仓）

输入（已由人工替换占位符；若你仍看到 {{…}} 或 REINSPECT_MODE 非三选一字面，须先追问用户，不得开工）：
- 主 task 路径（相对 Projects/）：
  docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md
- 子仓根（相对 Projects/；用于理解 diff 与路径）：
  ai-ink-brain-api-python
- 模式（必须恰好为以下之一：独立复检 / 全局验收 / 两者）：
  两者
- diff 或变更范围说明（全局验收单独模式可写「无」）：
  git diff origin/main...HEAD
- 任务审核书面结论路径（无则「无」）：
  ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列分节实质性结果之前，先将 **本用户消息全文**（= 本 Prompt、占位符已全部替换）落盘到 `ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_50_ops_chat_session_sink_p0_p1_P0-4.md`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。

【当模式为「独立复检」或「两者」时 — 对应 hat §一】
1. 读取 task 内「### 自检结论（执行者）· P0-4」及「### 自检结论（40 复核）· P0-4」；若缺失 → 阻塞首条：要求先跑 TEMPLATE-self-check-invoke + 40。
2. 输入裁剪：以 diff、命令输出要点、自检验收表为主；避免执行过程长文。
3. 对 P0-4 每条验收项输出表格：验收项 | pass/fail | 证据（文件:行 / 测试名 / 日志片段）| 备注；fail 须写复现步骤或缺失证据。
   重点核验：
   - `api/ops/tracing.py` 是否实现 `OPS_CHAT_TRACER` 主控开关（`langfuse` / `langsmith` / none）。
   - 是否保留旧 `LANGFUSE_TRACING` / `LANGSMITH_TRACING` 兼容。
   - `trace_span(...)` 上下文管理器是否存在且默认无操作。
   - `run_deep` / `run_react_fallback` 入口是否加 `run_id` / `session_id` / `agent_role` 元数据。
   - handoff / review 热路径是否包 `with trace_span(...)`。
   - 未设置 env 时是否零成本、不报错。
   - `tests/ops/test_tracing.py` 是否覆盖开关、mock span、元数据。
   - 是否未改 P1、Session 生产图、Agently lab、前端代码。
4. 执行 `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops` 并粘贴输出要点；与 30 / 40 结论交叉核对。
5. 通过 `git diff --name-status origin/main...HEAD` 核对全量变更路径，确认未扩 scope 到 P1、Session 生产图、Agently lab、前端。
6. 汇总阻塞合并项；给出是否建议合并（供维护者决策）。
7. 禁止：替执行者改代码（除非用户明确要求复检提交 patch）；缺口退回需求/审查帽。

【当模式为「全局验收」或「两者」时 — 对应 hat §二】
8. 核对本次 PR 变更是否在 P0-4 声明范围内；契约升级（tracing 元数据规范）是否在 task 行为变更节显式记录。
9. 输出 checklist 表（项 / 状态 / 签注栏「待人工」）；不伪造已签核；不跳过 CI 红灯叙事。

对话回复：若建议合并且无返工 → 输出「执行路线与 Commit 回溯」（docs/harness/prompts/HANDOFF_CLOSE_TRACE.md），勿编造下一棒 Prompt；若须打回 → 输出下一棒可复制 Prompt（按 50 打回路由表选最短回路；含打回、二次审查、上一棒修复）。
10. **自动 commit**：落盘后按 docs/harness/prompts/HANDOFF_AUTO_COMMIT.md 分仓 commit。仅对话、零文件变更则不必空提交；用户写明「不要 commit」则跳过。

Judgment（本帽 · 对话末尾必填；任一项 warn/fail 须写 judgment_notes）：
- experience_capture: 维持 | 建议升级 required | 建议降 n/a | 维持 n/a（≤1 行理由）
- gate/risk: 无 | 须人审:<HG-id> | 证据不足
- hat_self: pass | pass-with-notes | blocked
```
