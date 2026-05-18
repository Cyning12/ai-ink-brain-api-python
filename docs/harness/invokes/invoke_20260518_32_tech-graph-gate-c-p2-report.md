# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/30-execute-code.md · P2 结论报告 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-gate-c-v2-dual-track-v1 |
| notes | PR-2 P2 结论报告；canonical batch `gate_ctx_c_v1_batch_20260518_052803`；上一棒 40 帽 invoke_20260518_31 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「执行编码帽（P2 · 闸口 C 结论报告）」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-gate-c-v2-dual-track-v1

输入：
- 主 task：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- 上一棒 40 自检 invoke：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_31_tech-graph-gate-c-40-self-check.md
- 40 帽已签收：§3.1/3.2/共用 pass；P2 报告未写
- canonical batch run：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/
- 静态 token：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/payloads/materialize_report.json
- 对照结论（只引用，勿重跑主实验）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
- 子仓根：ai-ink-brain-api-python
- 合并前验证：
pytest tests -m "not intent_eval and not intent_benchmark"

开帽前硬检查：
0. 将本消息全文落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_32_tech-graph-gate-c-p2-report.md。
0b. human_gate：HG-GATE-C-SIGNOFF 仅阻塞 done/50，不阻塞 30；若其他闸对 30 为 pending → 拒开工。
1. 通读 task §0.3（臂 D/E）、§3.3 P2、§1.2 NR-1/2；对照 conclusion_gate_b 结构撰写：
   docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
2. 报告须含：§0 实验设计（复现命令引 batch README）、§1 轴 II 静态 token（D vs E）、§2 轴 I S0 行为（gold_f1.md/jsonl）、§3 D vs E 胜负与 Agent 默认消费轨建议；**明确不推翻** 闸口 B 已采纳的 CTX_QUERY 默认。
3. 状态先标 `draft`；**不得**将 HG-GATE-C-SIGNOFF 代填为关账用 approved（人签在 accepted 后）。
4. 回填 task §1 P2 勾选与「### 自检结论（执行者）」30 帽 P2 行；输出下一棒 40 自检 Prompt。
5. 按 HANDOFF_AUTO_COMMIT 仅 add 本轮路径；对话报 short-hash。

禁止：重跑 gate_ctx_ab/b batch；改 A/B 历史 runs；无证据写 accepted；git add -A。
```
