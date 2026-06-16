# Harness 30 执行编码 Agent — graph-yaml-p0-00-main

## 输入摘要
- 主 task: `docs/tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md`
- 逻辑子仓: `ai-ink-brain-api-python`
- 验证命令: `pytest tests -m "not intent_eval and not intent_benchmark"`
- 关联 SPEC: `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md`, `docs/_tech_graph/99_mermaid_protocol.md`, `docs/_tech_graph/graph_v2_schema.md`
- 22 R1 审查: `docs/harness/reviews/by-task/graph-yaml-p0-00-main/task_graph-yaml-p0-00-main_audit_R1_20260616.md`

## 交付范围
1. 创建 `docs/_tech_graph/00_main.graph.yaml`
2. 创建转换脚本 `scripts/graph_yaml_compile.py`
3. 生成 `docs/_tech_graph/00_main.md`
4. 新增 pytest 用例 ≥1
5. 执行验证
6. 回填 task §实现备忘 + §自检结论（执行者）
7. 自动 commit

## 残余风险处理
- R1-kind 缺失: graph.json 00_main 节点无 `kind` 字段，YAML schema 允许 `kind` 缺失
- R2-锚点渲染: 仅 4 条边带 anchors，YAML→MD 锚点注释格式与 `99_mermaid_protocol.md` §3 对齐
- R3-AUTO 块策略: P0 `00_main.md` 不嵌入 AUTO 块，`_manifest.json` 仍由现有工具维护

## 时间戳
2026-06-16
