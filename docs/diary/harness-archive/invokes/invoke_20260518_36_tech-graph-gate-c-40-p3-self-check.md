# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/40-self-check.md · PR-3 独立复验 |
| task_paths | ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | main（或任务分支） |
| notes | PR-3 P3 文档只读复验；上一棒 30 invoke_20260518_35 · 子仓 cf48ee9 · 工作区 738045c |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演 Harness「自检帽（40）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md

【输入】
- task：ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- 30 交付 commit：子仓 cf48ee9 · 工作区 738045c
- 30 invoke：docs/harness/invokes/invoke_20260518_35_tech-graph-gate-c-p3-docs.md
- 只读结论：docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md（勿改 accepted）

【复验范围 · PR-3 only】
1. 只读核对 Projects/docs/tech_graph/改进方向.md 闸口 C 表行、§2.7、三者关系注记与 B 默认表述。
2. 只读核对 Projects/docs/tech_graph/tasks/ai-ink-brain-api-python/README.md done 路径与结论链。
3. 独立跑：cd ai-ink-brain-api-python && pytest tests -m "not intent_eval and not intent_benchmark" -q
4. 回填 task §6「#### 40 帽（PR-3 · …）」；§1.1 P3 仅在有命令证据后保持 [x]。
5. 落盘 invoke_36 + 分仓 commit（禁止 git add -A）。

禁止：重跑 gate_ctx_c batch；代填 human_gate；修改结论 accepted。
```
