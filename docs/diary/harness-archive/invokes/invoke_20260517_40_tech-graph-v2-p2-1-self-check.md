# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md |
| created_utc_or_local | 2026-05-17（自检帽 P2-1 签收） |
| notes | 上一棒 invoke_20260517_30_tech-graph-v2-p2-1-exec.md；复跑 VERIFY + export --check + equivalence + v2 pytest |

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
  ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p2-1-exec.md
- 合并前 VERIFY：
  pytest tests -m "not intent_eval and not intent_benchmark"
- 审查结论（R2）：
  ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md

你必须完成：
0. 若本消息为「新帽」首条，按 docs/harness/invokes/README.md 将本 Prompt 全文落盘后再开工。
1. 对照 task §4.1 **P2-1 范围**：复跑 VERIFY、`export --check`、`equivalence_check`、v2 专项 pytest；仅勾选有命令证据的项。
2. 确认 `docs/_tech_graph/graph.json` 为 `graph_v2`（非 v1 等价冒充签收）；未引入 graphs[]/ref/kind；未合并 contract 与 graph 导出。
3. 更新 task「### 自检结论（执行者）」；§4.1 中 graph_query / 闸口 B 标 **未测**。
4. 对话回复：若 P2-1 签收 pass，输出 **P2-2 执行帽** Prompt（`graph_query`）；若 fail，输出阻塞清单。

禁止：无命令输出即勾选；把 v1 等价当 v2 通过；扩 scope 至闸口 B。
```
