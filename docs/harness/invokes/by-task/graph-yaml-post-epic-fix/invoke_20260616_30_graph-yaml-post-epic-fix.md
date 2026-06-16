---
task_slug: graph-yaml-post-epic-fix
round: T1
hat: 30
freeze_id: GRAPH-YAML-POST-EPIC-FIX
git_branch: task/graph-yaml-post-epic-fix
date: 2026-06-16
---

# 30 · 图谱 YAML Post-Epic 修复 · T1

## 背景
Epic YAML 迁移已关账；复查发现 `--all` stem bug、`10_flow_rag.md` Mermaid 漂移、CI 未校验 YAML、文档仍写 `.ai.md` 为机器轨。

## 执行项
- **D1** 修复 `scripts/graph_yaml_compile.py` 的 `all_graph_ids()`：用 `p.name[:-len(".graph.yaml")]` 代替 `p.stem`，避免得到 `00_main.graph`
- **D2** 扩展 `tests/test_graph_yaml_compile.py`：新增 `test_all_graph_ids_returns_seven_ids_without_graph_suffix`、`test_compile_all_check_mode_exits_zero`
- **D3** `python scripts/graph_yaml_compile.py --all` 重生成 7 张 `.md`；同步修复 `format_anchor_comment()` 以渲染裸 `path` 锚点
- **D4** `scripts/verify-tech-graph.sh` 在 export 前增加 `python scripts/graph_yaml_compile.py --all --check`
- **D5/D6/D7** 更新 `99_spec.md`、`99_mermaid_protocol.md`、`QNA_graph_wiki_history_upgrade_v1_zh.md`、`15_e2e_boundary.graph.yaml`

## 关键验证结果
- `pytest tests/test_graph_yaml*.py -q` → **64 passed**
- `python scripts/graph_yaml_compile.py --all --check` → **exit 0**
- `bash scripts/verify-tech-graph.sh` → **OK**
- `pytest tests -m "not intent_eval and not intent_benchmark" -q` → **416 passed, 1 skipped, 2 deselected**
- `ruff check api tests` → **All checks passed**

## 变更文件（相对 repo root）
- `scripts/graph_yaml_compile.py`
- `scripts/verify-tech-graph.sh`
- `tests/test_graph_yaml_compile.py`
- `tests/test_graph_yaml_p1_10_flow_rag.py`
- `tests/test_graph_yaml_p2_11_flow_text2sql.py`
- `tests/test_graph_yaml_p3a_12_flow_fts.py`
- `tests/test_graph_yaml_p3b_13_flow_supabase_rpc.py`
- `tests/test_graph_yaml_p4_14_runtime_observability.py`
- `tests/test_graph_yaml_p5_15_e2e_boundary.py`
- `docs/_tech_graph/00_main.md`
- `docs/_tech_graph/10_flow_rag.md`
- `docs/_tech_graph/11_flow_text2sql.md`
- `docs/_tech_graph/12_flow_fts.md`
- `docs/_tech_graph/13_flow_supabase_rpc.md`
- `docs/_tech_graph/14_runtime_observability.md`
- `docs/_tech_graph/15_e2e_boundary.md`
- `docs/_tech_graph/15_e2e_boundary.graph.yaml`
- `docs/_tech_graph/99_spec.md`
- `docs/_tech_graph/99_mermaid_protocol.md`
- `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md`

## 备注
- 50 按 task 指示 skip（`audit_profile: post_close` · 纯工具+文档）
- 下一步：40 自检回填 task → HG-REINSPECT 签后 PR
