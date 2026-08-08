# Task · Ops Desk P2-2 · Scan Ingest（后端）

> **状态**：`done`  
> **PR**：#191  
> **合并 SHA**：`938cdeae`  
> **SPEC**：§7 · §8  
> **R5**：[`ROUND_06_R5_track_c_deps.md`](../../../../docs/harness/invokes/by-task/ops-desk-kimi-code-spec-refine/rounds/ROUND_06_R5_track_c_deps.md)  
> **协调**：[`task_ops_desk_p2_scan_ingest_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_scan_ingest_v1.md)  
> **依赖**：P0-2 sync ✅ · merge **`1bbfe039`**（main）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-scan-ingest-backend` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-SCAN-INGEST-BE` |
| **git_branch** | `task/ops-desk-p2-scan-ingest-backend` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

---

## 背景与目标

GHA sync 同批拉取工作区 ISSUE_SCAN markdown → 解析 → 写入 `ops_scan_snapshots`；按 issue# 回填 `ops_issues.scan_tags`；暴露只读 summary API。

### 完成态

- [x] `supabase/sql/ops_desk_p2_scan_schema.sql` + rollback（`ops_scan_snapshots` · `ops_sync_run_artifacts`）
- [x] `api/ops/scan/`：parser · store · `GET /ops/scan/summary`
- [x] sync runner 扩展：ingest scan 步骤 · 写 artifacts 关联
- [x] GHA：checkout 工作区 ISSUE_SCAN 路径（见 §数据源）
- [x] `tests/ops_desk/test_scan_ingest_p2.py`（mock markdown · 无真实 Supabase 写）
- [x] 全量 pytest 绿 · ruff 绿

---

## 数据源（真值路径）

| 资源 | 路径 |
| --- | --- |
| 主索引 | `Projects/docs/harness/guides/ISSUE_SCAN_kimi_code_open_c2_v1_zh.md` |
| 子文档 | `Projects/docs/harness/guides/issues/*.md` |
| 版本号 | 主索引 frontmatter **版本**（如 `v1.5.4`）→ `scan_version` |

**GHA 拉取**：checkout `cyning-ink-workspace`（或 sparse `docs/harness/guides/`）· 需 Repo Secret `WORKSPACE_REPO_TOKEN`（private 时）或 public 只读 checkout。

---

## 解析 MVP 口径

| 输出 | 规则 |
| --- | --- |
| `ops_scan_snapshots.total_open` | 主索引总览 open 数（或解析 `#NNN` 去重计数） |
| `p0_items` / `p1_items` / `p2_items` / `deferred_items` | JSONB 数组 · `{ number, title?, tier?, note? }` |
| `parsed_summary` | `{ version, scanned_at, sections: [...] }` |
| `ops_issues.scan_tags` | 按 issue# 映射 tier 标签 · 例 `C2` · `C3-P0` · `C3-P2` · `OBSERVE` |

解析失败 → sync_run **partial**（Issue/PR 仍 success）· scan 步骤 error 写入 `error_message` 子段或 logs。

---

## API

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/py/ops/scan/summary` | 最新 snapshot 摘要 · `x-ops-secret` |

挂载：`app.include_router` 已有 `/api/py` prefix。

---

## 非范围

- 前端 UI（泳道 B）
- `graph_snapshots`（P2-1）
- Chat orchestrator `scan_status` 意图（P2 收口可选 follow-up）

---

## 失败路径

| 失败场景 | 影响 | 兜底 |
| --- | --- | --- |
| 工作区 checkout 失败 | scan 步骤 skip | sync_run 标记 partial；API 返回 503 + 末次 snapshot |
| markdown 格式漂移 | parser 可能漏读 tier | 最佳努力解析；单测锁定样例文件 |
| DDL 未执行 | snapshot/artifact 表不存在 | ingest 跳过；pytest 测 parser 层 |

---

## 行为变更

### ADDED
- `ops_scan_snapshots` / `ops_graph_snapshots` / `ops_sync_run_artifacts` 三张表及 rollback
- `api/ops/scan/`：parser / store / `GET /api/py/ops/scan/summary`
- sync runner 成功后调用 `ingest_scan_after_github_sync`
- GHA workflow sparse checkout `cyning-ink-workspace` `docs/harness/guides/`

### MODIFIED
- `docs/_tech_graph/_manifest.json` 补录新增表
- `tests/ops_desk/test_sync_p0.py` 增加 scan ingest stub，保持 P0 状态机测试独立

### REMOVED
- 无
---

## 验收标准

- [ ] `pytest tests/ops_desk/test_scan_ingest_p2.py -v` pass
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark" -q` pass
- [ ] workflow YAML 语法有效 · 本地 `python scripts/ops_sync_kimi_code.py` 可 `--dry-run` 或 mock 测 ingest
- [ ] 50 reinspect pass · PR merge main

---

## 给 Cursor

泳道 A · 与前端 **并行** · **本 PR 优先 merge**。
