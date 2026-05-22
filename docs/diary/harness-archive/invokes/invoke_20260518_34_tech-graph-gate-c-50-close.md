# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| template | docs/harness/prompts/50-independent-reinspect.md · 关账 |
| task_paths | ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-gate-c-v2-dual-track-v1 |
| notes | 独立复检 + 关账；上一棒 invoke_20260518_33；结论 accepted + HG-GATE-C-SIGNOFF approved |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「独立复检 + 关账帽（50）」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md
- docs/harness/prompts/HANDOFF_CLOSE_TRACE.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-gate-c-v2-dual-track-v1

【人侧前置（须已完成再开帽）】
- 将 docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md 状态由 draft 改为 accepted（人改，Agent 禁止代填）
- task 中 HG-GATE-C-SIGNOFF 已为 approved

输入：
- 主 task：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- 上一棒 40 invoke：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_33_tech-graph-gate-c-40-p2-self-check.md
- P2 结论（须已为 accepted）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
- canonical batch：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/
- 子仓根：ai-ink-brain-api-python
- 合并前验证：
pytest tests -m "not intent_eval and not intent_benchmark"

开帽前硬检查：
0. 落盘 invoke_20260518_34_tech-graph-gate-c-50-close.md（元数据表 + 快照）。
0b. 若结论仍为 draft → 拒开工，列出须人改路径。
1. 对照 task §3 全表 + 40 帽自检结论，输出复检 pass/fail 表（含证据路径）。
2. 输出 HANDOFF_CLOSE_TRACE（本 task 相关 commit 回溯表）。
3. 将 task 状态改为 done（或 §1.3 PR-3 若人授权 P3 文档帽则另开 invoke，不阻塞关账）。
4. 按 HANDOFF_AUTO_COMMIT 仅 add 本轮路径；对话报 short-hash。

禁止：结论仍为 draft 时勾选关账；代填 human_gate；git add -A；重跑 gate_ctx_c batch。
```

## 50 帽关账结论（落盘摘要）

| 项 | 结果 |
| --- | --- |
| 开帽前 0b | **pass** — 结论 L3 `accepted`；`HG-GATE-C-SIGNOFF` `approved` |
| §3 全表复检 | **pass**（P3 recommended 未勾选 · 不阻塞） |
| pytest 主链 | **pass** — 193 passed, 1 skipped |
| 建议合并 | **是**（闸口 C 实验收口；P3 可另 task） |
