# Task · Ops Desk P0-2 · GitHub Sync（GHA）

> **状态**：`done（2026-06-22 短链 30→40→50→CLOSE 验收通过）`  
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
| **HG-AUDIT-R1** | approved | — | 链审 R1 · 短链无中间人闸 · 维护者事后验收 |

---

## 背景与目标

实现 **MoonshotAI/kimi-code** 单仓 Issue/PR 日同步：GHA cron 24h + `workflow_dispatch`；写入 `ops_sync_runs` 状态与增量 cursor。

### 完成态

- [x] `.github/workflows/ops_sync_kimi_code.yml`
- [x] Python sync 脚本（`scripts/ops_sync_kimi_code.py` + `api/ops/sync/`）
- [x] 首次全量 · 后续 `updated_at > cursor` 增量
- [x] `ops_repos` 种子行 `MoonshotAI/kimi-code`
- [x] pytest mock GitHub API · 验证 upsert 与 sync_run 状态机

---

## 范围

- [x] GitHub REST · Issue + PR 必要字段
- [x] Rate limit 退避（403/502/504 · 最多 5 次）
- [x] 401/422 立即 failed 写入 sync_run
- [x] Secrets：`GITHUB_TOKEN` · `SUPABASE_*`

## 非范围

- ISSUE_SCAN markdown ingest（P2）
- graph.json ingest（P2）
- Webhook 实时同步

---

## 验收标准

- [x] `workflow_dispatch` 可手动触发
- [x] 成功 run 写入 `ops_sync_runs` status=success + cursor
- [x] 失败 run 写入 error_message
- [x] `pytest tests/ops_desk/test_sync_p0.py` 绿（mock）

---

## 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | GitHub 401/422 | sync_run failed · 不重试 |
| F2 | 403 rate limit | 指数退避 · 仍失败则 partial/failed |

---

## 测试策略

`required` · mock GitHub + FakeStore · 无外呼。

---

## 40 自检

### 自检结论（执行者 · 40 R1）

| 检查项 | 命令 | 退出码 | 判定 |
| --- | --- | --- | --- |
| sync 单测 | `pytest tests/ops_desk/test_sync_p0.py -v` | 0 | **pass** · 12 passed |
| 全量 pytest | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | **pass** · 442 passed · 8 skipped |
| workflow | `.github/workflows/ops_sync_kimi_code.yml` | — | **pass** · cron 24h + workflow_dispatch |
| F1 401/422 | `test_f1_*` | 0 | **pass** · fail_fast · 不重试 |
| F2 403 退避 | `test_github_client_retry_then_success` · `test_f2_partial_*` | 0 | **pass** · max 5 · partial 语义 |
| 状态机 | `test_sync_success_state_machine` | 0 | **pass** · pending→running→success |
| ruff | `ruff check api/ops scripts/ops_sync_kimi_code.py tests/ops_desk/test_sync_p0.py` | 0 | **pass** |

**commit SHA（40）**：见 CLOSE merge SHA  
**总体结论**：全部通过 · 建议合并 `task/ops-desk-p0-github-sync` → `main`

**50 独立复检 R1**：[`task_ops_desk_p0_github_sync_v1_reinspect_R1_20260621.md`](../../../../docs/harness/reviews/task_ops_desk_p0_github_sync_v1_reinspect_R1_20260621.md) · **pass** · 2026-06-22

---

## 给 Cursor

`ops-desk-p0-github-sync` · 单仓 · 24h · P0-1 schema 已 merge。
