---
task_slug: graph-v2-schema-dual-track
round: T1
hat: 40
freeze_id: GRAPH-V2-SCHEMA-DUAL-TRACK
git_branch: task/graph-v2-schema-dual-track
date: 2026-06-17
---

# 40 · graph_v2 JSON Schema 双轨 · T1

## 复跑验收
| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `python tools/tech_graph_graph_export.py --check` | 0 | OK |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7/7 OK |
| 3 | `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` | 0 | 113 passed, 1 skipped |
| 4 | `bash scripts/verify-tech-graph.sh` | 0 | OK（含新增 schema validation 步骤） |
| 5 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | 423 passed, 1 skipped, 2 deselected |
| 6 | `ruff check api tests` | 0 | All checks passed |

## 范围核对
- D1–D7 全部完成；task §实现备忘、§自检结论已回填
- HG-REINSPECT → **approved** · post_close 免检按 task
- 未改 `cyning-harness/` · HGM / events
- 未手改 `graph.json` 拓扑
- 未引入 `external_ref` schema

## 后续
- 开 PR → 等 CI 绿 → merge 入 `main`
- 合并后 `RECENT_TASK_SCHEDULE.md` §1.8 状态同步为 done
