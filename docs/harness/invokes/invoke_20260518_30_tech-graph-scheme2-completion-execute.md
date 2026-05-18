# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/30-execute-code.md + 用户 §3 执行调用体 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 |
| notes | 开帽前 gate 检查：**HG-TASK-DRAFT**、**HG-AUDIT-R1** 仍为 `pending` → **30 拒开工**（未改业务代码） |
| git_branch | task/engineering-tech-graph-scheme2-completion-v1 |
| outcome | blocked_by_human_gate |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）
- 子仓 AGENTS.md、task 内「给执行帽的必读」、根 AGENTS.md §8

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-scheme2-completion-v1

输入（占位符已替换）：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md
- 子仓根：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md
- 关联 SPEC / 总规：
Projects/docs/tech_graph/改进方向.md
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

开帽前硬检查：
0. 将本消息全文落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_30_tech-graph-scheme2-completion-execute.md（元数据表 + 快照 fenced code）。
0b. 复读 task Harness 表：若 HG-TASK-DRAFT 或 HG-AUDIT-R1 仍为 pending → 仅输出须人改的 gate_id 与路径，拒开工。
1. 通读 task：gates_before_code、§0.4～0.5、§1 范围/非范围（NR-1、禁止重跑闸口 B batch、禁止 Neo4j/schema/workflow/重命名）、§3 验收、§4 failure_paths、§5 必读。
2. test_strategy required：先在 tests/test_tech_graph_graph_query.py 为 has_path、describe_impact 写可失败用例，再实现 tools/tech_graph_graph_query.py + CLI（has-path、describe-impact）；禁止只实现后补测。
3. S2-A：has_path 复用 _bfs_reachable/downstream；未知节点 FP-4；describe_impact 组合 query_downstream/upstream 格式化为 str（非裸 JSON 替代）。
4. S2-B：更新工作区 scheme_2_graph_query.md、改进方向.md §2.3～2.7、子仓 docs/_tech_graph/graph_v2_schema.md §9 工具表；与 §2.1 映射表一致。
5. S2-C（recommended）：C1 MCP 示例或 C2 Harness 模板可选步骤二选一；未做须在 §6/CLOSE 写顺延理由。
6. 禁止：run_gate_b_batch 全 arms；改 .github/workflows；graph_v2 schema 语义变更；tech_graph_graph_query.py 重命名为 graph_query.py。
7. 跑 task §3.3：tech_graph_graph_export.py --check、tech_graph_graph_equivalence_check.py、上述 pytest；回填 task「### 自检结论（执行者）」。
8. 按 HANDOFF_AUTO_COMMIT 仅 commit 本轮路径；对话报 short-hash。

禁止：HG 未 approved 时写业务代码；默认整包 v1 作 query；扩 scope 到闸口实验 / Neo4j / 退役 .ai.md。
```
