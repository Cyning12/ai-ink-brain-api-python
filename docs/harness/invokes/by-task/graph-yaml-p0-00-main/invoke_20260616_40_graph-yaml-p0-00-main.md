# Harness 40 自检 Agent — graph-yaml-p0-00-main

## 输入摘要
- 主 task: `ai-ink-brain-api-python/docs/tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md`
- 逻辑子仓: `ai-ink-brain-api-python`
- 30 invoke: `ai-ink-brain-api-python/docs/harness/invokes/by-task/graph-yaml-p0-00-main/invoke_20260616_30_graph-yaml-p0-00-main.md`
- 22 R1 审查: `ai-ink-brain-api-python/docs/harness/reviews/by-task/graph-yaml-p0-00-main/task_graph-yaml-p0-00-main_audit_R1_20260616.md`
- HG-AUDIT-R1: approved
- 前置: 30 帽已完成

## 40 帽职责
1. 读取 task §自检结论（执行者）和 §实现备忘。
2. 独立复跑以下命令并记录退出码 + 摘要：
   - `python scripts/graph_yaml_compile.py --check`
   - `pytest tests/test_graph_yaml_compile.py -v`
   - `pytest tests -m "not intent_eval and not intent_benchmark" -q`
3. 核对 30 交付物：
   - `docs/_tech_graph/00_main.graph.yaml` 存在且可解析
   - `scripts/graph_yaml_compile.py` 存在且 `--check` 通过
   - `docs/_tech_graph/00_main.md` 已生成且含 frontmatter/表格/Mermaid
   - `tests/test_graph_yaml_compile.py` ≥1 用例
   - `00_main.ai.md` 未删除且头部有 `@deprecated · 源迁 YAML`
   - 未引入 `.cyning-harness/` 或 `npx @cyning/harness`
4. 如有缺失或命令失败，在 task §自检结论中新增修正项并要求打回 30；如全部通过，确认/完善 §自检结论表。
5. 落盘 invoke
6. 自动 commit（仅本轮路径：task 文件 + invoke）

## 时间戳
2026-06-16
