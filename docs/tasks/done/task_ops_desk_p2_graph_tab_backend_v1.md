# Task · Ops Desk P2-1 · Graph Tab（后端）

> **状态**：`done`  
> **SPEC**：§4.5 · §7  
> **R5**：[`ROUND_06_R5_track_c_deps.md`](../../../../docs/harness/invokes/by-task/ops-desk-kimi-code-spec-refine/rounds/ROUND_06_R5_track_c_deps.md)  
> **协调**：[`task_ops_desk_p2_graph_tab_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p2_graph_tab_v1.md)  
> **依赖**：P0-2 sync ✅ · P2-2 scan schema ✅（`ops_graph_snapshots` 已建）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-graph-tab-backend` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-GRAPH-TAB-BE` |
| **git_branch** | `task/ops-desk-p2-graph-tab-backend` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |

---

## 背景与目标

GHA sync 同批拉取 **`Cyning12/kimi-code`** @ **`cyning/meta`** 的 `graph.json`（本地路径前缀 `kimi-code-meta/` · 见 [`POINTER`](../../../../docs/harness/guides/POINTER_kimi_code_meta_git_mapping_v1_zh.md)）→ 写入 `ops_graph_snapshots`；暴露 graph summary 与 **模块×Issue 矩阵** API。

### 完成态

- [ ] `api/ops/graph/`：validator · store · router
- [ ] sync runner 扩展：`ingest_graph_after_github_sync` · 写 `ops_sync_run_artifacts.graph_snapshot_id`
- [ ] GHA：checkout **`Cyning12/kimi-code`** · `cyning/meta` · 路径 `docs/_tech_graph/graph.json`（落盘 `workspace/kimi-code-meta/`）
- [ ] `GET /api/py/ops/graph/summary` · `GET /api/py/ops/graph/module-issues`
- [ ] `tests/ops_desk/test_graph_ingest_p2.py`（fixture graph.json · mock Supabase）
- [ ] 全量 pytest 绿 · ruff 绿 · `_manifest.json` 端点同步

---

## 数据源（真值路径）

| 资源 | 路径 |
| --- | --- |
| graph.json | 本地 `kimi-code-meta/docs/_tech_graph/graph.json` · GHA：**`Cyning12/kimi-code`** @ `cyning/meta` |
| manifest | `kimi-code-meta/.cyning-harness/manifest.json` → `manifest_version` |
| 映射真值 | [`POINTER_kimi_code_meta_git_mapping_v1_zh.md`](../../../../docs/harness/guides/POINTER_kimi_code_meta_git_mapping_v1_zh.md) |
| 开发降级 | `tests/fixtures/graph_snapshot_sample_v1.json`（真实结构子集） |

**GHA 拉取**：checkout repository **`Cyning12/kimi-code`** · ref **`cyning/meta`** · Secret **`KIMI_META_REPO_TOKEN`**（PAT 授权该 fork · 与 P2-2 `WORKSPACE_REPO_TOKEN` 模式对称）。

---

## Ingest MVP 口径

| 字段 | 规则 |
| --- | --- |
| `ops_graph_snapshots.source_branch` | 如 `cyning/meta` |
| `source_commit` | checkout SHA |
| `manifest_version` | manifest.json 版本字段 |
| `payload` | 完整 graph.json JSONB |
| artifacts | 与 scan 同批写入 `ops_sync_run_artifacts` |

graph ingest 失败 → sync_run **partial**（Issue/PR/scan 仍保留）· 与 P2-2 scan 语义一致。

---

## 模块×Issue 矩阵 API

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/py/ops/graph/summary` | 最新 snapshot 元数据 · `x-ops-secret` |
| GET | `/api/py/ops/graph/module-issues` | 模块×Issue 矩阵 · query: `state=open` |

**MVP 映射规则**（实现备忘）：

1. 从 `payload.nodes[]` 提取 `id` · `label` · `graph_id`
2. open issues 与 module 关联：优先 `labels` 含 `module:<node_id>` 或 title/body 关键词；无映射时 `open_issue_count=0`
3. 返回 `{ modules: [{ module_id, label, graph_id, open_issue_count, sample_issues[] }] }`

---

## 非范围

- 前端 Graph Tab / Issues 清空筛选（泳道 B）
- 新 DDL（表已在 P2-2 创建）
- Chat orchestrator `graph_module` 意图（P2 收口）

---

## 失败路径

| 失败场景 | 影响 | 兜底 |
| --- | --- | --- |
| `Cyning12/kimi-code` checkout 失败或缺 `KIMI_META_REPO_TOKEN` | graph 步骤 skip | sync_run **partial** · Issue/PR/scan 仍保留 |
| graph.json 校验失败 | 无新 snapshot | 记录 error · partial · 保留末次 snapshot |
| 无 snapshot | API 404 | `GRAPH_SNAPSHOT_NOT_FOUND` |

---

## 行为变更

### ADDED
- GHA checkout **`Cyning12/kimi-code`** @ `cyning/meta`（落盘 `workspace/kimi-code-meta/`）
- `api/ops/graph/` · ingest · summary/module-issues API

### MODIFIED
- `docs/tasks/done/task_ops_desk_p2_graph_tab_backend_v1.md` · POINTER 远程映射说明

### REMOVED
- 无

---

## 验收标准

- [ ] `pytest tests/ops_desk/test_graph_ingest_p2.py -v` pass
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark" -q` pass
- [ ] 50 reinspect pass · PR merge main

---

## 给 Cursor

泳道 A · 与前端 **并行** · **本 PR 优先 merge** · 参照 `api/ops/scan/` 目录结构。
