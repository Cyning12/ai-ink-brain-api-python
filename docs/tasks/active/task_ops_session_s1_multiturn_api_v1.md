# Task · Ops Session S1 Multiturn API（sessions REST · DB 绑定 · messages）

> **状态**：`draft`  
> **epic**：Session Orchestrator · S1 `ops-session-s1-multiturn`  
> **schedule_ref**：SPEC §12.1 S1 · MVP 首片（S0+S1+S2）  
> **关联 SPEC**：`[SPEC_ops_session_orchestrator_v1_zh.md](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md)` §9 · §12 S1 · §13  
> **前置**：`[task_ops_session_s0_schema_v1.md](../done/task_ops_session_s0_schema_v1.md)` · **done** · PR #226  
> **配对前端**：`[task_ops_session_s1_multiturn_ui_v1.md](../../../ai-ink-brain/content/tasks/active/task_ops_session_s1_multiturn_ui_v1.md)`  
> **BLOCKERS**：B2（session:run 1:N）· 本 task 落地查询与 `latest_run_id`

---



## Harness 元信息


| 字段                | 值                                   |
| ----------------- | ----------------------------------- |
| **task_slug**     | `ops-session-s1-multiturn-api`      |
| **module_id**     | `OPS-SESSION-ORCH`                  |
| **freeze_id**     | `OPS-SESSION-ORCH-SPEC-V1`          |
| **test_strategy** | `required`                          |
| **worktree_root** | `ai-ink-brain-api-python/`          |
| **git_branch**    | `task/ops-session-s1-multiturn-api` |
| **blocks**        | S2 `ops-session-s2-langgraph-00`    |
| **blocked_by**    | S0 `ops-session-s0-schema`          |




### 人工闸 `human_gate`


| human_gate_id | status     | blocks_hats       | 说明        |
| ------------- | ---------- | ----------------- | --------- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 00 起草     |
| HG-AUDIT-R1   | `approved` | 30                | 20 R1 后人签 |


---



## 背景与目标

S0 已交付 `harness_runtime` 文件 Inform 真值（`create_session` · `gate_sync`）。本 task 在 **api-python** 暴露 **Session REST**，将 `session_id` 与现有 `ops_runs` **1:N** 绑定，并支持 **多轮 messages**（沿用 P1 Chat 编排 · **不**引入 S2 LangGraph 00 图）。

**完成态一句话**：客户端可 `POST /ops/sessions` 创建 session · `GET` 列表/详情 · `POST .../messages` 多轮续聊（每轮创建 `ops_run` 且 `session_id` 非空）· `session.meta.yaml.latest_run_id` 与 `session.created` 事件落盘 · 单轮 `/ops/chat/messages` **不退化**。

---



## 范围

- [ ] `api/ops/sessions.py`（或 `api/ops/sessions/router.py`）注册到 `ops_router`
- [ ] **POST** `/ops/sessions`：`harness_runtime.create_session` · 写 `session.created` event（首 run 可选延迟到首条 message）
- [ ] **GET** `/ops/sessions`：扫描 `docs/harness/sessions/` · 读 meta · 分页/按 `status` 过滤（文件系统真值）
- [ ] **GET** `/ops/sessions/{session_id}`：meta + `gate_summary` + 最近 N 条 message 摘要（来自 session 下 runs/events 或 meta 缓存）
- [ ] **POST** `/ops/sessions/{session_id}/messages`：校验 session 存在 · 创建 `ops_run(session_id=...)` · 调用现有 `classify`/`run_deep`/`run_fast` 路径（与 `chat.py` 同逻辑 · **非** `session_orchestrator_v1` 图）· 更新 `latest_run_id` · append `session.status_changed` 等事件
- [ ] **GET** `/ops/sessions/{session_id}/events`：聚合该 session 下所有 runs 的 events（或 `OpsRunStore` 新方法）
- [ ] `OpsRunStore` **扩展**：`list_runs_by_session_id` · 可选 `list_sessions` 辅助（若走 DB 索引而非纯文件扫描）
- [ ] **B2 契约**：`ops_runs.session_id` 可空兼容 legacy；新 session 路径 **必须**写入非空 `session_id`（DDL 已在 `ops_desk_p1_run_schema.sql` · 验收索引存在）
- [ ] **pytest**：`tests/ops_desk/test_sessions_s1.py` 或 `tests/harness_runtime/test_sessions_api.py`（TestClient · mock store / tmp sessions 目录）



## 非范围

- **POST** `/ops/sessions/{id}/auth` · LangGraph interrupt（**S2**）
- **POST** `.../promote`（**S4**）
- `session_orchestrator_v1` StateGraph（**S2**）
- Ink UI / BFF（配对 **前端 task**）
- probe subprocess（**S4**）
- `HG-SESSION-PLAN` 授权按钮 UX（**S2**；S1 messages 仅透传编排）

---



## 依赖与引用


| 依赖项       | 路径                                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------------- |
| S0 交付     | `api/harness_runtime/` · `[task_ops_session_s0_schema_v1.md](../done/task_ops_session_s0_schema_v1.md)` |
| 现有 Chat   | `api/ops/chat.py` · `api/ops/orchestrator/`                                                             |
| Run Store | `api/ops/store/runs.py`                                                                                 |
| DDL       | `supabase/sql/ops_desk_p1_run_schema.sql`（`session_id` + index 已有）                                      |
| SPEC §9.2 | Session API 最小集（S1 不含 auth/promote）                                                                     |
| 鉴权        | `require_ops_secret` · M0（SPEC §9.2）                                                                    |


---



## 技术方案（摘要）



### 路由（挂载 `/ops/sessions`）


| 方法   | 路径                                    | S1 行为                                                                        |
| ---- | ------------------------------------- | ---------------------------------------------------------------------------- |
| POST | `/ops/sessions`                       | body: `{ slug, title }` → `create_session` → `{ session_id, meta }`          |
| GET  | `/ops/sessions`                       | `?status=&limit=&offset=` → 文件扫描 + meta 列表                                   |
| GET  | `/ops/sessions/{session_id}`          | meta + gates + `recent_messages` 摘要                                          |
| POST | `/ops/sessions/{session_id}/messages` | body: `{ message, model? }` → run + 编排 · 返回 `{ run_id, answer, session_id }` |
| GET  | `/ops/sessions/{session_id}/events`   | 聚合 events                                                                    |




### messages 与单轮 Chat 关系

```text
POST /ops/sessions/{id}/messages
  → load_meta(session_dir) · 404 SESSION_NOT_FOUND
  → create_run(..., session_id=id)
  → 复用 chat.py 内 classify / deep / fast 分支（提取共享函数 · 避免双份逻辑）
  → update meta.latest_run_id · updated_at
  → store.append_event(..., "session.status_changed", ...)
  → 返回与 /ops/chat/messages 兼容字段 + session_id
```



### 事件（§9.4 · S1 最小）


| event_type               | 时机                                   |
| ------------------------ | ------------------------------------ |
| `session.created`        | POST /ops/sessions                   |
| `session.status_changed` | messages 后 status 变更（如保持 `planning`） |


---



## 行为变更（Delta）



### ADDED

- **Requirement**：Session REST CRUD + multiturn messages。  
  - **Scenario**：`s1-create-and-message` — GIVEN 合法 secret WHEN POST sessions 再 POST messages THEN `ops_runs.session_id` 非空且 meta `latest_run_id` 更新。
- **Requirement**：未知 session 返回 404。  
  - **Scenario**：`s1-session-not-found` — GIVEN 无效 id WHEN GET/POST THEN `SESSION_NOT_FOUND`。



### MODIFIED

无（legacy `/ops/chat/messages` 保持 · Previously: 无 session 路由）

---



## 失败路径


| #   | Scenario ID                     | 触发条件                 | 系统行为                                  | 可重试 | 测试                      |
| --- | ------------------------------- | -------------------- | ------------------------------------- | --- | ----------------------- |
| F1  | `fp-session-not-found`          | session_id 不存在       | HTTP 404 `SESSION_NOT_FOUND`          | 否   | test_sessions_api       |
| F2  | `fp-session-schema-unsupported` | meta 损坏/版本不支持        | HTTP 409 `SESSION_SCHEMA_UNSUPPORTED` | 否   | test_sessions_api       |
| F3  | `fp-session-id-mismatch`        | 目录/meta 不一致          | HTTP 409 `SESSION_ID_MISMATCH`        | 否   | test_sessions_api       |
| F4  | `fp-legacy-chat-ok`             | 无 session_id 单轮 Chat | `/ops/chat/messages` 仍 200            | —   | 回归 test_orchestrator_p1 |


---



## 实施清单

- [ ] 1.1 提取 `chat.py` 可复用编排入口（如 `_handle_chat_message`）
- [ ] 1.2 实现 `api/ops/sessions.py` + 注册 `ops_router`
- [ ] 1.3 `OpsRunStore.list_runs_by_session_id` + events 聚合
- [ ] 1.4 写 `session.created` / `session.status_changed` events
- [ ] 2.1 `tests/.../test_sessions_s1.py`（tmp sessions_root fixture）
- [ ] 2.2 回归：现有 ops_desk chat 单测仍绿

---



## 验收标准

- [ ] POST/GET sessions 与 SPEC §9.2 S1 子集一致（无 auth/promote）
- [ ] 多轮 messages 同一 `session_id` 产生多个 `ops_run`（1:N）
- [ ] `latest_run_id` 与最近一次 run 一致
- [ ] `SESSION_NOT_FOUND` / schema 错误码与 §13 一致
- [ ] `/ops/chat/messages` 无 session_id 行为不退化
- [ ] `pytest tests/...` 新增用例全绿 · PR pytest workflow 绿
- [ ] 配对前端 task 可联调 BFF

**合并前必绿**：`pytest tests -m "not intent_eval and not intent_benchmark"` · `ruff check`（触及路径）

---



## 给 Cursor

`ops-session-s1-multiturn-api` · Open `ai-ink-brain-api-python/` · `harness_runtime` · `OPS-SESSION-ORCH-SPEC-V1` · B2 · 配对 Ink UI task · **非 S2 LangGraph**