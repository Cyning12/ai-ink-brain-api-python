# Invoke · 30 执行帽 · chatbi_intent_hints_step1_v1 · 2026-06-04

| 字段 | 值 |
| --- | --- |
| **hat_code** | 30 |
| **task_slug** | `chatbi_intent_hints_step1_v1` |
| **task_path** | `docs/tasks/active/task_chatbi_intent_hints_step1_v1.md` |
| **git_branch** | `task/chatbi-intent-hints-step1-v1` |
| **audit_review** | `docs/harness/reviews/task_chatbi_intent_hints_step1_v1_audit_R1_20260604.md` |
| **human_gate** | HG-TASK-DRAFT + HG-AUDIT-R1 approved |
| **semi_auto** | true → 40 链式（无 gate 阻塞） |

## §3 快照（30 开帽 · 摘要）

执行 Step1 C-lite：intent_hints.yaml + api/intent_hints.py + intent_agent Prompt 注入 + 测试 + PROJECT_CONFIG。

VERIFY: `pytest tests -m "not intent_eval and not intent_benchmark"`
