# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/40-self-check.md |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_query_coverage_v1.md |
| related_review_or_none | none（工程 follow-up · 继承闸口 C R1 范围） |
| created_utc_or_local | 2026-05-19 CST |
| git_branch | task/engineering-tech-graph-v2-query-coverage-v1 |
| notes | 30 交付 commit 05c1b39；上一棒 invoke_20260519_36_tech-graph-v2-query-coverage-execute.md |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 主 task：ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_query_coverage_v1.md
- 子仓根：ai-ink-brain-api-python
- 主验证命令：pytest tests -m "not intent_eval and not intent_benchmark"
- 变更范围：git diff main...HEAD（分支 task/engineering-tech-graph-v2-query-coverage-v1，commit 05c1b39）

你必须完成：
0. 落盘 invoke 快照到 docs/harness/invokes/
1. 逐条运行 task §3 验证命令：
   - python tools/tech_graph_graph_export.py --check
   - python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
   - pytest tests/test_gate_ctx_c_v1_materialize.py tests/test_tech_graph_graph_export.py tests/test_tech_graph_graph_query.py
   - pytest tests -m "not intent_eval and not intent_benchmark"
2. 输出验收 pass/fail 表
3. 回填 task「### 自检结论（执行者）」
4. 按 HANDOFF_AUTO_COMMIT 分仓 commit（用户未说「不要 commit」）

禁止：无命令输出却勾选验收；代填 human_gate；git add -A；重跑闸口 A/B/C 主 batch。
```
