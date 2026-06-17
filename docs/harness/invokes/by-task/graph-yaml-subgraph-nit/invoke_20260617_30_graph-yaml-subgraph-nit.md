# Invoke · 30 执行 · graph-yaml-subgraph-nit

| 字段 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-subgraph-nit` |
| **hat** | 30 |
| **date** | 2026-06-17 |
| **branch** | `task/graph-yaml-subgraph-nit` |
| **freeze_id** | `GRAPH-YAML-SUBGRAPH-NIT` |

---

## 执行摘要

| 交付 | 结果 |
| --- | --- |
| D1 `generate_sub_graph_links()` | Struct/Version 仅 `.md` · 标注手写 |
| D2 重生成 `00_main.md` | pass |
| D3 `test_00_main_subgraph_no_dead_yaml_href` | pass |
| D4 verify-tech-graph | pass |

---

## 验证

```bash
pytest tests/test_graph_yaml_compile.py -q
bash scripts/verify-tech-graph.sh
```
