# Task · Ops Desk · Graph 矩阵 + graph_analyst 消费层 · 后端 · v1

> **状态**：`pending`  
> **Harness 母单**：[`Projects/docs/harness/tasks/active/task_ops_desk_graph_consume_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_graph_consume_v1.md)  
> **Open Folder**：**本仓根** `ai-ink-brain-api-python/`

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` |
| **git_branch** | `task/ops-desk-graph-consume-backend` |
| **freeze_id** | `OPS-DESK-GRAPH-CONSUME-V1` |

---

## 背景与目标

meta graph Epic 已补 `module_id` + module 级边；Ops 消费层仍用 flow `node.id` join → Graph 矩阵与 `graph_analyst` 不可用。本 task 交付 **共享模块矩阵服务** + **graph_analyst 读 edges**。

---

## 范围

- [x] `api/ops/graph/module_matrix.py`：distinct `module_id` · issue 映射（labels + scan_tags + flow_map 回落）
- [x] 重构 `OpsGraphStore` / `GET /ops/graph/module-issues`
- [x] `graph_analyst` evidence 含 `module_edges`
- [x] pytest `tests/ops_desk/test_graph_module_matrix_v1.py`
- [x] `_manifest.json` 若变更则同步

## 非范围

- 改 kimi-code-meta graph 源
- 新建 DB 表

## 失败路径

| 触发条件 | 系统行为 | 可重试 | 用户可见 |
|----------|----------|--------|----------|
| 无 graph snapshot | Graph Tab 空态 · API 404 `GRAPH_SNAPSHOT_NOT_FOUND` | 是 · sync | 「尚未 ingest」 |
| snapshot 旧版无 `module_id` | 矩阵降级为 struct 节点 label；日志 warn | 是 · re-ingest | 行数少 / 边为空提示 |
| module 映射 0 命中 | 矩阵行存在 · issue_count=0 | 是 · 调映射规则 | 数字 0（非 500） |
| graph_analyst LLM 失败 | deep 502 结构化 | 是 | `LLM_REQUEST_FAILED` |

## 行为变更 Delta

- `GET /api/py/ops/graph/module-issues` 响应字段扩展：新增 `p0_count`, `p1_count`, `p2_count`, `issue_numbers`
- `graph_analyst` evidence 新增 `module_edges` 字段
- `OpsGraphStore` 新增 `get_module_matrix` / `get_module_edges` 方法（向后兼容，旧 `get_open_issues_for_module` 保留）

---

## 验收标准

- [ ] `pytest tests/ops_desk -m "not intent_eval and not intent_benchmark" -q` 绿
- [ ] `GET /api/py/ops/graph/module-issues` 模块行 ≤20 · staging 至少 1 行 issue_count>0
- [ ] graph_analyst 单测：evidence 含 edges 摘要

---

## 依赖

- [`api/ops/graph/store.py`](../../api/ops/graph/store.py)
- [`api/ops/agents/graph_analyst.py`](../../api/ops/agents/graph_analyst.py)
- [`kimi-code-meta/docs/_tech_graph/graph_module_flow_map.yaml`](../../../../kimi-code-meta/docs/_tech_graph/graph_module_flow_map.yaml)
