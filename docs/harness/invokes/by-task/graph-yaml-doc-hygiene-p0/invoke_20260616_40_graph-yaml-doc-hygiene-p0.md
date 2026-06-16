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

## 下一步
- `git mv` task → `docs/tasks/done/`
- 更新 `docs/tasks/_views/done.md`、`done_by_domain.md`、`RECENT_TASK_SCHEDULE.md` §1.6 续
- commit · push · 开 PR → 等 CI 绿 → merge 入 main
- **P0 merge 前不得启动 P1**
