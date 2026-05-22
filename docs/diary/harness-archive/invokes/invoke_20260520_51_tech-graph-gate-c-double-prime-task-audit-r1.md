# Harness invoke snapshot · 闸口 C″ 任务审核 R1

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| template | `Projects/docs/harness/prompts/TEMPLATE-task-audit-invoke.md` §3 |
| task_paths | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_double_prime_v1.md` |
| related_review_or_none | 无（首轮 R1） |
| created_utc_or_local | 2026-05-20 CST |
| notes | 落盘审查：`task_engineering_tech_graph_gate_c_double_prime_v1_audit_R1_20260520.md` |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/22-task-audit.md（身份、禁止项、输出形状、交接物）
- docs/harness/reviews/README.md（文件命名、R1/R2 闭环）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths 等与 task 字段对齐）

输入（已由人工替换占位符；若你仍看到 {{…}} 或本段「待填」字样，须先追问用户，不得开工）：
- 待审 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_double_prime_v1.md
- 关联 SPEC / 总规路径（无则写「无」）：
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
Projects/docs/tech_graph/改进方向.md
- 上一轮审查文档路径（首轮写「无」；复审必填）：
无

落盘文件建议名（须与文内元信息一致）：
- ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_double_prime_v1_audit_R1_20260520.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文** 按 docs/harness/invokes/README.md 落盘到 ai-ink-brain-api-python/docs/harness/invokes/（含元数据表 + 快照 fenced code）。落盘审查 md 时须在文首元信息表增加 **invoke_snapshot** 指向该 invoke 文件（相对 Projects/）。同一会话内追问 **不** 再新增快照文件。
1. 通读待审 task 全文及头部元信息（状态、freeze_id、gates_before_code、test_strategy、failure_paths、验收、必读链接）。
2. 对照 HARNESS_V2_PLAN.md §5 检查验收可观测性、required 与可失败自动化测试说明。
3. 重点审查：
   - P0/P1/P-禁止 是否与 C/C′ accepted 结论一致（不推翻 CTX_V2_QUERY 默认）
   - PR-1 T003 物化是否可执行、T002「继承 C′」是否写清避免重复争论
   - §3.2 主 KPI（OR）与 T002 守卫是否可量化、基线表是否引用 052803 + 083014
   - PR-4 / NR-9 是否与 HG-GATE-C-DOUBLE-PRIME-SIGNOFF 阻塞关系一致
   - failure_paths FP-CDP1～8 是否可操作
4. 落盘一篇审查文档至 **上表路径**（与 reviews/README.md、22-task-audit.md 子仓规则一致）。
5. 文内结构：元信息 → 审查结论摘要 → 阻塞 / 非阻塞 → 需任务帽回填清单（若有）→ 是否建议执行帽开工 → 「签收 / 关闭」→ 收尾二选一：**有下一棒** → **「下一棒可复制 Prompt」**；**终轮无下一棒** → **「执行路线与 Commit 回溯」**（HANDOFF_CLOSE_TRACE.md）。
6. 禁止仅在对话里说「过了」而不写 reviews；禁止在仍有阻塞时指示执行帽开工。
7. 不要写业务实现代码；不要擅自改写 task 正文。
8. 完成步骤 3–7 后，按 HANDOFF_AUTO_COMMIT.md 在相关 git 根分别 commit（仅本轮路径）；用户写明「不要 commit」则跳过。

审查时可只读对照（勿改 accepted 正文）：
- docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md
- docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
- docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/gold_f1.md
- docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_083014/gold_f1.md
- docs/harness/invokes/invoke_20260520_50_tech-graph-gate-c-double-prime-requirements.md
```
