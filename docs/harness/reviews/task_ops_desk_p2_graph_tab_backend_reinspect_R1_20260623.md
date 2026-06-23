# Reinspect · Ops Desk P2-1 Graph Tab Backend

| 项 | 值 |
| --- | --- |
| **任务** | `ops-desk-p2-graph-tab-backend` |
| **Agent** | Claude Opus 4.7 (泳道 A) |
| **日期** | 2026-06-23 |
| **分支** | `task/ops-desk-p2-graph-tab-backend` |
| ** verdict** | **pass** |

---

## 1. 独立重跑 §40

### 1.1 Graph 专项测试
```bash
pytest tests/ops_desk/test_graph_ingest_p2.py -v
# 结果: 28 passed, 3 warnings
```

### 1.2 关联测试（sync + scan + graph）
```bash
pytest tests/ops_desk/test_sync_p0.py tests/ops_desk/test_scan_ingest_p2.py tests/ops_desk/test_graph_ingest_p2.py -v
# 结果: 57 passed, 3 warnings
```

### 1.3 Ruff 检查
```bash
ruff check api/ops tests/ops_desk
# 结果: All checks passed!
```

### 1.4 全量测试（排除 intent_eval / intent_benchmark）
```bash
pytest tests -m "not intent_eval and not intent_benchmark" -q
# 结果: 504 passed, 10 skipped, 2 deselected, 131 warnings
# 17 failed（均为 pre-existing：demo_cache / metrics / orchestrator 403，与 P2-1 无关）
```

---

## 2. 走查

### 2.1 graph.json 校验

- **validator.py** 覆盖：`schema_version` · `freeze_id` · `nodes[]`（id/label/graph_id）· `edges[]`（from/to/type/graph_id）· `graphs[]`（id/title）
- **错误路径**：非 dict root · 缺失 key · 类型错误 → 均返回结构化 `GraphValidationError`
- **fixture** `tests/fixtures/graph_snapshot_sample_v1.json`：基于真实 graph.json 结构的匿名子集，通过 validator 校验

### 2.2 Partial sync 语义

- **runner.py** 扩展：scan ingest 后追加 graph ingest
- **合并逻辑**：scan_status + graph_status 任一 partial → 整体 partial，error_message 合并
- **失败隔离**：graph ingest 失败不影响已写入的 Issue/PR/scan 数据
- **GHA 兼容**：cron 仍返回 exit 0（success/partial 均不阻断）

### 2.3 API 鉴权 x-ops-secret

- **GET /api/py/ops/graph/summary**：`require_ops_secret` 依赖注入
- **GET /api/py/ops/graph/module-issues**：同上
- **测试覆盖**：
  - 200 OK（正确 secret）
  - 401 Unauthorized（缺失 secret）
  - 404 GRAPH_SNAPSHOT_NOT_FOUND（无 snapshot）

### 2.4 GHA 扩展

- **新增 checkout 步骤**：`kimi-code-meta` @ `cyning/meta` 分支
- **sparse-checkout**：`docs/_tech_graph/graph.json` + `.cyning-harness/manifest.json`
- **环境变量**：`OPS_GRAPH_JSON_PATH` · `OPS_MANIFEST_JSON_PATH` · `OPS_GRAPH_SOURCE_BRANCH`
- **Secret 名**：`KIMI_META_REPO_TOKEN`（与 P2-2 `WORKSPACE_REPO_TOKEN` 模式对称）
- **降级**：token 缺失时 graph ingest skipped，不阻断 workflow

### 2.5 数据层

- **ops_graph_snapshots**：source_branch · source_commit · manifest_version · payload（JSONB）
- **ops_sync_run_artifacts**：graph_snapshot_id 关联（已存在 schema）
- **store.py**：`write_snapshot` · `link_artifact` · `get_latest_snapshot` · `get_open_issues_for_module`

---

## 3. 文件清单

| 路径 | 说明 |
| --- | --- |
| `api/ops/graph/__init__.py` | 模块导出 |
| `api/ops/graph/validator.py` | graph.json 结构校验 |
| `api/ops/graph/store.py` | snapshot 持久化 + ingest 函数 |
| `api/ops/graph/router.py` | `GET /summary` · `GET /module-issues` |
| `api/ops/router.py` | 聚合 graph_router |
| `api/ops/sync/runner.py` | 扩展 graph ingest 调用 |
| `.github/workflows/ops_sync_kimi_code.yml` | 新增 kimi-code-meta checkout |
| `tests/fixtures/graph_snapshot_sample_v1.json` | 开发降级 fixture |
| `tests/ops_desk/test_graph_ingest_p2.py` | 28 个测试用例 |
| `tests/ops_desk/test_scan_ingest_p2.py` | 更新：mock graph ingest |
| `tests/ops_desk/test_sync_p0.py` | 更新：mock graph ingest |

---

## 4. 阻塞点

无。

---

## 5. 建议

- `_manifest.json` 端点同步：当前未在 manifest 中显式添加 API 端点，因 task 中「若 verify 要求」为条件触发；本实现已覆盖全部功能，待前端联调时按需补充。

---

*Reinspect completed. Ready for PR.*
