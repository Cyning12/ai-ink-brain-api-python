# Task · Ops Session S1 Multiturn API（sessions REST · DB 绑定 · messages）

> **状态**：`done（2026-07-02 验收通过）`  
> **epic**：Session Orchestrator · S1 `ops-session-s1-multiturn`  
> **schedule_ref**：SPEC §12.1 S1 · MVP 首片（S0+S1+S2）  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) §9 · §12 S1 · §13  
> **前置**：[`task_ops_session_s0_schema_v1.md`](task_ops_session_s0_schema_v1.md) · PR #226  
> **配对前端**：[`task_ops_session_s1_multiturn_ui_v1.md`](../../../ai-ink-brain/content/tasks/done/task_ops_session_s1_multiturn_ui_v1.md) · PR #106  
> **20-task-audit**：[`task_ops_session_s1_multiturn_api_v1_audit_R1_20260702.md`](../harness/reviews/by-task/ops-session-s1-multiturn-api/task_ops_session_s1_multiturn_api_v1_audit_R1_20260702.md)  
> **50-reinspect**：工作区 [`task_ops_session_s1_multiturn_reinspect_R1_20260702.md`](../../../docs/harness/reviews/task_ops_session_s1_multiturn_reinspect_R1_20260702.md)  
> **PR**：[#228](https://github.com/Cyning12/ai-ink-brain-api-python/pull/228) merged

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-session-s1-multiturn-api` |
| **module_id** | `OPS-SESSION-ORCH` |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **test_strategy** | `required` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **git_branch** | `task/ops-session-s1-multiturn-api` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 2026-07-02 |
| HG-AUDIT-R1 | `approved` | 30 | 2026-07-02 |

---

## 范围（已交付）

- [x] `api/ops/sessions.py` + `ops_router` 注册
- [x] POST/GET `/ops/sessions` · GET/POST `.../messages` · GET `.../events`
- [x] `api/ops/chat_service.py` 编排复用 · 单轮 `chat.py` 精简
- [x] `OpsRunStore.list_runs_by_session_id` · `list_events_for_session`
- [x] `session.created` / `session.status_changed` · `latest_run_id` 回写
- [x] `tests/ops_desk/test_sessions_s1.py` · harness_runtime 回归

---

## 验收标准

- [x] SPEC §9.2 S1 子集（无 auth/promote）
- [x] 1:N `ops_runs.session_id` · `latest_run_id`
- [x] `/ops/chat/messages` 不退化
- [x] pytest + ruff 绿 · 本地验收 checklist 人签

---

## 实现备忘

| 路径 | 说明 |
| --- | --- |
| `api/ops/sessions.py` | Session REST |
| `api/ops/chat_service.py` | 单轮与 session messages 共享编排 |
| `api/harness_runtime/session_store/io.py` | `list_sessions` · `session_dir_for_id` |
| `tests/ops_desk/test_sessions_s1.py` | S1 API 测试 |

---

## 行为变更（Delta）

### ADDED

- `api/ops/sessions.py` · Session REST（create/list/messages/events）
- `api/ops/chat_service.py` · 单轮与 session messages 共享编排

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-session-not-found | 无效 `session_id` | `404 SESSION_NOT_FOUND` |
| F2 | fp-ops-secret-invalid | 错误或未传 `x-ops-secret` | `401` |
| F3 | fp-message-empty | messages body 为空 | `422` 校验失败 |
