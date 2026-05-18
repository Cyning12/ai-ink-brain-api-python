# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| template | docs/harness/prompts/TEMPLATE-task-audit-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md |
| related_review_or_none | 无 |
| created_utc_or_local | 2026-05-20 CST |
| git_branch | task/engineering-tech-graph-gate-c-prime-f1-v1（待 30 创建） |
| notes | 闸口 C′ · F1 优先；post_close · HG-TASK-DRAFT 已 approved |

## 可复制 Prompt 快照（22 · R1 任务审核）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/22-task-audit.md
- docs/harness/reviews/README.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入：
- 待审 task（相对 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md
- 关联 SPEC / 总规：
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
Projects/docs/tech_graph/改进方向.md
- 上一轮审查：无

落盘建议名：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_prime_f1_audit_R1_20260520.md

你必须完成：
0. 落盘 invoke 到 docs/harness/invokes/（若尚未存在本快照则跳过重复）
1. 通读 task §0～§4；核对 test_strategy: required、failure_paths、F1/token/C′ 分期与 NR。
2. 对照 canonical 基线表（§2.1）与 §3.2 验收阈值是否可观测、可复现。
3. 落盘审查 md；元信息含 invoke_snapshot 指向本 invoke。
4. 结论：是否建议 30 开工；若有阻塞写入「需任务帽回填清单」。
5. 有下一棒 → 输出 30 执行 Prompt（可链 invoke_20260520_41）；无阻塞则签收节 + HANDOFF_AUTO_COMMIT。
6. 禁止写业务代码；禁止代填 HG-GATE-C-PRIME-SIGNOFF approved。

审查关注点（本 task 特有）：
- PR-3 新 run 目录 vs NR-1 不覆盖 052803
- F1 优先序 vs PR-2 token 守门触发条件
- 不推翻闸口 C accepted、不升 CTX_DUAL_MD 默认
```
