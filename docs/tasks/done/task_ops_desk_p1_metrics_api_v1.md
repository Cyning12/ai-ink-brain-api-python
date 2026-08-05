# Task · Ops Desk P1-1 · Metrics & List API

> **状态**：`active`  
> **SPEC**：[`SPEC_ops_desk_kimi_code_mvp_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_desk_kimi_code_mvp_v1_zh.md) · §6.2 · §8 · §13 P1-1  
> **invoke**：[`ROUND_07_R6_demo_cache_chat.md`](../../../../docs/harness/invokes/by-task/ops-desk-kimi-code-spec-refine/rounds/ROUND_07_R6_demo_cache_chat.md) · §3.3  
> **依赖**：[`task_ops_desk_p0_github_sync_v1.md`](../done/task_ops_desk_p0_github_sync_v1.md) · P0 sync 数据已入库  
> **后继**：P1-2 ops-run-schema · P1-3 orchestrator fast path

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p1-metrics-api` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P1-METRICS-API` |
| **git_branch** | `task/ops-desk-p1-backend-chain` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **链序** | P1-1 / 3 · **须先于 P1-2、P1-3** |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

---

## 背景与目标

将 P0 前端直读 Supabase 的指标/列表查询 **下沉到 Python API**，供 Orchestrator fast path 与后续 BFF 复用。

### 完成态

- [ ] `api/ops/` 路由模块挂载至 `api/index.py`
- [ ] `GET /ops/metrics/cycle-time?days=30`
- [ ] `GET /ops/metrics/review-time?days=30`
- [ ] `GET /ops/metrics/issue-throughput?days=30`
- [ ] `GET /ops/issues`（`state` · `label` · `module`/`scan_tags` · `age` · 分页）
- [ ] `GET /ops/pulls`（`state` · `ci` · `author` · 分页）
- [ ] 默认 `repo` = `MoonshotAI/kimi-code`（`ops_repos` 种子行）
- [ ] `tests/ops_desk/test_metrics_api_p1.py`（mock Supabase · required）

---

## 范围

- 只读查询 `ops_issues` / `ops_pull_requests` / `ops_sync_runs`
- JSON 响应与 SPEC §6.2 三指标口径一致（与 P0-4 总览页语义对齐）
- 服务层可复用：`api/ops/queries/` 或 `api/ops/metrics.py`

## 非范围

- `ops_runs` / Chat（P1-2/3）
- `ops_demo_answers`（P1-6）
- 前端 BFF（P1-5）
- NL→SQL

---

## 验收标准

- [x] 三 metrics 端点返回 `{ series[], summary, as_of, sync_status }` 或等价结构
- [x] issues/pulls 分页 `limit`/`offset` 或 cursor · 默认 `days=30` 过滤
- [x] 空库 / 无 repo 种子 → 404 或结构化空结果（task 内写死一种）
- [x] `pytest tests/ops_desk/test_metrics_api_p1.py` 绿
- [x] 全量 pytest 绿

---

## 40 自检表

| 项 | 状态 | 证据 |
| --- | --- | --- |
| pytest tests/ops_desk/test_metrics_api_p1.py -v | ✅ pass | 7 passed |
| ruff check api/ops tests/ops_desk | ✅ pass | All checks passed |
| commit | ✅ | `feat(ops-desk): P1-1 metrics and list API` |

## 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | Supabase 连接失败 | HTTP 500 · `{ code: "DATABASE_DISCONNECT" }` |
| F2 | 非法 query 参数 | HTTP 422 |
| F3 | repo 不存在 | HTTP 404 |

---

## 图谱

- 实现后更新 [`16_flow_ops_chat.graph.yaml`](../../_tech_graph/16_flow_ops_chat.graph.yaml) 锚点 · `METRICS` 节点（P1-3 统一回填）
- compile + `graph.json` export · `--check` 绿（P1-3 统一跑）

---

## 给 Cursor

`ops-desk-p1-metrics-api` · P1-1 · 串行链首棒 · Open `ai-ink-brain-api-python/`。
