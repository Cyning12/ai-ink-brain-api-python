# Task · Ops Desk P0-2 · GitHub Sync（GHA）

> **状态**：`pending`  
> **SPEC**：[`SPEC_ops_desk_kimi_code_mvp_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_desk_kimi_code_mvp_v1_zh.md) · §4.2 · §13 P0-2  
> **invoke 真值**：[`ROUND_03_R2_gha_sync_schema.md`](../../../../docs/harness/invokes/by-task/ops-desk-kimi-code-spec-refine/rounds/ROUND_03_R2_gha_sync_schema.md)  
> **依赖**：[`task_ops_desk_p0_supabase_schema_v1.md`](task_ops_desk_p0_supabase_schema_v1.md)  
> **后继**：前端 P0-4～P0-6 · P1 metrics API

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p0-github-sync` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P0-GITHUB-SYNC` |
| **git_branch** | `task/ops-desk-p0-github-sync` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **audit_profile** | `full` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | approved | 30 | 依赖 P0-1 schema |

---

## 背景与目标

实现 **MoonshotAI/kimi-code** 单仓 Issue/PR 日同步：GHA cron 24h + `workflow_dispatch`；写入 `ops_sync_runs` 状态与增量 cursor。

### 完成态

- [ ] `.github/workflows/ops_sync_kimi_code.yml`
- [ ] Python sync 脚本（`scripts/ops_sync_kimi_code.py` 或 `api/ops/sync/`）
- [ ] 首次全量 · 后续 `updated_at > cursor` 增量
- [ ] `ops_repos` 种子行 `MoonshotAI/kimi-code`
- [ ] pytest mock GitHub API · 验证 upsert 与 sync_run 状态机

---

## 范围

- [ ] GitHub REST · Issue + PR 必要字段
- [ ] Rate limit 退避（403/502/504 · 最多 5 次）
- [ ] 401/422 立即 failed 写入 sync_run
- [ ] Secrets：`GITHUB_TOKEN` · `SUPABASE_*`

## 非范围

- ISSUE_SCAN markdown ingest（P2）
- graph.json ingest（P2）
- Webhook 实时同步

---

## 验收标准

- [ ] `workflow_dispatch` 可手动触发
- [ ] 成功 run 写入 `ops_sync_runs` status=success + cursor
- [ ] 失败 run 写入 error_message
- [ ] `pytest tests/ops_desk/test_sync_p0.py` 绿（mock）

---

## 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | GitHub 401/422 | sync_run failed · 不重试 |
| F2 | 403 rate limit | 指数退避 · 仍失败则 partial/failed |

---

## 给 Cursor

`ops-desk-p0-github-sync` · 单仓 · 24h · 与 P0-1 schema 同 PR 或紧随 PR。
