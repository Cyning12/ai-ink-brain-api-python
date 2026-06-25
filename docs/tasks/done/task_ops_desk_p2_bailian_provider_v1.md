# Task · Ops Desk P2-5c · 百炼 Provider（后端子仓）

> **状态**：`done` · human CLOSE pass 2026-06-25  
> **协调 task**：Projects [`task_ops_desk_p2_bailian_provider_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p2_bailian_provider_v1.md)  
> **invoke**：[`PROMPT_CHAIN_30_40_50_CLOSE_v1.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-bailian-provider/PROMPT_CHAIN_30_40_50_CLOSE_v1.md)  
> **PR**：[#212](https://github.com/Cyning12/ai-ink-brain-api-python/pull/212) · `8c2c25b3`

---

## 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-bailian-provider` |
| **test_strategy** | `required` |
| **human_gate** | run `33d484ea-92ff-4d1f-a1a8-b8e0303fdcd0` · D4 bailian · tt=1855 |

---

## 交付清单

- [x] `BailianProvider.complete()` · OpenAI 兼容 Chat
- [x] env `BAILIAN_*` · 与 RAG embedding 分离
- [x] 缺 key → 503 `LLM_PROVIDER_MISCONFIGURED`
- [x] `llm.usage` ×2 · `metrics_json.llm.provider=bailian`
- [x] `openai_compatible_complete` 共用 helper
- [x] pytest · PROJECT_CONFIG · `.env.example`

---

## 下一棒

P2-5f LLM model fallback · Projects [`task_ops_desk_p2_llm_model_fallback_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_llm_model_fallback_v1.md)
