# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-gate-c-v2-dual-track-v1 |
| notes | PR-2 P1 batch 独立复验；上一棒 invoke_20260518_30_tech-graph-gate-c-p1-batch.md |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-gate-c-v2-dual-track-v1

输入：
- 主 task 路径（相对工作区根 Projects/）：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md 
- 子仓根（验证命令 cwd）：
ai-ink-brain-api-python
- 主验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 变更范围说明：
git diff 514976e..add8fa8（P1 batch runner + run gate_ctx_c_v1_batch_20260518_052803 + test_gate_ctx_c_v1_batch.py）

开帽前硬检查：
0. 将本消息全文落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_31_tech-graph-gate-c-40-self-check.md（元数据表 + 快照 fenced code）。
0b. 复读 task human_gate：凡 blocks 含 40 且 status=pending → 拒开工并列 gate_id。
1. 通读 task §3（P0/P1/共用）、§6 已有「### 自检结论（执行者）」；**独立复跑**下列命令并摘录退出码/要点（不得凭 30 帽记忆勾选）：
   - pytest tests/test_gate_ctx_c_v1_materialize.py
   - pytest tests/test_gate_ctx_c_v1_batch.py
   - pytest tests -m "not intent_eval and not intent_benchmark"
   - python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
2. 核对 P1 产物（只读、不重跑 LLM 除非 task 要求）：
   - canonical run：docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/
   - 须含 batch_index.json、round_01..03/raw/*_S0.jsonl、index.json、gold_f1.json；dry_run 须为 false
   - 复现命令与 batch README / batch_index.reproduce_commands 一致
3. 输出验收表（pass/fail + 证据）；更新/增补 task「### 自检结论（执行者）」**40 帽**小节（命令、cwd、退出码、P1 §3.2 项结论）。
4. 对话末尾输出 **下一棒可复制 Prompt**（P2 结论报告帽，见 task §0.4/§3.3 P2）。
5. 按 HANDOFF_AUTO_COMMIT 仅 add 本轮路径；对话报 short-hash。

禁止：无命令输出却勾选验收；代填 human_gate；git add -A；重跑 gate_ctx_b_batch / 改 A/B 历史 runs。
```
