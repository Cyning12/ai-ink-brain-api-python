---
task_slug: chatbi_intent_llm_retry_u1_5_v1
round: T1
hat: 22
freeze_id: GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08
git_branch: task/chatbi-intent-llm-retry-u1.5-chain-v1
audit_profile: full
date: 2026-06-08
---

# 22 R1 · Harness 审查

## 审查焦点
- test_strategy: required → 50 不可 skip
- semi_auto → false 迁移确认
- failure_paths Scenario ID F1–F4 与测试映射
- api 范围 bounded（无 scope creep）
- task §行为变更 Delta 清单

## 前置产出
- explore_intent_retry_u1_5_impl_gap.md：实现已存在于 main，测试 6/6 绿
- 代码来源：PR #110 / commit 9a01ebd

## 审查路径
1. task_chatbi_intent_llm_retry_u1_5_v1.md 元信息 + 验收标准
2. api/intent_agent.py：_llm_decide_v2_with_retries + env 读取 + 日志
3. tests/test_intent_llm_retry.py：6 case → F1–F4 覆盖
4. .env.example 注释
