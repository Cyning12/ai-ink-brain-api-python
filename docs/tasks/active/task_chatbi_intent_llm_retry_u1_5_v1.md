# Task：ChatBI Intent LLM 外呼重试（U1.5 · micro-PR）

> **状态**：`active`  
> **Epic**：ChatBI Intent Hints · **U1.5**（独立于 Step1 PR · 不阻塞 Step2 U2）  
> **前置**：Step1 `chatbi_intent_hints_step1_v1` 已开 PR；本单 **不** 含 `intent_hints.yaml`  
> **关联代码**：`api/intent_agent.py` · `api/agent.py`（`decide_intent_v1` import 修复）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `chatbi_intent_llm_retry_u1_5_v1` |
| **semi_auto** | `true` |
| **test_strategy** | `required` |
| **git_branch** | `task/chatbi-intent-llm-retry-u1.5` |

---

## 目标

Intent V2 LLM 外呼在 **瞬态失败**（超时、5xx、限流）时 **最多 3 次**（含首次），耗尽后走现有 **`v1_fallback`**；JSON 非法 / tool 不在白名单 **不重试**。

---

## 交付

| # | 项 | 说明 |
| --- | --- | --- |
| 1 | `CHATBI_V2_INTENT_LLM_RETRIES` | 默认 `3`，上限 5 |
| 2 | `CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S` | 指数退避基数，默认 `0.15` |
| 3 | `_llm_decide_v2_with_retries` | 包装单次 `_llm_decide_v2` |
| 4 | 可观测 | `raw_response.used=llm_retry` + `attempt` + `timeout_s` |
| 5 | 超时阶梯 | 首轮全量；二三轮默认 **65% / 40%**（`CHATBI_V2_INTENT_RETRY_TIMEOUT_FACTORS` 可覆盖） |
| 6 | `api/agent.py` | （Step1 #109 已含 `decide_intent_v1` import · 本 PR 不重复改） |
| 7 | 单测 | `tests/test_intent_llm_retry.py` |
| 8 | RUNBOOK | §4.1 Q-INTENT 补充问（Step1 五问已验 · 不单独落盘） |

---

## 验收

- [ ] `pytest tests/test_intent_llm_retry.py -q`
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark" -q`
- [x] Step1 五问 5/5 人验已通过（#109 · **不**单独 reinspect 落盘）
- [ ] RUNBOOK §4.1 Q-INTENT spot-check（可选 · 与 U1.5 合 PR 说明）

---

## 非范围

- Intent hints YAML / Prompt 注入（Step1）  
- Step2 router 仲裁（U2）  
- 前端 Timeline 专用 retry UX

---

## 修订

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 自 Step1 拆出 micro-PR |
