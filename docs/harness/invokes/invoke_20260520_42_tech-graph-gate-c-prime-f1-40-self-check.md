# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_prime_f1_audit_R1_20260520.md |
| created_utc_or_local | 2026-05-20 CST |
| git_branch | task/engineering-tech-graph-gate-c-prime-f1-v1 |
| notes | 上一棒 30 · commit `51a1aa3`；主 run `gate_ctx_c_v1_batch_20260518_083014` |

## 可复制 Prompt 快照（40 · 自检）

```text
你正在扮演工作区 Harness「自检帽（40）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（不得代填 HG-GATE-C-PRIME-SIGNOFF approved）

【Git 前提】
- 子仓 ai-ink-brain-api-python：分支 task/engineering-tech-graph-gate-c-prime-f1-v1（基线 commit 51a1aa3 或更新）

【输入】
- 主 task：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md
- 30 帽 invoke：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_41_tech-graph-gate-c-prime-f1-execute.md
- C′ 结论：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md
- 主 run（勿改 052803）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_083014/
- canonical：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/

【开帽前硬检查】
0. 落盘 invoke：invoke_20260520_42_tech-graph-gate-c-prime-f1-40-self-check.md
0b. HG-GATE-C-PRIME-SIGNOFF 仍 pending → 可自检，不可关账 done
1. 独立复跑（不得凭 30 记忆勾选）：
   - python tools/tech_graph_graph_export.py --check
   - python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
   - pytest tests/test_gate_ctx_c_v1_materialize.py
   - pytest tests -m "not intent_eval and not intent_benchmark"
2. 核对 PR-3 产物：
   - run 含 batch_index、round_01..03/raw/*_S0.jsonl、gold_f1.md/json
   - §3.2：T002 D impact ≥0.55 或中位数 ≥0.45；entry 无显著退化；token 中位数 ≤ canonical×1.25
   - 未改 conclusion_gate_c_v2_dual_track_v1_zh.md accepted 正文
3. 更新 task「### 自检结论（执行者）」40 帽小节 + 验收表
4. HANDOFF_AUTO_COMMIT：仅本轮路径；报 short-hash

【禁止】
覆盖 052803；代填 HG-GATE-C-PRIME-SIGNOFF；git add -A
```
