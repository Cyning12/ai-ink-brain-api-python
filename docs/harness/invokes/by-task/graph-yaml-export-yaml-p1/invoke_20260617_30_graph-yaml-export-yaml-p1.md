---
task_slug: graph-yaml-export-yaml-p1
round: T1
hat: 30
freeze_id: GRAPH-YAML-EXPORT-YAML-P1
git_branch: task/graph-yaml-export-yaml-p1
date: 2026-06-17
---

# 30 · 图谱 graph.json 导出改读 YAML（Export-from-YAML · P1）· T1

## 背景
P0 已清理 `.ai.md` 编辑源指针；本 task 完成 Inform 闭环：export 主路径改读 `*.graph.yaml`，`graph.json` 由 YAML 生成，CI 不再依赖 `.ai.md` 内容。

## 执行项
- **D1** 新增 `tools/tech_graph_graph_v2_yaml.py`：遍历 `*.graph.yaml`，合并为与 `build_reference_graph_v2` 等价的 graph_v2 载荷
- **D2** `tools/tech_graph_graph_export.py` · `build_graph_payload()` 改调 YAML builder；docstring / CLI 更新为「默认读 `.graph.yaml`」
- **D3** 保留 `collect_raw_edges` / `raw_edges_to_graph_dict` 等 `.ai.md` 解析函数供单测 / 迁移对照
- **D4** `tools/tech_graph_manifest_check.py`：移除 `00_main.ai.md` auto 区块 TIP，改指向 `_manifest.json` / `00_main.graph.yaml`
- **D5** `docs/_tech_graph/99_spec.md` §机器轨：`graph.json` 由 YAML export 生成；`.ai.md` 只读 deprecated 对照
- **D6** 扩展 pytest：`tests/test_tech_graph_graph_export.py` YAML fixture 用例 + `test_run_check_ignores_ai_md_drift`（F3 回归）
- **D7** 运行 `bash scripts/verify-tech-graph.sh` 全绿

## 关键验证结果
- `python tools/tech_graph_graph_export.py --check` → **exit 0**
- `python scripts/graph_yaml_compile.py --all --check` → **exit 0（7/7 slices OK）**
- `bash scripts/verify-tech-graph.sh` → **OK**
- `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` → **109 passed, 1 skipped**
- `pytest tests -m "not intent_eval and not intent_benchmark" -q` → **419 passed, 1 skipped, 2 deselected**
- `ruff check api tests` → **All checks passed**

## 变更文件（相对 repo root）
- `tools/tech_graph_graph_v2_yaml.py`（新增）
- `tools/tech_graph_graph_export.py`
- `tools/tech_graph_graph_equivalence_check.py`
- `tools/tech_graph_manifest_check.py`
- `docs/_tech_graph/99_spec.md`
- `docs/_tech_graph/graph.json`（由 export 重新生成）
- `tests/test_tech_graph_graph_export.py`
- `tests/test_tech_graph_graph_v2_equivalence.py`
- `tests/test_tech_graph_graph_v2_p4_export.py`

## 备注
- 50 按 task 指示 skip（`audit_profile: post_close`）
- 下一步：40 自检 → 回填 task §自检结论 → HG-REINSPECT signed → PR → CI 绿 → merge
- PR 标题建议：`feat(graph): graph.json export 改读 YAML · 单源闭环`
