# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| template | docs/harness/prompts/TEMPLATE-task-audit-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | 无（首轮 R1） |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-gate-c-v2-dual-track-v1 |
| notes | 闸口 C task v0.1 · R1 开帽；HG-TASK-DRAFT pending 触发 0b 硬停 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「任务审核帽（R1）」，严格遵循：
- docs/harness/prompts/22-task-audit.md
- docs/harness/prompts/TEMPLATE-task-audit-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-gate-c-v2-dual-track-v1

输入：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- 子仓根：ai-ink-brain-api-python
- 需求帽 invoke：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_10_tech-graph-gate-c-v2-dual-track-requirements.md
- 关联 SPEC / 总规：
Projects/docs/tech_graph/改进方向.md（R4 对比实验）
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
- 前置结论（勿重跑为主实验）：
docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md
docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
- materialize 参考：
docs/diary/jsonPKmermaid/fixtures/gate_ctx_b_v1/scripts/materialize_gate_b_payloads.py

开帽前硬检查：
0. 落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_22_tech-graph-gate-c-v2-dual-track-audit-r1.md
0b. 若 HG-TASK-DRAFT 仍为 pending → 仅输出须人改的 gate_id，拒开工。
1. 通读 task：§0.3 双臂 D/E、§1.2 NR-1/2、P0～P2 分期、§4 failure_paths、§5 必读。
2. 核对：CTX_DUAL_MD 非整包灌入；与闸口 B 的 CTX_QUERY 差异是否写清；freeze_id 是否需 bump 规则。
3. 输出：审查 md → docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md
4. 零硬阻塞则附「下一棒 30 执行」Prompt；有阻塞则回填清单。
5. 禁止代填 HG-AUDIT-R1；禁止写业务代码。
6. HANDOFF_AUTO_COMMIT 仅 commit 本轮路径；对话报 short-hash。
```
