# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md |
| related_review_or_none | none |
| created_utc_or_local | 2026-05-20 CST |
| git_branch | task/engineering-tech-graph-gate-c-prime-f1-v1 |
| notes | 30 交付后接力；含 C′ batch 与 gold_f1 复跑 |

## 可复制 Prompt 快照（40 · 自检）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task：ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md
- 子仓根：ai-ink-brain-api-python
- 变更范围：git diff main...HEAD（分支 task/engineering-tech-graph-gate-c-prime-f1-v1）
- 上一棒 invoke：docs/harness/invokes/invoke_20260520_41_tech-graph-gate-c-prime-f1-execute.md

主验证命令（按 task §3 增补）：
1. python tools/tech_graph_graph_export.py --check
2. python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
3. pytest tests/test_gate_ctx_c_v1_materialize.py -q
4. pytest tests -m "not intent_eval and not intent_benchmark" -q
5. （若 PR-3 已完成）python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py --batch-dir <新 run 目录>

你必须完成：
0. 落盘 invoke 到 docs/harness/invokes/
1. 逐条运行上述命令；对照 §3.1/§3.2 输出 pass/fail 表（含 F1 相对 §2.1 基线数值）
2. 回填 task「### 自检结论（执行者）」
3. 输出下一棒 50 复检 Prompt + HANDOFF_AUTO_COMMIT（用户未说不要 commit）
4. 禁止无命令输出勾选验收；禁止代填 HG-GATE-C-PRIME-SIGNOFF approved
```
