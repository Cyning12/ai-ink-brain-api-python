# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | Projects/docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md |
| audit_review | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_p4_extended_v1_audit_R1_20260517.md |
| audit_invoke | ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_22_tech-graph-v2-p4-task-audit-r1.md |
| git_branch | task/engineering-tech-graph-v2-p4-extended-v1 |
| created | 2026-05-17 |
| notes | R1 零硬阻塞；开 30 前须 HG-AUDIT-R1: approved |

## 可复制 Prompt 快照（下一棒 · 执行编码帽）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md

【人工闸 — 开帽前必读】
task 文首 HG-AUDIT-R1 须为 approved 且 blocks_hats 含 30；若为 pending → 仅输出阻塞说明，禁止改业务代码。

输入（占位符已替换）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md
- 子仓根（相对 Projects/）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_p4_extended_v1_audit_R1_20260517.md
- 关联 SPEC / 总规：
docs/tech_graph/改进方向.md（v1.1.3）；docs/_tech_graph/graph_v2_schema.md；docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md

你必须完成：
0. Invoke 快照：本消息已落盘 invoke_20260517_30_tech-graph-v2-p4-exec.md 后可开工。
0b. 确认 HG-AUDIT-R1: approved；否则拒开工。
1. 通读 task v0.2 与 R1 审查 N-1：从 P2-4a 开工；建议首 PR 仅 kind + schema 条件分支（4a-1），次 PR graphs[]+ref（4a-2）；禁止单 PR 塞 4b/4c/多分图 query。
2. 升级 tech_graph_graph_v2_schema.py（现 FORBIDDEN 须改为有则校验）；更新 graph_v2_schema.md。
3. test_strategy: required — 先增失败 pytest（含无 P2-4 字段时 FP-4-4 回归、非法 ref 非 0），再改导出/等价。
4. 禁止：graph_query 默认多读分图；run_gate_b_batch 全 arms 重跑（NR-1）；默认整包 v2 进 prompt（FP-5）。
5. P2-4a 首 merge 前 bump freeze_id 与 fixtures/gate_ctx_ab_v1/protocol_version.yaml 对齐。
6. 子仓根执行 VERIFY；回填 task「### 自检结论（执行者）」。
7. semi_auto：完成后再落盘 40 自检 invoke 并 commit（若 HG 无阻塞）。
8. 按 HANDOFF_AUTO_COMMIT 提交本轮代码/测试/task 变更。

禁止：扩 scope 至 Neo4j/退役 .ai.md；无测试静默放开 graphs[]/ref/kind。
```
