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

- [ ] `api/ops/graph/module_matrix.py`：distinct `module_id` · issue 映射（labels + scan_tags + flow_map 回落）
- [ ] 重构 `OpsGraphStore` / `GET /ops/graph/module-issues`
- [ ] `graph_analyst` evidence 含 `module_edges`
- [ ] pytest `tests/ops_desk/test_graph_module_matrix_v1.py`
- [ ] `_manifest.json` 若变更则同步

## 非范围

- 改 kimi-code-meta graph 源
- 新建 DB 表

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
