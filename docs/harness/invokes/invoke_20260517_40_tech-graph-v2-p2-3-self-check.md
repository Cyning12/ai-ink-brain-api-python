# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md |
| created_utc_or_local | 2026-05-17（自检帽 P2-3 闸口 B 证据核对） |
| notes | 上一棒 invoke_20260517_30_tech-graph-v2-p2-3-gate-b-exec.md；HG-P2-3-GATE-B 仍 pending |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/prompts/TEMPLATE-self-check-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task（相对 Projects/）：
  ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md
- 子仓根：ai-ink-brain-api-python
- 上一棒 invoke 快照：
  ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p2-3-gate-b-exec.md
- 闸口 B 报告：
  ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
- batch run：
  ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_b_v1_batch_20260517_095228/
- 合并前 VERIFY：
  pytest tests -m "not intent_eval and not intent_benchmark"

你必须完成：
0. 若本消息为「新帽」首条，按 docs/harness/invokes/README.md 将本 Prompt 全文落盘后再开工。
1. 复跑 VERIFY；核对 materialize_report（CTX_QUERY 非整包 v2）与 batch 内 3× parse_ok、gold_f1.md。
2. 对照 task §4.2 / §4.3 与报告 §3–§5：仅在有证据项勾选；§4.3 B-1「部分满足」须保留说明。
3. 更新 task「### 自检结论（执行者）」为 P2-3 自检签收；**不得**将 HG-P2-3-GATE-B 改为 approved。
4. 若 pass：输出关账前 Prompt（HANDOFF_CLOSE_TRACE 或终轮审查）；若 fail：打回执行帽并列阻塞项。

禁止：无命令输出即勾选；代填 HG-P2-3-GATE-B；把 v1 整包当作 CTX_QUERY 默认。
```
