# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 10 |
| template | Projects/docs/harness/prompts/TEMPLATE-requirements-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md |
| related_review_or_none | 无（v0.1 草案 · 本棒结构化至 v0.2） |
| created_utc_or_local | 2026-05-18 |
| notes | 方案2 工程已交付于 graph_query task；本棒补 API/文档/MCP 缺口；**无新闸口实验** |
| git_branch | task/engineering-tech-graph-scheme2-completion-v1 |
| next_hat | 22 R1 |

## 可复制 Prompt 快照（开帽 · 需求帽）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-scheme2-completion-v1
（自 origin/main 拉出；P2-4b/4c 在独立分支 task/engineering-tech-graph-v2-p4-bc-followup-v1 待合）

【目标与上下文】
graph_query task 已交付 graph_v2 + tech_graph_graph_query.py（downstream/upstream/neighbors）+ 闸口 B 定稿。
本棒结构化「方案2 补全」task：对齐改进方向.md §方案2 与 scheme_2_graph_query.md；
补 has_path / describe_impact（或等价）+ pytest；文档勾选与模块名一致；
可选 MCP 或 Harness 模板挂钩（recommended）。
禁止：闸口 A/B 主实验、run_gate_b_batch 全 arms、Neo4j、graph_v2 schema 语义变更、改 workflow。

【已有材料路径】
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_p4_bc_followup_v1.md
ai-ink-brain-api-python/tools/tech_graph_graph_query.py
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
Projects/docs/tech_graph/改进方向.md（v1.1.3）
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
Projects/docs/harness/reviews/README.md（指针索引）

【是否按任务审核文档回填】
无

你必须完成：
0. Invoke 快照已落盘 invoke_20260518_10_tech-graph-scheme2-completion-requirements.md
1. 将 task 升至 v0.2：矛盾扫描（改进方向 graph_query.py 名 vs tech_graph_graph_query.py）；§1.3 分期；§3 可勾选命令化
2. test_strategy: required + note（保持）
3. semi_auto / human_gate / git_branch 与分支一致
4. 禁止写业务代码；禁止改 CI
5. 对话输出下一棒 22 R1 可复制 Prompt（TEMPLATE-task-audit-invoke §3）
6. 按 HANDOFF_AUTO_COMMIT 提交 task + invoke
```
