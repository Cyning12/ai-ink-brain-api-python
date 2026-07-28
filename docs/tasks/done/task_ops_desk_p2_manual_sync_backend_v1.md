# Task · Ops Desk P2-3 · Manual Sync（后端）

> **状态**：`pending`  
> **SCOPE**：[`SCOPE_NOTE_manual_sync_v1_zh.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-manual-sync/SCOPE_NOTE_manual_sync_v1_zh.md)  
> **协调**：[`task_ops_desk_p2_manual_sync_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_manual_sync_v1.md)  
> **依赖**：P0-2 sync ✅ · P2-2 `ops_sync_run_artifacts` ✅

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-manual-sync-backend` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-MANUAL-SYNC-BE` |
| **git_branch** | `task/ops-desk-p2-manual-sync-backend` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

---

## 背景与目标

暴露 **手动触发 GHA sync** 与 **最近 sync run 列表** API；复用现有 `ops_sync_runs` / `ops_sync_run_artifacts`，**无新 DDL**。

### 完成态

- [ ] `api/ops/sync/` 扩展：`dispatch.py` · `router.py`
- [ ] `POST /api/py/ops/sync/trigger` · `x-ops-secret`
- [ ] `GET /api/py/ops/sync/runs?limit=20`
- [ ] Env：`OPS_GITHUB_DISPATCH_TOKEN`（PAT · `actions:write` on `Cyning12/ai-ink-brain-api-python`）
- [ ] `tests/ops_desk/test_manual_sync_p2.py`（mock httpx GitHub · mock Supabase）
- [ ] `docs/_tech_graph/_manifest.json` 补端点（若 verify 要求）
- [ ] pytest + ruff 绿

---

## API 契约

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/py/ops/sync/trigger` | 调 GitHub `workflow_dispatch` · workflow `ops-sync-kimi-code` · ref `main` |
| GET | `/api/py/ops/sync/runs` | query `limit` 默认 20 · 含 artifact 布尔字段 |

**POST 响应**：

- 200 `{ dispatched: true, workflow, repository }`
- 409 `SYNC_ALREADY_RUNNING`（最近 run `pending|running`）
- 503 token 未配置 · 502 GitHub 失败

**GET runs[] 字段**：`id` · `started_at` · `finished_at` · `status` · `trigger` · `records_issue` · `records_pr` · `error_message` · `has_graph_snapshot` · `has_scan_snapshot`

---

## GitHub dispatch 真值

| 项 | 值 |
| --- | --- |
| repository | `Cyning12/ai-ink-brain-api-python` |
| workflow file | `ops_sync_kimi_code.yml` |
| event | `workflow_dispatch` |
| ref | `main` |

GHA 已设 `OPS_SYNC_TRIGGER=manual` when dispatch（见 workflow env）。

---

## 非范围

- 前端按钮 / BFF（泳道 B）
- 修改 sync runner ingest 逻辑
- 新表 / migration

---

## 失败路径

| 失败场景 | HTTP | 兜底 |
| --- | --- | --- |
| 无 `OPS_GITHUB_DISPATCH_TOKEN` | 503 | 明确 error code `DISPATCH_TOKEN_MISSING` |
| 已有 running sync | 409 | 不重复 dispatch |
| GitHub 403/422 | 502 | 记录 message · 不写 sync_run |
| Supabase 读 runs the runs list | 500 | 结构化错误 |

---

## 行为变更

### ADDED
- `POST /api/py/ops/sync/trigger`
- `GET /api/py/ops/sync/runs`

### MODIFIED
- `api/ops/sync/` 模块组织（若需从 runner 拆 router）

### REMOVED
- 无

---

## 验收标准

- [ ] `pytest tests/ops_desk/test_manual_sync_p2.py -v` pass
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark" -q` pass
- [ ] 50 reinspect pass · **本 PR 优先 merge**

---

## 给 Cursor

泳道 A · 参照 `api/ops/graph/router.py` · `api/ops/scan/router.py` 鉴权模式。
