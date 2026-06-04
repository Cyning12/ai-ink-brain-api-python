# Invoke · 10 需求帽 · chatbi_baseline_merge_gate_v1 · 2026-06-04

| 字段 | 值 |
| --- | --- |
| **hat_code** | 10 |
| **task_slug** | `chatbi_baseline_merge_gate_v1` |
| **git_branch** | `task/chatbi-baseline-merge-gate-v1` |
| **semi_auto** | `true` |
| **test_strategy** | `required` |
| **audit_profile** | `post_close` |
| **SDD 状态** | 不涉及新 SPEC（§3 省略） |
| **NEW_OR_MAJOR_SPEC** | 否 |
| **audit_review** | 无 |
| **blocks** | `chatbi_graph_p0_foundation_v1` |
| **交付** | `docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md` |

## §3 快照（开帽 Prompt 全文）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md

输入：

【目标与上下文】
维护者决策 **选 B**（见 50 复检 `reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md`）：在合入 P0 Graph PR 之前，**先**在独立分支修复 **origin/main 既有** 的合并阻塞项，使 AGENTS §8 全集 pytest + `tech_graph_contract_check` 变绿。

阻塞 P0 合入的两类红项（main 与 `task/chatbi-graph-p0-foundation-v1` 同型，**非 P0 引入**）：
1. **10× pytest fail** — `tests/test_unified_chat_backend_v2_agent.py` 内 v3 plan/clarify 相关：
   - test_v3_low_confidence_clarify_json_skips_text2sql
   - test_v3_plan_preview_json_includes_plan_preview_and_ttl_notice
   - test_v3_plan_execution_token_json_bypasses_clarify
   - test_v3_plan_execution_token_invalid_json_denies_bypass
   - test_v3_plan_preview_fail_json_no_token
   - test_v3_plan_preview_sse_parity
   - test_v3_rag_plan_preview_json_includes_rewrite_query
   - test_v3_rag_plan_execution_token_json_bypasses_clarify
   - test_v3_rag_plan_preview_fail_json_no_token
   - test_v3_rag_plan_preview_sse_parity
   （典型断言：`'agent.plan.preview' not in events` 等）
2. **contract_check fail** — `python tools/tech_graph_contract_check.py` → `contract.frontend_anchors.sse_consumer_files` · 字段 **`label`** 未声明（main 已红）

**合并策略（task 须写清）**：
- 本 task **独立 PR → main**（基线修复）；**禁止**夹带 P0 Graph 五步（`chatbi_events` / graph 路由等）。
- P0 task `chatbi_graph_p0_foundation_v1` **blocked_by** 本 task；本 task **blocks** P0 合 main。
- P0 分支 `task/chatbi-graph-p0-foundation-v1` 在本 PR 合入 main 后 **rebase** 再开 PR。

建议 task_slug：`chatbi_baseline_merge_gate_v1` · 分支 `task/chatbi-baseline-merge-gate-v1` · 从 **最新 origin/main** 拉出。

【已有材料路径】
ai-ink-brain-api-python/docs/tasks/reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md
ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md
ai-ink-brain-api-python/tests/test_unified_chat_backend_v2_agent.py
ai-ink-brain-api-python/docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md
ai-ink-brain-api-python/docs/_tech_graph/_contract_manifest.json

【是否按任务审核文档回填】
无

【SDD 三轮状态】
不涉及新 SPEC（§3 省略）

【是否新建或重大修订 SPEC】
否

你必须完成：
0. Invoke 快照落盘 `docs/harness/invokes/by-task/chatbi_baseline_merge_gate_v1/invoke_YYYYMMDD_10_chatbi-baseline-merge-gate.md`
1. 在 `docs/tasks/active/` 新建 `task_chatbi_baseline_merge_gate_v1.md`（Harness 元信息齐全；`test_strategy: required`；`audit_profile: post_close`；`blocked_by`/`blocks` 链 P0；**非范围** 明确排除 P0 Graph 交付物）。
2. 验收须含：`pytest tests -m "not intent_eval and not intent_benchmark"` 全绿 · `tech_graph_contract_check` 全绿 · PR pytest workflow 全绿（表述写入验收标准）。
3. failure_paths ≥1 表行 + Scenario ID；`## 失败路径` / `## 验收标准` 标题精确（validate 可扫）。
4. 若 contract 修复触达 `_contract_manifest` / `.ai.md`，task §行为变更 Delta 须 ADDED/MODIFIED。
5. 输出下一棒 **A（22 R1，推荐）** 与 **B（30 跳过 22）** 两条完整 Prompt；推荐 **A**（涉 api/ + required）。
6. 状态栏 + 按 HANDOFF_AUTO_COMMIT 仅 commit 本轮 task/invoke。
禁止：写业务实现代码；把 P0 graph 路由/manifest 纳入本 task 范围。
```
