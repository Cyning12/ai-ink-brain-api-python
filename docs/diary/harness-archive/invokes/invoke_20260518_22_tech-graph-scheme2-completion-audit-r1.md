# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| template | Projects/docs/harness/prompts/TEMPLATE-task-audit-invoke.md §3（用户自定义审查清单） |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md |
| related_review_or_none | 无（首轮 R1） |
| created_utc_or_local | 2026-05-18 |
| notes | 方案2 补全 v0.2 · post_close · test_strategy required |
| git_branch | task/engineering-tech-graph-scheme2-completion-v1 |
| next_hat | 30（须 HG-TASK-DRAFT + HG-AUDIT-R1 approved 后） |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/22-task-audit.md（身份、禁止项、输出形状、交接物）
- docs/harness/reviews/README.md（文件命名、R1/R2 闭环）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、human_gate）
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（不得代填 HG-* approved）

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-scheme2-completion-v1

【待审 task】
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md
（元信息：v0.2 · semi_auto · post_close · test_strategy: required）

【关联 SPEC / 总规】
Projects/docs/tech_graph/改进方向.md（§方案2 · §2.3～2.7）
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

【上一轮审查】
无（首轮 R1）

【对照材料（只读）】
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md
ai-ink-brain-api-python/tools/tech_graph_graph_query.py
ai-ink-brain-api-python/tests/test_tech_graph_graph_query.py
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_10_tech-graph-scheme2-completion-requirements.md

【落盘建议名】
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md

【R1 重点核对清单】
1. §0.4 矛盾裁定（C-1～C-5）是否可执行、是否与 §1.2 非范围一致
2. §0.5：`has_path` / `describe_impact` 锁定是否合理；`get_all_affected` 非范围是否充分
3. §3 验收是否可观测、可命令断言；`test_strategy: required` 是否写明先测后实现
4. §4 failure_paths 是否覆盖 FP-4/FP-5 与 scope 误用（NR-1 / batch）
5. human_gate：`HG-TASK-DRAFT` 仍 pending 时，是否 **仅** 输出审查结论、**不** 指示 30 开工
6. 禁止项：闸口 B 重跑、Neo4j、schema 语义变更、改 workflow、重命名模块

你必须完成：
0. Invoke 快照：先将本消息全文落盘 docs/harness/invokes/invoke_20260518_22_tech-graph-scheme2-completion-audit-r1.md；审查 md 元信息填 invoke_snapshot
1. 通读 task v0.2 全文及 Harness 元信息表
2. 对照 HARNESS_V2_PLAN.md §5 检查验收、failure_paths、test_strategy
3. 落盘审查文档至上述 reviews 路径
4. 文内结构：元信息 → 结论摘要 → 阻塞/非阻塞 → 需需求帽回填清单（若有）→ 是否建议执行帽开工 → 签收
5. 禁止写业务代码；禁止擅自改 task 正文；禁止将 HG-TASK-DRAFT / HG-AUDIT-R1 改为 approved
6. 对话末尾输出「下一棒可复制 Prompt」：若零硬阻塞且 **须人先批准 HG-TASK-DRAFT + HG-AUDIT-R1** 后再 30，则给出 TEMPLATE-execute-invoke 风格执行帽 Prompt；若有阻塞则给需求帽回填 Prompt
7. 按 HANDOFF_AUTO_COMMIT 仅 commit 本轮 invoke + reviews（用户写明不要 commit 则跳过）

【禁止】
写业务实现；改 CI；扩 scope 到闸口实验 / Neo4j / 退役 .ai.md
```
