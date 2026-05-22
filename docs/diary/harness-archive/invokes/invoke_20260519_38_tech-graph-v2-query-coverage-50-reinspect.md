# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| template | docs/harness/prompts/TEMPLATE-independent-reinspect-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_query_coverage_v1.md |
| related_review_or_none | 无（`audit_profile: post_close` · 工程 follow-up） |
| created_utc_or_local | 2026-05-19 CST |
| git_branch | task/engineering-tech-graph-v2-query-coverage-v1 |
| notes | 上一棒 40：`invoke_20260519_37_tech-graph-v2-query-coverage-40-self-check.md`；实现 `05c1b39` · 40 落盘 `ab187fa`/`1fcf51c` |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task：ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_query_coverage_v1.md
- 子仓根：ai-ink-brain-api-python
- 模式：独立复检
- diff：git diff main...HEAD（分支 task/engineering-tech-graph-v2-query-coverage-v1；实现 05c1b39 · 40 落盘 ab187fa/1fcf51c）
- 任务审核路径：无

上一节 invoke：docs/harness/invokes/invoke_20260519_37_tech-graph-v2-query-coverage-40-self-check.md

你必须完成：
0. 落盘 invoke 到 docs/harness/invokes/
1. 读取 task「### 自检结论（执行者）」；对照 diff 与 §3 验收项输出 pass/fail 表
2. 汇总阻塞合并项；给出是否建议合并
3. 建议合并且无返工 → HANDOFF_CLOSE_TRACE；须打回 → 下一棒 Prompt + HANDOFF_AUTO_COMMIT
```

## 50 帽复检结论（摘要）

- **自检结论**：已回填（40 · invoke_37）；与独立复跑一致。
- **§3 验收**：PR-1/PR-2/§3.3 **全部 pass**；PR-3 可选未测（非阻塞）。
- **独立复跑**（2026-05-19）：`export --check` 0；materialize 0（T002 17 nodes / 3494 tokens）；focused pytest 31 passed；全量 195 passed。
- **建议合并**：是（无阻塞项）；流程关闭 → `HANDOFF_CLOSE_TRACE`。
