# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 10 |
| template | docs/harness/prompts/TEMPLATE-requirements-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | 无 |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-gate-c-v2-dual-track-v1 |
| notes | 闸口 C 新实验 task v0.1 初稿 |

## 可复制 Prompt 快照

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md
- docs/harness/HARNESS_V2_PLAN.md §5

【目标与上下文】
立项闸口 C：对比 graph_v2 查询轨（CTX_V2_QUERY）vs 双轨原文（CTX_DUAL_MD：精选 *.ai.md + 配对 *.md）。
不复跑闸口 A/B 主实验。首要交付 P0 protocol + materialize + pytest。

【已有材料路径】
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
docs/tasks/done/task_engineering_tech_graph_scheme2_completion_v1.md（§8 F-exp-v2-dual）
docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
docs/diary/jsonPKmermaid/fixtures/gate_ctx_b_v1/

【是否按任务审核文档回填】
无
```
