---
task_slug: graph-yaml-export-yaml-p1
round: T1
hat: 40
freeze_id: GRAPH-YAML-EXPORT-YAML-P1
git_branch: task/graph-yaml-export-yaml-p1
date: 2026-06-17
---

# 40 · 图谱 graph.json 导出改读 YAML（Export-from-YAML · P1）· T1

## 复跑验收
| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `python tools/tech_graph_graph_export.py --check` | 0 | 与已提交 graph.json 语义一致 |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7/7 graph slices OK |
| 3 | `bash scripts/verify-tech-graph.sh` | 0 | 全步骤通过 |
| 4 | `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` | 0 | 109 passed, 1 skipped |
| 5 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | 419 passed, 1 skipped, 2 deselected |
| 6 | `ruff check api tests` | 0 | All checks passed |

## 范围核对
- D1–D7 全部完成；task §实现备忘、§自检结论已回填
- HG-REINSPECT → **signed**
- 未删除 7× `.ai.md`
- 未手改 `graph.json` 拓扑（graph.json 由 export 重新生成，仅节点/边标签按 YAML 真值校正、graphs[] 新增 `source_yaml_path`）
- 未引入 `external_ref` schema / `.cyning-harness/`

## 后续
- 开 PR → 等 CI 绿 → merge 入 `main`
- 合并后 `RECENT_TASK_SCHEDULE.md` §1.6 续 标注「Inform YAML 单源闭环完成」
- `.ai.md` 删除仍属 G0 另 task
