# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| template | docs/harness/prompts/TEMPLATE-self-check-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md |
| prev_invoke | ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_30_tech-graph-scheme2-completion-execute.md |
| created_utc_or_local | 2026-05-18 |
| git_branch | task/engineering-tech-graph-scheme2-completion-v1 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/40-self-check.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 的 test_strategy 等一致）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md
- 子仓根（相对 Projects/；运行验证命令的 cwd）：
ai-ink-brain-api-python
- 主验证命令（与 CI / task 一致；task 另有命令须一并执行并在结论中分列）：
pytest tests -m "not intent_eval and not intent_benchmark"
- 变更范围说明（无则写「无」）：
git diff origin/main...HEAD（子仓 task/engineering-tech-graph-scheme2-completion-v1）；工作区 main 含 docs/tech_graph 与 harness 模板

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文** 落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_40_tech-graph-scheme2-completion-self-check.md（元数据表 + 快照 fenced code）。
1. 通读 task §3 验收；逐条运行：
   - pytest tests/test_tech_graph_graph_query.py -q
   - python tools/tech_graph_graph_export.py --check
   - python tools/tech_graph_graph_equivalence_check.py
   - pytest tests -m "not intent_eval and not intent_benchmark" -q
   cwd=ai-ink-brain-api-python；对话给出退出码与关键摘要。
2. 输出验收表（pass/fail + 证据）。
3. 更新 task「### 自检结论（执行者）」：命令、退出码、验收摘要、已知未测项、自检时间。
4. 禁止凭记忆勾选；不把独立复检走查塞入本帽。
5. 按 HANDOFF_AUTO_COMMIT 仅 commit 本轮路径；用户要求 push 则 push 对应分支。
```
