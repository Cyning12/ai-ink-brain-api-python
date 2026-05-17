# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md |
| prev_exec | invoke_20260517_30_tech-graph-v2-p4-a2-exec.md |
| created | 2026-05-17 |

## 可复制 Prompt 快照（自检帽 · P2-4a-2 复核）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循 docs/harness/prompts/40-self-check.md。

输入：
- task：ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md
- 子仓：ai-ink-brain-api-python
- VERIFY：pytest tests -m "not intent_eval and not intent_benchmark"
- 变更：P2-4a-2 graphs[]/ref/graph_id 导出 · freeze V2_2

须逐条跑 export --check、equivalence、P2-4 pytest、graph_query；确认 task §3 P2-4a 勾选与自检表一致。
```
