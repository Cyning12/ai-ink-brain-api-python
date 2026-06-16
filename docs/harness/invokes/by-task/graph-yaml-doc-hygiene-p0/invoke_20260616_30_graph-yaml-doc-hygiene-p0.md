---
task_slug: graph-yaml-doc-hygiene-p0
round: T1
hat: 30
freeze_id: GRAPH-YAML-DOC-HYGIENE-P0
git_branch: task/graph-yaml-doc-hygiene-p0
date: 2026-06-16
---

# 30 · 图谱 YAML 文档卫生（Doc Hygiene · P0）· T1

## 背景
Post-Epic 修复后 `99_spec` 已确立 `.graph.yaml` 为编辑源、`.ai.md` deprecated，但 `00_main.md` 的 Sub-graph Links 仍指向 `.ai.md`，人类导航与规约矛盾。本 task 清理 `.ai.md` 编辑源指针、记录幽灵节点遗留、加 pytest 防回归。

## 执行项
- **D1** 修改 `scripts/graph_yaml_compile.py` · `generate_sub_graph_links()`：7 张子流程链改为「编辑源 *.graph.yaml」，移除「AI 协议版 *.ai.md」链；Struct / Version 亦补编辑源链
- **D2** `python scripts/graph_yaml_compile.py --graph-id 00_main` 重生成 `docs/_tech_graph/00_main.md`
- **D3** `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` 增 §已知遗留 · 幽灵节点；版本 v1.0→v1.2；修订记录增 v1.2 行；关联 L0 指针 00_main.ai.md → 00_main.graph.yaml
- **D4** `docs/_tech_graph/` 内 grep 清扫：更新 `graph_v2_schema.md` 中 graphs[] 相关说明，避免将 `.ai.md` 标为编辑源；QNA 历史正文保留 `.ai.md` 讨论（非当前编辑源）
- **D5** `tests/test_graph_yaml_compile.py` 新增 `test_00_main_subgraph_links_no_ai_md_href`

## 关键验证结果
- `pytest tests/test_graph_yaml_compile.py -q` → **11 passed**
- `python scripts/graph_yaml_compile.py --all --check` → **exit 0（7/7 slices OK）**
- `bash scripts/verify-tech-graph.sh` → **OK**
- `pytest tests -m "not intent_eval and not intent_benchmark" -q` → **417 passed, 1 skipped, 2 deselected**
- `ruff check api tests` → **All checks passed**

## 变更文件（相对 repo root）
- `scripts/graph_yaml_compile.py`
- `tests/test_graph_yaml_compile.py`
- `docs/_tech_graph/00_main.md`
- `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md`
- `docs/_tech_graph/graph_v2_schema.md`

## 备注
- 50 按 task 指示 skip（`audit_profile: post_close` · 纯文档+工具卫生）
- 下一步：40 自检 → 回填 task §自检结论 → HG-REINSPECT signed → PR → CI 绿 → merge
