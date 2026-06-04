# Invoke · 22 任务审核 R1 · chatbi_intent_hints_step2_v1 · 2026-06-04

| 字段 | 值 |
| --- | --- |
| **hat_code** | 22 |
| **round** | R1 |
| **task_slug** | `chatbi_intent_hints_step2_v1` |
| **task_path** | `docs/tasks/active/task_chatbi_intent_hints_step2_v1.md` |
| **git_branch** | `task/chatbi-intent-hints-step2-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **audit_round** | R1 |
| **review_path** | `docs/harness/reviews/by-task/chatbi_intent_hints_step2_v1/task_chatbi_intent_hints_step2_v1_audit_R1_20260604.md` |

## §3 快照（22 开帽 Prompt 全文 · 可复制）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/hats/22-task-audit.md（身份、禁止项、输出形状、交接物）
- docs/harness/reviews/README.md（文件命名、R1/R2 闭环）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths 等与 task 字段对齐）

输入（已由人工替换占位符；若你仍看到 {{…}} 或本段「待填」字样，须先追问用户，不得开工）：
- 待审 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_intent_hints_step2_v1.md
- 关联 SPEC / 总规路径（无则写「无」）：
ai-ink-brain-api-python/docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md
ai-ink-brain-api-python/docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md
ai-ink-brain-api-python/docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md
- 上一轮审查文档路径（首轮写「无」；复审必填）：
无

落盘文件建议名（须与文内元信息一致）：
ai-ink-brain-api-python/docs/harness/reviews/by-task/chatbi_intent_hints_step2_v1/task_chatbi_intent_hints_step2_v1_audit_R1_20260604.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文** 落盘到 docs/harness/invokes/by-task/chatbi_intent_hints_step2_v1/（含元数据表 + 快照 fenced code）。审查 md 文首元信息表增加 invoke_snapshot 指向该 invoke。
1. 通读待审 task 全文及头部元信息（状态、freeze_id、gates_before_code、test_strategy、failure_paths、验收、必读链接）。
2. 对照 HARNESS_V2_PLAN.md §5 检查验收可观测性、required 与可失败自动化测试说明。
3. 落盘一篇审查文档至上述 by-task 路径。
4. 文内结构：元信息 → 审查结论摘要 → 阻塞 / 非阻塞 → 需任务帽回填清单（若有）→ 是否建议执行帽开工 → 「签收 / 关闭」→ 下一棒可复制 Prompt（30 执行 §3 全文，若零阻塞）。
5. 禁止仅在对话里说「过了」而不写 reviews；禁止在仍有阻塞时指示执行帽开工。
6. Fresh Context（P1）：新对话开帽；禁止要求阅读 30 invoke 全文。
7. 不要写业务实现代码；不要擅自改写 task 正文。
8. 自动 commit：完成落盘后按 HANDOFF_AUTO_COMMIT.md commit（仅本轮路径）。
```
