# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | Projects/docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md |
| prev_exec_invoke | ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p4-exec.md |
| created | 2026-05-17 |
| notes | P2-4a-1 执行后自检；HG 无 40 阻塞 |

## 可复制 Prompt 快照（下一棒 · 自检帽）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入（占位符已替换）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md
- 子仓根（相对 Projects/）：
ai-ink-brain-api-python
- 主验证命令（与 CI / task 一致）：
pytest tests -m "not intent_eval and not intent_benchmark"
- 变更范围说明（无则写「无」）：
P2-4a-1：tech_graph_graph_v2_schema.py kind；test_tech_graph_graph_v2_p4_schema.py；freeze V2_1；graph_v2_schema.md v0.2

你必须完成：
0. Invoke 快照：本消息已落盘 invoke_20260517_40_tech-graph-v2-p4-a1-self-check.md 后可开工。
1. 通读 task §3 验收与「### 自检结论（执行者）」；逐条运行：
   - pytest tests -m "not intent_eval and not intent_benchmark"
   - python tools/tech_graph_graph_export.py --check
   - python tools/tech_graph_graph_equivalence_check.py
   - pytest tests/test_tech_graph_graph_query.py tests/test_tech_graph_graph_v2_p4_schema.py -q
2. 输出验收表（pass/fail + 证据）。
3. 更新或确认 task「### 自检结论（执行者）」与 §3 勾选一致。
4. 对话输出下一棒：30 执行帽 P2-4a-2（graphs[]+ref）可复制 Prompt，或说明关账前仍缺 4a-2。
5. 按 HANDOFF_AUTO_COMMIT 提交本轮变更。
```
