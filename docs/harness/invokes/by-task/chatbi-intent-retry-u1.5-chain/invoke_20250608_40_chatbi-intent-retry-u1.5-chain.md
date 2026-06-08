---
task_slug: chatbi_intent_llm_retry_u1_5_v1
round: T1
hat: 40
freeze_id: GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08
git_branch: task/chatbi-intent-llm-retry-u1.5-chain-v1
date: 2026-06-08
---

# 40 · 自检

## 必须
- pytest tests -m "not intent_eval and not intent_benchmark"（全绿 · 贴摘要）
- python tools/harness_task_validate.py docs/tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md → OK
- task 验收项勾选证据

## 前置状态
- 30 帽：tests/test_intent_llm_retry.py 6 passed
- 22 R1：签收，无阻塞
- task 自检结论已回填
