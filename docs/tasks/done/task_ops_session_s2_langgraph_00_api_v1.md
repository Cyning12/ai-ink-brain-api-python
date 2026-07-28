# Task · Ops Session S2 LangGraph 00 API（plan · auth interrupt · synthesize · 双写）

> **状态**：`done（2026-07-02 本地验收通过）`  
> **epic**：Session Orchestrator · S2 `ops-session-s2-langgraph-00`  
> **schedule_ref**：SPEC §12.1 S2 · MVP 首片（S0+S1+**S2**）  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) §6–§7 · §9.2 · §12 S2 · §13  
> **前置**：[`task_ops_session_s1_multiturn_api_v1.md`](../done/task_ops_session_s1_multiturn_api_v1.md) · PR #228 merged  
> **配对前端**：[`task_ops_session_s2_langgraph_00_ui_v1.md`](../../../ai-ink-brain/content/tasks/done/task_ops_session_s2_langgraph_00_ui_v1.md)  
> **本地验收**：[`CHECKLIST_ops_session_s2_local_acceptance_v1_zh.md`](../../../docs/harness/reviews/CHECKLIST_ops_session_s2_local_acceptance_v1_zh.md) · HG-S2-LOCAL-ACCEPTANCE  
> **PR**：暂缓 · 与 S3/S4 合并批次开 PR（`task/ops-session-s2-langgraph-00-api`）  
> **BLOCKERS**：B3（按钮主 + NL 辅）· B7（probe 可选 · 非阻塞）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-session-s2-langgraph-00-api` |
| **module_id** | `OPS-SESSION-ORCH` |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **test_strategy** | `required` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **git_branch** | `task/ops-session-s2-langgraph-00-api` |
| **blocks** | S3 `ops-session-s3-subagent` |
| **blocked_by** | S1 `ops-session-s1-multiturn-api` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 00 起草 · 2026-07-02 |
| HG-AUDIT-R1 | `approved` | 30 | 20 R1 后人签 · 2026-07-02 |

---

## 背景与目标

S1 已交付 Session REST 与多轮 messages（**仍走 P1 `chat_service` 编排**）。本 task 引入 **`session_orchestrator_v1` LangGraph 00 层**：多轮 plan → 呈现计划 → **interrupt 等人授权** → synthesize；完成 **文件 Inform + DB checkpoint/events 双写**；暴露 **`POST .../auth`**。

**完成态一句话**：`POST .../messages` 在 `planning`/`awaiting_auth` 走 00 图更新 task 草稿与计划摘要 · `POST .../auth` 结构化 `approve|revise|cancel` 同步 `HG-SESSION-PLAN` → `dispatched` · **不含** subagent dispatch（S3）。

### 拍板（00 统筹 · 2026-07-02）

| # | 决策 |
| --- | --- |
| D1 | `planning` / `awaiting_auth` 阶段 **messages 一律进 00 图**（plan/present），不走 `chat_service` deep/fast |
| D2 | `node_00_plan` / `present` 使用 **LLM 轻量计划** + 更新 session 内 `task_*.md` 草稿（非固定模板） |
| D3 | `dispatched` 后 S2 **仅 synthesize 确认文案**；deep/ReAct 明确 **S3** |
| D4 | auth 后 **可选** subprocess `harness-probe task validate`（warn-only · B7） |

---

## 范围

- [ ] **`api/harness_runtime/graph/session_orchestrator_v1.py`**：`StateGraph(SessionState)` · 图名 `session_orchestrator_v1` 与单轮图 **并存**
- [ ] **节点（S2 子集）**：`node_00_plan` · `node_00_present_plan` · `node_00_auth_gate`（`interrupt`）· `node_00_synthesize` — **无** `node_dispatch` / subagent
- [ ] **Checkpointer**：复用 `ops_run_checkpoints` · `thread_id` = `{session_id}:{run_id}` · 双写纪律 §7.3（文件 → checkpoint → events）
- [ ] **POST** `/ops/sessions/{session_id}/auth`：body `{ action: approve | revise | cancel }` → `Command(resume=...)` · 幂等已 approved
- [ ] **改造** `POST .../messages`：按 `session.status` 路由 — `planning|awaiting_auth` → 触发/续跑 00 图；`dispatched`（S2）→ 仅 synthesize 占位回复并提示待 S3
- [ ] **`gate_sync`**：`approve` → patch `HG-SESSION-PLAN` approved · `transition_status` → `dispatched` · `gate.approved` event
- [ ] **`revise`**：status → `planning` · gate 保持 pending · 回到 plan
- [ ] **`cancel`**：status → `planning` · 不 dispatch
- [ ] **依赖**：引入/确认 `langgraph`（及 checkpointer 适配）· import 边界仍遵守 `harness_runtime` §11
- [ ] **pytest**：`tests/harness_runtime/test_session_orchestrator_s2.py` — interrupt/resume · auth 双写 · gate 与 meta 一致 · 崩溃恢复以文件为准
- [ ] **回归**：`test_sessions_s1.py` · `test_orchestrator_p1.py`（单轮 legacy）

---

## 非范围

- `node_dispatch` · `node_subagent_*` · `node_review`（**S3**）
- **POST** `.../promote`（**S4**）
- probe `verify --ci` 阻塞（**S4**）
- Ink 授权按钮 UI（配对 **前端 task**）
- NL `auth_confirm` 无二次确认（**前端 S2** 辅路径）
- P3-2 DB auth 迁移

---

## 依赖与引用

| 依赖项 | 路径 |
| --- | --- |
| S0/S1 | `api/harness_runtime/` · `api/ops/sessions.py` |
| gate_sync | `api/harness_runtime/gate_sync/human_gate.py` |
| SPEC §6–§7 | 授权 UX · 图拓扑 · SessionState |
| SPEC §13 | auth 双写失败路径 |
| 鉴权 | `require_ops_secret` · M0 |

---

## 技术方案（摘要）

### 状态机（§4.3 · S2 触及）

```text
planning → awaiting_auth → dispatched
     ↑           │ revise/cancel
     └───────────┘
```

- 首条 message 或 plan 完成：`planning` → `awaiting_auth`
- `approve`：`awaiting_auth` → `dispatched` + `HG-SESSION-PLAN` approved

### auth 原子序（§6.2 · §7.3）

```text
POST .../auth (approve)
  → 校验 status == awaiting_auth（已 approved 则幂等 200）
  → patch task human_gate HG-SESSION-PLAN
  → save_meta status=dispatched
  → checkpoint commit
  → append gate.approved + session.status_changed
  → 可选 probe task validate（非阻塞）
  → resume graph → node_00_synthesize → END
```

### messages 路由（D1）

```text
POST .../messages
  → load_meta · create_run(session_id=...)
  → if status in (planning, awaiting_auth):
       invoke session_orchestrator_v1 until interrupt or END
  → elif status == dispatched:
       S2: synthesize 占位（「已授权 · 派工能力 S3」）· 不调用 deep/fast
  → else: 按 §13 返回 409/合理错误
```

---

## 行为变更（Delta）

### ADDED

- **Requirement**：结构化 session 授权 API。  
  - **Scenario**：`s2-auth-approve` — GIVEN `awaiting_auth` WHEN POST auth `approve` THEN gate `HG-SESSION-PLAN` approved · status `dispatched`.
- **Requirement**：LangGraph interrupt/resume。  
  - **Scenario**：`s2-interrupt-resume` — GIVEN 图在 auth_gate interrupt WHEN auth THEN synthesize 完成 · run events 含 `gate.approved`.

### MODIFIED

- **Requirement**：session messages 编排路径。  
  - **Scenario**：`s2-messages-00-graph` — GIVEN `planning` WHEN POST messages THEN **不**调用 `chat_service` classify/deep · 走 00 plan 图。  
  - **Previously（S1）**：messages → `chat_service` · P1 orchestrator。

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 测试 |
| --- | --- | --- | --- | --- | --- |
| F1 | `fp-auth-wrong-status` | 非 `awaiting_auth` 点 approve | 409 · `SESSION_STATUS_INVALID` | 否 | test_session_orchestrator_s2 |
| F2 | `fp-auth-gate-already-approved` | 已 approved 再 approve | 200 幂等 | — | test_session_orchestrator_s2 |
| F3 | `fp-dual-write-file-fail` | task 写失败 | **阻塞** dispatch · 409/500 | 是 | test_session_orchestrator_s2 |
| F4 | `fp-dual-write-db-fail` | events 失败 · 文件成功 | `partial` · reconcile 提示 | 是 | integration |
| F5 | `fp-legacy-chat-ok` | 无 session 单轮 | `/ops/chat/messages` 仍 200 | — | test_orchestrator_p1 |

---

## 实施清单

- [ ] 0.1 确认/添加 `langgraph` 依赖与 checkpointer 适配（spike）
- [ ] 0.2 **DB migration** · `supabase/sql/ops_desk_s2_session_00_route.sql`（`ops_runs.route` 加 `session_00`）
- [ ] 1.1 `SessionState` pydantic · `graph/session_orchestrator_v1.py`
- [ ] 1.2 节点 `n00_plan` · `n00_present` · `n00_auth_gate` · `n00_synthesize`
- [ ] 1.3 `sessions.py`：`POST .../auth` · messages 路由改造
- [ ] 1.4 `gate_sync` 接 auth · `transition_status`
- [ ] 2.1 `test_session_orchestrator_s2.py`
- [ ] 2.2 回归 S1 + legacy chat

---

## 验收标准

- [ ] `session_orchestrator_v1` 可 plan → interrupt → auth resume → synthesize
- [ ] `HG-SESSION-PLAN` 与 `session.meta.yaml` 双写一致
- [ ] `POST .../auth` 三 action 行为符合 §6.3 · B3（API 侧）
- [ ] messages 在 planning/awaiting_auth **不走** chat_service deep/fast
- [ ] 单轮 `/ops/chat/messages` 不退化
- [ ] `pytest` + `ruff` 绿

**合并前必绿**：`pytest tests/harness_runtime tests/ops_desk/test_sessions_s1.py tests/ops_desk/test_orchestrator_p1.py -q` · `ruff check api/harness_runtime api/ops/sessions.py`

---

## 给 Cursor

`ops-session-s2-langgraph-00-api` · Open `ai-ink-brain-api-python/` · **HG-AUDIT-R1 pending 拒开工** · SPEC §6–§7 · **非 S3 subagent**
