# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| template | Projects/docs/harness/prompts/TEMPLATE-task-audit-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md |
| related_review_or_none | 无（首轮 R1） |
| prev_review | 无 |
| requirements_invoke | ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_10_tech-graph-v2-p4-requirements.md |
| created_utc_or_local | 2026-05-17 |
| notes | R1 审查已落盘 reviews/…_audit_R1_20260517.md；下一棒 30 invoke_20260517_30_tech-graph-v2-p4-exec.md |
| completed | 2026-05-17 · R1 零硬阻塞 |

## 可复制 Prompt 快照（下一棒 · 任务审核帽 R1）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/22-task-audit.md（身份、禁止项、输出形状、交接物）
- docs/harness/reviews/README.md（文件命名、R1/R2 闭环）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths 等与 task 字段对齐）
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（human_gate 硬规则）

【人工闸前置 — 开帽前必读】
task 文首 HG-TASK-DRAFT 须为 approved 且 blocks_hats 含 22-R1；若为 pending → 仅输出阻塞说明与须人改路径，禁止落盘审查结论或指示执行帽开工。

输入（占位符已替换）：
- 待审 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md
- 关联 SPEC / 总规路径（无则写「无」）：
docs/tech_graph/改进方向.md（v1.1.3）；docs/_tech_graph/graph_v2_schema.md；docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
- 上一轮审查文档路径（首轮）：
无

落盘文件建议名：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_p4_extended_v1_audit_R1_20260517.md

【对照材料 — 须通读】
- 前置 done task：docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md（§0.2 NR、G-END、FP-5）
- 关账审查：docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_CLOSE_20260517.md（P2-4 延后、§5.4 follow-up）
- P2-0 schema：docs/_tech_graph/graph_v2_schema.md
- 需求帽 invoke：docs/harness/invokes/invoke_20260517_10_tech-graph-v2-p4-requirements.md

【R1 审查焦点 — 须逐项结论】
1. P2-4a 字段表是否仍过重？`graphs[]`/`ref`/`kind` 能否再砍首 PR 范围？
2. §2.2 分期阻塞是否与 semi_auto `post_close` 一致（4a 阻塞、4b/4c 可选）？
3. test_strategy: required + note 是否对应可失败 pytest/CLI？
4. failure_paths FP-4-1～FP-4-4 是否可观测、与验收 §3 一一映射？
5. NR-1 / FP-5 / FP-4-3 是否足以拦住「重跑闸口 B」「整包 v2 默认」「query 破坏单图」？
6. freeze_id TBD 是否标注 merge 前 bump（非阻塞项须标明）？
7. P2-4c follow-up 是否与 conclusion_gate_b §5.4 一致且明确「非主实验重跑」？

你必须完成：
0. Invoke 快照：本消息已落盘 invoke_20260517_22_tech-graph-v2-p4-task-audit-r1.md 后可开工（元信息 invoke_snapshot 指向该路径）。
1. 通读待审 task 全文及 human_gate / test_strategy / failure_paths / §2.1–§2.2。
2. 对照 HARNESS_V2_PLAN.md §5 检查验收可观测性。
3. 落盘审查 md 至上述路径。
4. 文内结构：元信息 → 审查结论摘要 → 阻塞/非阻塞 → 需任务帽回填清单（若有）→ 是否建议执行帽开工 → 签收。
5. 若零硬阻塞：对话输出下一棒 **30 执行帽** 可复制 Prompt（TEMPLATE-execute-invoke §3，占位符已替换）；若需回填则输出 **10 需求帽** Prompt。
6. 禁止写业务代码；禁止代改 human_gate 为 approved。
7. 按 HANDOFF_AUTO_COMMIT 提交本轮 reviews/invoke 变更。
```
