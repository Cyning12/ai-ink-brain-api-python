# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/40-self-check.md · P2 独立复验 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-gate-c-v2-dual-track-v1 |
| notes | PR-2 P2 结论 draft 只读核对 + pytest 独立复验；上一棒 invoke_20260518_32 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-gate-c-v2-dual-track-v1

输入：
- 主 task（相对工作区根 Projects/）：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- 上一棒 30 P2 invoke：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_32_tech-graph-gate-c-p2-report.md
- P2 结论（只读核对，勿重跑 LLM batch）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
- canonical batch（证据链）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/
- 静态 token：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/payloads/materialize_report.json
- 子仓根：ai-ink-brain-api-python
- 主验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"

开帽前硬检查：
0. 将本消息全文落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_33_tech-graph-gate-c-40-p2-self-check.md（元数据表 + 快照 fenced code）。
0b. 复读 task human_gate：凡 blocks 含 40 且 status=pending → 拒开工并列 gate_id。
1. 只读核对 P2 报告：§0～§3 与 gold_f1.md、materialize_report.json、batch README 数字一致；状态须为 draft（不得代填 accepted）。
2. 独立复跑：pytest tests -m "not intent_eval and not intent_benchmark"（及可选 test_gate_ctx_c_v1_*.py）。
3. 核对 NR-1/2：未改 gate_ctx_ab/b 历史 run；未重跑 gate_ctx_b_batch。
4. 更新 task「### 自检结论（执行者）」**40 帽 P2 复验**小节；§3.3 P2 项 pass/fail 表。
5. 对话末尾输出下一棒 Prompt（人签 HG-GATE-C-SIGNOFF 后 50 关账，或 P3 文档帽若 task 授权）。
6. 按 HANDOFF_AUTO_COMMIT 仅 add 本轮路径；对话报 short-hash。

禁止：无证据勾选 accepted；代填 human_gate；git add -A；重跑 gate_ctx_c batch。
```
