# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_prime_f1_audit_R1_20260520.md |
| created_utc_or_local | 2026-05-20 CST |
| git_branch | task/engineering-tech-graph-gate-c-prime-f1-v1 |
| notes | 优先级：impact F1 → token → 闸口 C′ batch；freeze TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0 |

## 可复制 Prompt 快照（30 · 执行编码）

```text
你正在扮演工作区 Harness「执行编码帽（30）」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
- 子仓 ai-ink-brain-api-python：从 main 新建分支 task/engineering-tech-graph-gate-c-prime-f1-v1
- 工作区根 Projects/：本 task 默认不改 docs/tech_graph/ 除非 C′ 结论需索引一行且人签

【输入】
- 主 task：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md
- 任务审核（若已落盘，否则先自证已读 task）：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_prime_f1_audit_R1_20260520.md
- 闸口 C canonical（只读 · 基线 F1）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/gold_f1.md
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
- query coverage（已合 main · 物化起点）：
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_query_coverage_v1.md
- 方案2 SPEC：
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
- 物化 / batch / 评分：
fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py
fixtures/gate_ctx_c_v1/query_seeds.json
fixtures/gate_ctx_c_v1/protocol_version.yaml
fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py
fixtures/gate_ctx_ab_v1/tasks.json
- 子仓根：ai-ink-brain-api-python
- 合并前验证：
pytest tests -m "not intent_eval and not intent_benchmark"

【开帽前硬检查】
0. 落盘 invoke：docs/harness/invokes/invoke_20260520_41_tech-graph-gate-c-prime-f1-execute.md
0b. human_gate：HG-TASK-DRAFT、HG-AUDIT-R1（若 task 表有）须 approved；HG-GATE-C-PRIME-SIGNOFF 仍 pending（不阻塞 30）。
1. 通读 task §0.2 优先级：**先 F1 物化，再 token，再 C′ batch**。
2. 自 main 检出分支 task/engineering-tech-graph-gate-c-prime-f1-v1。

【范围 · 按 task §1.3】

PR-1（F1 导向 · D 臂物化）— 主 KPI：
- T002：强化 contract_slice（按 tasks.json gold impact 补 SSE/unified chat 契约段；_contract_manifest.json 定向切片）
- T001/T003：按需 manifest 切片；无收益则保持现状
- 可选：单题试验 describe-impact 与 JSON 子图并列（须 pytest + token 门禁）
- bump/写入本 task freeze_id：TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0（protocol/query_seeds 指针）
- 命令绿：
  python tools/tech_graph_graph_export.py --check
  python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
  pytest tests/test_gate_ctx_c_v1_materialize.py

PR-2（仅 PR-1 超 token 限时）：
- 收缩顺序：裁 slice 字段 → 减 depth → 最后减 union 臂
- 记录 F1/token 前后表；仍须 <8192 且 <5026 mermaid 基线

PR-3（闸口 C′ batch）— 在 PR-1/2 完成后：
- 新目录 runs/gate_ctx_c_v1_batch_<YYYYMMDD>_*（禁止改 052803）
- materialize → run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD
- score_gold_f1.py → gold_f1.md/json
- 结论：docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md
  · 相对 §2.1 canonical 的 Δimpact/Δentry/Δtokens
  · 验收：impact 中位数≥0.45 或 T002 D≥0.55；entry 无显著退化；token ≤ canonical D×1.25
  · 产品：维持 CTX_V2_QUERY 默认（除非数据强烈反对且写变更请求）

【禁止】
NR-1～7：不覆盖 052803；不重跑 A/B 主 batch；不改 gate_c accepted 正文
不升 CTX_DUAL_MD 默认；不整包 15_e2e / graph.json
git add -A

【交付】
1. 回填 task §6 +「### 自检结论（执行者）」30 帽摘要
2. 输出下一棒 40 自检 Prompt（ branding invoke_20260520_42 ）
3. HANDOFF_AUTO_COMMIT：仅本轮路径；报 short-hash
```
