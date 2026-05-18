# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 10 |
| template | Projects/docs/harness/prompts/TEMPLATE-requirements-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md |
| related_review_or_none | 无 |
| created_utc_or_local | 2026-05-18 |
| notes | 方案2 补全 v0.2；graph_query 已交付；**无新闸口实验** |
| git_branch | task/engineering-tech-graph-scheme2-completion-v1 |
| next_hat | 22 R1 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-scheme2-completion-v1

【目标与上下文】
graph_query task 已交付 graph_v2 + tech_graph_graph_query.py + 闸口 B 定稿。
本棒将 task_engineering_tech_graph_scheme2_completion_v1 结构化至 v0.2：
对齐改进方向.md §方案2 与 scheme_2_graph_query.md；补 has_path / describe_impact + pytest；
文档与实现模块名一致；可选 MCP 或 Harness 挂钩（recommended）。
禁止：闸口 A/B 主实验、run_gate_b_batch 全 arms、Neo4j、schema 语义变更、改 workflow。

【已有材料路径】
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md
ai-ink-brain-api-python/tools/tech_graph_graph_query.py
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
Projects/docs/tech_graph/改进方向.md
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_10_tech-graph-scheme2-completion-requirements.md

【是否按任务审核文档回填】
无

你必须完成：
0. 读 invoke 快照；更新 task 至 v0.2
1. 结构化块 + 矛盾扫描（graph_query.py 命名 vs tech_graph_graph_query.py）
2. test_strategy: required
3. semi_auto / human_gate / git_branch 一致
4. 禁止业务代码与 CI
5. 输出下一棒 22 R1 可复制 Prompt
6. HANDOFF_AUTO_COMMIT 提交本轮 task/invoke
```
