---
task_slug: graph-v2-schema-dual-track
round: T1
hat: 30
freeze_id: GRAPH-V2-SCHEMA-DUAL-TRACK
git_branch: task/graph-v2-schema-dual-track
date: 2026-06-17
---

# 30 · graph_v2 JSON Schema 双轨 · T1

## 执行摘要
- 落盘 `docs/_tech_graph/graph_v2.schema.json`（P2-0 + P2-4a 机器真值）
- 重构 `tools/tech_graph_graph_v2_schema.py`：导入时加载 JSON，Python 保留跨引用/重复/互斥逻辑
- 更新 `docs/_tech_graph/graph_v2_schema.md`：canonical pointer + 修订记录
- 更新 `docs/_tech_graph/99_spec.md` §机器轨：schema 双轨指针
- `scripts/verify-tech-graph.sh` 显式接入 `tools/tech_graph_graph_v2_schema.py`
- `tests/test_tech_graph_graph_v2_p4_schema.py` 新增 F1 回归 + committed `graph.json` 直接 validate

## 关键决策
- JSON 路径：`docs/_tech_graph/graph_v2.schema.json`（与 `graph.json` 同目录）
- 同步策略：load JSON；禁止 Python 再维护字段表
- D7：仅 `graph_id_from_source_path` docstring，无行为变更

## 验证（30 预跑）
| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `python tools/tech_graph_graph_export.py --check` | 0 | OK |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7/7 OK |
| 3 | `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` | 0 | 113 passed, 1 skipped |
| 4 | `bash scripts/verify-tech-graph.sh` | 0 | OK |
| 5 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | 423 passed, 1 skipped, 2 deselected |
| 6 | `ruff check api tests` | 0 | All checks passed |

## 下一步
- 40 独立复跑 + 关账 + PR
