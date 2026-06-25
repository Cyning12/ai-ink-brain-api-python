# Task · Ops Desk P2-5c · 百炼 Provider（后端子仓）

> **状态**：`done` · human CLOSE pass 2026-06-25  
> **协调 task**：Projects [`task_ops_desk_p2_bailian_provider_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p2_bailian_provider_v1.md)  
> **invoke**：[`PROMPT_CHAIN_30_40_50_CLOSE_v1.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-bailian-provider/PROMPT_CHAIN_30_40_50_CLOSE_v1.md)  
> **PR**：[#212](https://github.com/Cyning12/ai-ink-brain-api-python/pull/212) · `8c2c25b3`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-bailian-provider` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-BAILIAN-PROVIDER` |
| **git_branch** | `task/ops-desk-p2-bailian-provider` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **human_gate** | run `33d484ea` · D4 bailian · tt=1855 |

---

## 背景与目标

实现 `BailianProvider.complete()` · OpenAI 兼容 `POST …/chat/completions` · `OPS_LLM_PROVIDER=bailian` 可生产切换。

---

## 范围 / 非范围

| 范围 | 非范围 |
| --- | --- |
| `api/ops/llm/providers/bailian.py` · OpenAI 兼容 Chat | DashScope 原生 SDK · Responses API |
| env `BAILIAN_*`（与 RAG `DASHSCOPE_EMBEDDING_*` 分离） | SiliconFlow 自动换模（P2-5f） |
| 缺 key → 503 `LLM_PROVIDER_MISCONFIGURED` | 前端 Provider UI（本 PR 外） |
| `llm.usage` · `metrics_json.llm.provider=bailian` | H4 Provider KV（#211 独立） |

---

## 行为变更（Delta）

### ADDED

- **Requirement**：百炼 OpenAI 兼容 Chat Provider
  - **Scenario**：`bailian-chat-complete` — GIVEN `OPS_LLM_PROVIDER=bailian` WHEN D4 deep THEN 2× `llm.usage` · `provider=bailian`

### MODIFIED

- **Requirement**：`SiliconFlowProvider` 共用 `openai_compatible_complete` helper（行为不变）

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- | --- | --- |
| F1 | `fp-bailian-misconfigured` | 缺 `BAILIAN_API_KEY` / `DASHSCOPE_API_KEY` | HTTP 503 · `LLM_PROVIDER_MISCONFIGURED` | 配置 key 后 | 结构化 detail |
| F2 | `fp-bailian-upstream` | DashScope 4xx/5xx（非额度） | HTTP 502 · `LLM_REQUEST_FAILED` | 视错误 | 错误 message |
| F3 | `fp-bailian-stub-removed` | 曾 stub `NotImplementedError` | 已移除 · 不再 500 | — | — |

---

## 验收标准

- [x] `pytest tests/ops_desk/test_llm_usage_metrics.py -v` 绿
- [x] `pytest tests/ops_desk/ -q` 绿
- [x] `pytest tests -m "not intent_eval and not intent_benchmark" -q` 绿
- [x] `ruff check api/ops tests/ops_desk` 绿
- [x] mock bailian HTTP · 缺 key 503 · D4 人验 run `33d484ea` · `total_tokens=1855`

---

## 交付清单

- [x] `BailianProvider.complete()` · `openai_compatible` helper
- [x] `.env.example` · `PROJECT_CONFIG`
- [x] human checklist §8 V9「可生产切换」

---

## 下一棒

P2-5f LLM model fallback · Projects [`task_ops_desk_p2_llm_model_fallback_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_llm_model_fallback_v1.md)

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-25 | task_validate 补齐 §失败路径 + §验收 pytest · human CLOSE |
| 2026-06-25 | 初版 CLOSE · PR #212 |
