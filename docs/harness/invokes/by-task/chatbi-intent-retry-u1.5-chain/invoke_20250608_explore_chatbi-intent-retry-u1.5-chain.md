---
task_slug: chatbi_intent_llm_retry_u1_5_v1
round: T1
hat: explore
freeze_id: GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08
git_branch: task/chatbi-intent-llm-retry-u1.5-chain-v1
date: 2026-06-08
---

# explore · B 轨 · api 差分

## 输入
- task: docs/tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md
- api/intent_agent.py（重试/超时相关段落）
- tests/test_intent_llm_retry.py
- task §行为变更 · failure_paths F1–F4

## 发现

### 实现状态
- `_llm_decide_v2_with_retries` 已在 `api/intent_agent.py:513-561` 实现
- env 读取：`CHATBI_V2_INTENT_LLM_RETRIES`、`CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S`、`CHATBI_V2_INTENT_RETRY_TIMEOUT_FACTORS`
- timeout 阶梯：`_intent_llm_timeout_s_for_attempt` 按系数递减
- 可观测：`used=llm_retry` + `attempt` + `timeout_s`
- 日志：`_log_intent_retry_*` 三套

### 测试状态
- `tests/test_intent_llm_retry.py` 已存在，6 个 test：
  - `test_intent_llm_retry_succeeds_on_third_attempt` → F3
  - `test_intent_llm_retry_exhausted_falls_back_v1` → F1
  - `test_intent_llm_json_error_not_retried` → F2
  - `test_intent_llm_retry_timeout_decreases_per_attempt` → F4
  - `test_intent_llm_retry_logs_without_debug_intent_cache`
  - `test_intent_llm_retryable_classifier`

### 缺口
- `.env.example` U1.5 retry / timeout factors 注释（task §行为变更 ADDED）
- task 验收标准 §自检结论待回填

## 30 TDD 顺序建议
1. 先补 `.env.example` 注释
2. 跑 `pytest tests/test_intent_llm_retry.py -q` 确认绿
3. 改 `api/intent_agent.py` 若有 gap（当前目测无）
4. 全集 pytest
