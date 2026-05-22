# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md |
| created_utc_or_local | 2026-05-17（自检帽 P2-2 签收） |
| notes | 上一棒 invoke_20260517_30_tech-graph-v2-p2-2-exec.md |

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
  ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p2-2-exec.md
- 合并前 VERIFY：
  pytest tests -m "not intent_eval and not intent_benchmark"
- 审查结论（R2）：
  ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md

你必须完成：
0. 若本消息为「新帽」首条，按 docs/harness/invokes/README.md 将本 Prompt 全文落盘后再开工。
1. 对照 task §4.1 **P2-2 / graph_query**：复跑 VERIFY、`pytest tests/test_tech_graph_graph_query.py -q`、`python tools/tech_graph_graph_query.py downstream AUTH 2`（及 FP-4：`downstream __UNKNOWN__ 1` 期望退出码 4）；仅勾选有命令证据的项。
2. 确认：无 v1 静默降级（FP-5 测试/行为）；`10-tech-graph.mdc` query 优先；未合并 contract 与 graph 导出。
3. 更新 task「### 自检结论（执行者）」；§4.1 **闸口 B** 仍标 **未测**（P2-3）。
4. 对话回复：若 P2-2 签收 pass，输出 **P2-3 执行帽** Prompt（闸口 B）；若 fail，输出阻塞清单打回执行帽。

禁止：无命令输出即勾选；把 v1 整包当 query 默认；扩 scope 至闸口 B 实验实现（仅验收 query 工程项）。
```
