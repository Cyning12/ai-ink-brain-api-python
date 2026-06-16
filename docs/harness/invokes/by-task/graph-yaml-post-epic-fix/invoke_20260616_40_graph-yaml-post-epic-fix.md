---
task_slug: graph-yaml-post-epic-fix
round: T1
hat: 40
freeze_id: GRAPH-YAML-POST-EPIC-FIX
git_branch: main
date: 2026-06-16
---

# 40 · 图谱 YAML Post-Epic 修复 · 自检

## 输入

- task: `docs/tasks/done/task_engineering_graph_yaml_post_epic_fix_v1.md`
- 30 invoke: `invoke_20260616_30_graph-yaml-post-epic-fix.md`
- 合并 commit: `f12e2a6`（已合入 `main`）

## 40 独立复验

| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `pytest tests/test_graph_yaml*.py -q` | 0 | 64 passed |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7 graph 全 OK |
| 3 | Mermaid body vs `generate_md()`（7 图） | — | 7/7 无 drift |
| 4 | `bash scripts/verify-tech-graph.sh` 核心步（skip human_gate 若离线） | 0 | manifest → yaml check → export → drift → equiv 全绿 |

## 交付物核对

- [x] D1–D7 范围项均已实现（见 task §实现备忘）
- [x] `verify-tech-graph.sh` 含 YAML `--all --check`（export 前）
- [x] `99_spec` / `99_mermaid_protocol` / QNA 已更新
- [x] 7× `.ai.md` **未删**（非范围 · `@deprecated` 保留）
- [x] `tech_graph_graph_export.py` **未改**（非范围 · 过渡方案）
- [x] invoke 30 已落盘

## 结论

**PASS** · HG-REINSPECT 可签 · 50 skip（`audit_profile: post_close`）

## 下一棒

task → `done/` · 索引更新 · 遗留项另 task（export 迁移 · G0 删 `.ai.md`）
