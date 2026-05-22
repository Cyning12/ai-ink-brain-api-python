# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 10 |
| template | Projects/docs/harness/prompts/TEMPLATE-requirements-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md |
| related_review_or_none | 无 |
| created_utc_or_local | 2026-05-17 |
| notes | 前置 task 已 done；10 帽 v0.2 已结构化 task；下一棒 invoke_20260517_22_tech-graph-v2-p4-task-audit-r1.md |
| completed | 2026-05-17 · task v0.2 |

## 可复制 Prompt 快照（下一棒 · 需求帽）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md

【目标与上下文】
前置 task「graph_v2 + graph_query + 闸口 B」已关账（done）。本棒将草案 task_engineering_tech_graph_v2_p4_extended_v1.md 结构化为可审、可执行的 P2-4 任务：graphs[]、edges[].ref、nodes[].kind、可选 manifest 互引与闸口 B §5.4 query follow-up。保持 CTX_QUERY 默认，禁止 NR-1 重跑闸口 A/B 主实验。

【已有材料路径或粘贴说明】
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_CLOSE_20260517.md
ai-ink-brain-api-python/docs/_tech_graph/graph_v2_schema.md
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
Projects/docs/tech_graph/改进方向.md

【是否按任务审核文档回填】
无

你必须完成：
0. Invoke 快照：本消息已落盘 invoke_20260517_10_tech-graph-v2-p4-requirements.md 后可开工。
1. 结构化块：背景/范围/非范围/依赖/验收/failure_paths/必读；分期 P2-4a/b/c 写清阻塞关系。
2. test_strategy: required + note。
3. 补全 human_gate 初值说明；建议 semi_auto、audit_profile post_close、git_branch 与草案一致。
4. 禁止写业务代码；禁止改未授权 CI。
5. 对话输出下一棒可复制 Prompt → 22 任务审核帽 R1（TEMPLATE-task-audit-invoke §3，占位符已替换）。
6. 按 HANDOFF_AUTO_COMMIT 提交本轮 task/invoke 变更。
```
