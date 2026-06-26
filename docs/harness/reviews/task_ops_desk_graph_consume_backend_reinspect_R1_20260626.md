# 50 独立复检 · OPS-DESK-GRAPH-CONSUME-BACKEND-V1

> 日期：2026-06-26  
> 执行者：OPS-DESK-GRAPH-CONSUME-V1 泳道 A 后端 Agent  
> 分支：`task/ops-desk-graph-consume-backend`  
> 状态：**PASS**（全部自检项通过）

---

## 1. 40 命令复跑结果

| 命令 | 结果 |
|------|------|
| `pytest tests/ops_desk/test_graph_module_matrix_v1.py -v` | 25 passed |
| `pytest tests/ops_desk/test_graph_ingest_p2.py -q` | 28 passed |
| `pytest tests/ops_desk/ -q` | 228 passed, 9 skipped |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 651 passed, 10 skipped |
| `python tools/tech_graph_manifest_check.py` | OK |
| `ruff check api/ops tests/ops_desk` | All checks passed |

---

## 2. 走查清单

### 2.1 模块行 ≤20
- `_extract_module_ids` 在 `module_matrix.py:75` 处 `if len(result) >= 20: break`
- `test_max_20` 验证 25 节点仅返回 20 个
- **PASS**

### 2.2 至少 1 模块在 fixture 下 issue_count>0
- `test_build_matrix` 中 `agent_core` issue_count=1, `cli` issue_count=1, `node_sdk` issue_count=1
- **PASS**

### 2.3 module_id 来源合规
- 优先 `node.module_id`（post-Epic），次选 `node.kind == "struct"` 的 `node.id`
- 禁止 flow `node.id` 作 module_id（`FLOW_TURN` 被过滤）
- `test_extracts_module_id_first` / `test_fallback_struct_kind` / `test_no_module_nodes` 覆盖
- **PASS**

### 2.4 Issue 映射优先级
- labels `module:{id}` 优先 → `test_label_hit`
- scan_tags 非空 + flow_map 回落 → `test_label_miss_scan_hit` / `test_body_substring_hit`
- **PASS**

### 2.5 graph_analyst evidence 含 edges 摘要
- `test_evidence_has_module_edges` 验证 evidence[0]["module_edges"] 存在且 `from/to/relation` 正确
- prompt 含 "模块依赖边摘要" 字符串
- **PASS**

### 2.6 API 契约一致性
- `GET /api/py/ops/graph/module-issues` 返回字段：`module_id`, `label`, `open_issue_count`, `p0_count`, `p1_count`, `p2_count`, `issue_numbers`, `sample_issues`
- `test_module_issues_v1_schema` 逐项断言
- 与 CHAIN API 契约一致
- **PASS**

### 2.7 禁止项
- 未改 kimi-code-meta 上游
- 未硬编码假 issue 数
- 未遍历全部 flow node 作矩阵行
- **PASS**

---

## 3. 变更文件清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `api/ops/graph/module_matrix.py` | 新增 | 模块矩阵服务（module_id 提取、issue 映射、tier 计数、edges 过滤） |
| `api/ops/graph/store.py` | 修改 | 新增 `get_module_matrix` / `get_module_edges` 委托方法 |
| `api/ops/graph/router.py` | 修改 | `GET /module-issues` 委托矩阵服务，返回 v1 契约 |
| `api/ops/graph/__init__.py` | 修改 | 导出 `ModuleMatrixService` |
| `api/ops/agents/graph_analyst.py` | 修改 | 使用矩阵服务，evidence 增加 `module_edges` |
| `tests/ops_desk/test_graph_module_matrix_v1.py` | 新增 | 25 个测试用例覆盖全部核心逻辑 |
| `tests/ops_desk/test_graph_ingest_p2.py` | 修改 | FakeGraphStore 新增 `get_module_matrix` / `get_module_edges` 兼容 |

---

## 4. 结论

- **40 全绿**：6 项命令全部通过
- **50 走查**：7 项检查全部通过
- **落盘**：本文件已写入 `docs/harness/reviews/task_ops_desk_graph_consume_backend_reinspect_R1_20260626.md`
- **建议**：可进入 CLOSE 阶段（git mv task → done + push + PR）
