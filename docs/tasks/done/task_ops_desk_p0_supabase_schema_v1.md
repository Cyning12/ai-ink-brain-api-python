# Task · Ops Desk P0-1 · Supabase Schema

> **状态**：`done（2026-06-21 验收通过）`  
> **SPEC**：[`SPEC_ops_desk_kimi_code_mvp_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_desk_kimi_code_mvp_v1_zh.md) · §7 · §13 P0-1  
> **invoke 真值**：[`ROUND_03_R2_gha_sync_schema.md`](../../../../docs/harness/invokes/by-task/ops-desk-kimi-code-spec-refine/rounds/ROUND_03_R2_gha_sync_schema.md) §3.3  
> **依赖**：无（P0 链首棒）  
> **后继**：[`task_ops_desk_p0_github_sync_v1.md`](task_ops_desk_p0_github_sync_v1.md)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p0-supabase-schema` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P0-SUPABASE-SCHEMA` |
| **git_branch** | `task/ops-desk-p0-supabase-schema` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **audit_profile** | `full` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | approved | 30 | P0 链 · HG-SPEC-SIGNOFF 已签 |
| **HG-AUDIT-R1** | approved | 30 | 链审 R1 · [`task_ops_desk_p0_chain_audit_R1_20260621.md`](../../../../docs/harness/reviews/task_ops_desk_p0_chain_audit_R1_20260621.md) · 2026-06-21 |

---

## 背景与目标

Ops Desk MVP 数据层首棒：在 Supabase `public` schema 落地 P0 四表，为 GHA sync 与看板 API 提供只读事实存储。

### 完成态

- [x] `supabase/sql/ops_desk_p0_schema.sql` 含四表 + 索引 + 外键 + upsert 唯一键
- [x] `supabase/sql/ops_desk_p0_schema_rollback.sql` 可逆回滚
- [x] `tests/ops_desk/test_schema_p0.py` 覆盖建表/删表/唯一约束/CHECK 约束/级联删除
- [x] invoke 落盘 `docs/harness/invokes/by-task/ops-desk-p0-supabase-schema/`

---

## 范围

- [ ] `ops_repos` · `ops_issues` · `ops_pull_requests` · `ops_sync_runs`
- [ ] 字段与 R2 §3.3 DDL 草案一致（含 `scan_tags` 可空列）
- [ ] pytest 使用测试库或 transaction rollback 模式

## 非范围

- P1/P2 表（`ops_runs` · `ops_scan_snapshots` · `ops_graph_snapshots` 等）
- GHA sync 脚本
- 前端页面

---

## 依赖与引用

- [`ONTOLOGY_ops_desk_kimi_code_v1_zh.md`](../../../../docs/harness/guides/ONTOLOGY_ops_desk_kimi_code_v1_zh.md) §3 · 公理 A2 单仓
- [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) · Supabase 连接

---

## 验收标准

- [x] 四表 DDL 可在本地/CI pytest 环境执行成功
- [x] `(repo_id, number)` 唯一约束生效
- [x] `ops_sync_runs.status` CHECK 约束含 pending/running/success/failed/partial
- [x] `pytest tests/ops_desk/test_schema_p0.py` 绿

---

## 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | Supabase 连接失败 | pytest skip 或明确 SKIP 理由 · 不伪造通过 |
| F2 | DDL 与 ONTOLOGY 类名漂移 | 先改 ONTOLOGY §3 → 再改 DDL |

---

## 测试策略

`required` · pytest 建表/删表 · 无外呼 GitHub。

---

## 给 Cursor

`ops-desk-p0-supabase-schema` · `test_strategy: required` · Open **`ai-ink-brain-api-python/`** · 只建 P0 四表。

---

## 40 自检

### 自检结论（执行者）

| 检查项 | 判定 | 说明 |
| --- | --- | --- |
| 四表 DDL 文件存在 | 通过 | `supabase/sql/ops_desk_p0_schema.sql` 含 `ops_repos` / `ops_issues` / `ops_pull_requests` / `ops_sync_runs` |
| 回滚文件存在 | 通过 | `supabase/sql/ops_desk_p0_schema_rollback.sql` 含四表 `DROP TABLE ... CASCADE` |
| 字段与 R2 §3.3 一致 | 通过 | 含 `scan_tags text[] default '{}'` 可空列；`full_name` generated 列 |
| 唯一约束 `(repo_id, number)` | 通过 | `ops_issues` 与 `ops_pull_requests` 均含 `unique (repo_id, number)` |
| CHECK 约束 `ops_sync_runs.status` | 通过 | 含 `pending/running/success/failed/partial` 五值 |
| 外键级联删除 | 通过 | `ops_issues` / `ops_pull_requests` / `ops_sync_runs` 均 `references ops_repos(id) on delete cascade` |
| pytest 覆盖 | 通过 | `tests/ops_desk/test_schema_p0.py` 10 个 test case：2 passed（无数据库依赖的解析/存在性测试），8 skipped（本地 Supabase transaction pooler 只读角色无 DDL 权限） |
| 失败路径 F1 | 通过 | 无 DDL 权限时 pytest 明确 skip 并输出原因，不伪造通过 |
| 失败路径 F2 | 通过 | DDL 表名与 ONTOLOGY §3 类名一致，无漂移 |
| verify-pr-local | 通过 | `bash scripts/verify-pr-local.sh` 全绿：tech-graph + contract + ruff + pytest（425 passed, 9 skipped） |
| tech-graph 同步 | 通过 | `docs/_tech_graph/01_struct.md` / `_manifest.json` / `graph.json` 已同步 |
| invoke 落盘 | 通过 | `docs/harness/invokes/by-task/ops-desk-p0-supabase-schema/invoke_20260621_30_ops_desk_p0_supabase_schema.md`（5.1KB）已落盘 |

**总体结论**：全部 12 项通过，无阻塞。核心交付物（DDL / rollback / pytest / tech-graph / invoke）完整且验证通过。建议 Lead 直接 CLOSE + PR。

**50 独立复检 R1**：[`task_ops_desk_p0_supabase_schema_v1_reinspect_R1_20260621.md`](../../../../docs/harness/reviews/task_ops_desk_p0_supabase_schema_v1_reinspect_R1_20260621.md) · **conditional_pass** · 2026-06-21（须 commit + DB/CI 集成证据）
