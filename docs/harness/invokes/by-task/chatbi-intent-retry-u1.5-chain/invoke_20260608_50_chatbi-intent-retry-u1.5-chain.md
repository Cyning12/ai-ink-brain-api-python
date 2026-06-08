---
task_slug: chatbi_intent_llm_retry_u1_5_v1
round: T1
hat: 50
freeze_id: GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08
git_branch: task/chatbi-intent-llm-retry-u1.5-chain-v1
date: 2026-06-08
---

# 50 · 独立复检 · required 不可 skip

## 读序
1. docs/tasks/done/task_chatbi_intent_llm_retry_u1_5_v1.md
2. 40 证据：pytest 323 passed + task_validate OK
3. api/intent_agent.py：_llm_decide_v2_with_retries
4. tests/test_intent_llm_retry.py
5. 22 R1 审查报告

## 审查焦点
- 重试阶梯：3 次（含首次），上限 5
- 超时递减：系数 1.0/0.65/0.4
- failure_paths F1–F4 与测试映射
- 无 scope creep

## 交付
- docs/tasks/reinspect_results/reinspect_chatbi_intent_llm_retry_u1_5_20260608_v1.md
