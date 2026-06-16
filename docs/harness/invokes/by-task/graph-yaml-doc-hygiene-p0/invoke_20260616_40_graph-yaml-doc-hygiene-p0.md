---
task_slug: graph-yaml-doc-hygiene-p0
round: T1
hat: 40
freeze_id: GRAPH-YAML-DOC-HYGIENE-P0
git_branch: task/graph-yaml-doc-hygiene-p0
date: 2026-06-16
---

# 40 · 图谱 YAML 文档卫生（Doc Hygiene · P0）· T1

## 复跑验收
| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `pytest tests/test_graph_yaml_compile.py -q` | 0 | 11 passed |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7/7 graph slices OK |
| 3 | `bash scripts/verify-tech-graph.sh` | 0 | 全步骤通过 |
| 4 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | 417 passed, 1 skipped, 2 deselected |
| 5 | `ruff check api tests` | 0 | All checks passed |

## 范围核对
- D1–D5 全部完成；task §实现备忘、§自检结论已回填
- HG-REINSPECT → **signed**
- 未触碰 `tools/tech_graph_graph_export.py`、`tools/tech_graph_manifest_check.py`、`graph.json` 拓扑、`external_ref` schema
- 未删除任意 `.ai.md`

## 后续（已执行）
- PR [#176](https://github.com/Cyning12/ai-ink-brain-api-python/pull/176) · CI 全绿 · merged `57f1035`
- `RECENT_TASK_SCHEDULE.md` §1.6 续 已更新：P0 merged · P1 unblocked
- **P0 merge 后，P1 `graph-yaml-export-yaml-p1` 方可开 30**
