---
task_slug: chatbi_intent_llm_retry_u1_5_v1
round: T1
hat: 30
freeze_id: GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08
git_branch: task/chatbi-intent-llm-retry-u1.5-chain-v1
date: 2026-06-08
---

# 30 · api 实现 · TDD 硬约束（验证性执行）

## 背景
本 task 为"已合代码的 harness 链式补关账"（PR #110 / commit 9a01ebd 已入 main）。
api/intent_agent.py 与 tests/test_intent_llm_retry.py 已完整实现。

## 执行顺序
1. 跑 `pytest tests/test_intent_llm_retry.py -q` 确认绿
2. 检查 `.env.example` U1.5 env 注释完整性
3. 若测试绿且 env 齐全 → 无需改代码
4. 回填 task §自检结论
5. 准备 40 帽全集 pytest 命令

## forbidden
- git commit（由 Lead 执行）
- 扩大 task 非范围
- 改 .github/
