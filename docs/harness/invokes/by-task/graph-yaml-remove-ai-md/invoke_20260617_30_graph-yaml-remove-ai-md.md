# Invoke · 30 执行 · graph-yaml-remove-ai-md

| 字段 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-remove-ai-md` |
| **hat** | 30 |
| **date** | 2026-06-17 |
| **branch** | `task/graph-yaml-remove-ai-md` |
| **freeze_id** | `GRAPH-YAML-REMOVE-AI-MD` |
| **predecessor** | G0 `ontology-inventory-scan-g0` · HG-INVENTORY-ARCHIVED signed |

---

## 执行摘要

| 交付 | 结果 |
| --- | --- |
| D1 删 7× `.ai.md` | pass · `find` → 0 |
| D2–D4 规约/QNA/schema | pass |
| D5 pytest + dual_track_manifest v3 | pass |
| D6 RECENT 日志 | pass |
| D7 verify + pytest | pass · 419 passed |

---

## 验证

```bash
find docs/_tech_graph -name '*.ai.md' | wc -l   # 0
python scripts/graph_yaml_compile.py --all --check
python tools/tech_graph_graph_export.py --check
bash scripts/verify-tech-graph.sh
pytest tests -m "not intent_eval and not intent_benchmark" -q
```

---

## 待关账

- PR merge · task → `done/` · HG-REINSPECT（skip 50）
