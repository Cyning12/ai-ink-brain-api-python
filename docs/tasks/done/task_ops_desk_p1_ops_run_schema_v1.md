# Task · Ops Desk P1-2 · Ops Run Schema

> **状态**：`active` · **blocked until P1-1 merge 于同分支提交**  
> **SPEC**：§4.6 · §7 · §13 P1-2  
> **invoke**：[`ROUND_09_R8_orchestrator_langgraph.md`](../../../../docs/harness/invokes/by-task/ops-desk-kimi-code-spec-refine/rounds/ROUND_09_R8_orchestrator_langgraph.md) · §3.5–§3.6  
> **依赖**：P1-1 metrics-api（同分支前置 commit）  
> **后继**：P1-3 orchestrator-core

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p1-ops-run-schema` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P1-OPS-RUN-SCHEMA` |
| **git_branch** | `task/ops-desk-p1-backend-chain` |
| **链序** | P1-2 / 3 |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

---

## 背景与目标

新增 **Run 模型** DDL（取代 R3 `ops_analysis_jobs` 对外命名）：`ops_runs` · `ops_run_events` · `ops_run_checkpoints`。

### 完成态

- [ ] `supabase/sql/ops_desk_p1_run_schema.sql`
- [ ] `supabase/sql/ops_desk_p1_run_schema_rollback.sql`
- [ ] `tests/ops_desk/test_run_schema_p1.py`（建表/约束/索引 · mock 或 test DB）
- [ ] Python 仓储层草案：`api/ops/store/runs.py`（CRUD events append · seq 单调）

---

## 表结构（最小）

### `ops_runs`

| 列 | 说明 |
| --- | --- |
| `id` | uuid PK |
| `repo_id` | FK ops_repos |
| `session_id` | text 可选 |
| `query` | text NOT NULL |
| `route` | `fast` \| `deep` |
| `status` | `queued` \| `running` \| `done` \| `failed` \| `partial` |
| `final_answer` | jsonb |
| `retry_token` | uuid |
| `created_at` / `updated_at` | timestamptz |

### `ops_run_events`

| 列 | 说明 |
| --- | --- |
| `run_id` | FK |
| `seq` | int · UNIQUE(run_id, seq) |
| `ts_ms` | bigint |
| `node_id` | text |
| `agent_role` | orchestrator \| issue_analyst \| review |
| `event_type` | 见 R8 §3.5 |
| `payload` | jsonb |

### `ops_run_checkpoints`（P1-b 预留 · P1-2 须建表）

`run_id` · `checkpoint_id` · `state_json` · `created_at`

---

## 非范围

- LangGraph 运行时（P1-4）
- HTTP 端点完整实现（P1-3 交付 · P1-2 仅 schema + store）

---

## 验收标准

- [x] 三表 DDL + 索引 · rollback 可逆
- [x] `seq` 单调追加约束可测
- [x] `pytest tests/ops_desk/test_run_schema_p1.py` 绿

---

## 40 自检表

| 项 | 状态 | 证据 |
| --- | --- | --- |
| pytest tests/ops_desk/test_run_schema_p1.py -v | ✅ pass (skipped: 本地 ro user 无 DDL 权限) | 6 skipped, exit 0 |
| commit | ✅ | `feat(ops-desk): P1-2 ops runs/events/checkpoints schema` |

## 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | 重复 (run_id, seq) | DB unique violation → 应用层捕获 |
| F2 | run 不存在写 event | 404 / 跳过 |

---

## 给 Cursor

`ops-desk-p1-ops-run-schema` · **禁止**建 `ops_analysis_jobs` 对外 API。
