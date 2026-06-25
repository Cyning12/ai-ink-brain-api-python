# Task · Ops Desk P2-5c · 百炼 Provider（后端子仓）

> **状态**：`active` · 2026-06-24  
> **协调 task**：Projects [`task_ops_desk_p2_bailian_provider_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_bailian_provider_v1.md)  
> **invoke**：[`PROMPT_CHAIN_30_40_50_CLOSE_v1.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-bailian-provider/PROMPT_CHAIN_30_40_50_CLOSE_v1.md)

---

## 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-bailian-provider` |
| **test_strategy** | `required` |
| **分支建议** | `task/ops-desk-p2-bailian-provider` |

---

## 目标

实现 `BailianProvider.complete()`，使 `OPS_LLM_PROVIDER=bailian` 可走 Ops Desk deep/fast LLM（**OpenAI 兼容 Chat**，非 DashScope 原生 SDK）。

---

## 交付清单

- [x] `api/ops/llm/providers/bailian.py` — 真实 `POST …/chat/completions`
- [x] env：`BAILIAN_API_KEY`（fallback `DASHSCOPE_API_KEY`）· `BAILIAN_BASE_URL` · `BAILIAN_MODEL`
- [x] 缺 key → **503** `LLM_PROVIDER_MISCONFIGURED`（`OpsLlmMisconfiguredError` + `chat_completion` 映射）
- [x] `usage` → `LlmUsage` · `llm.usage` event · `metrics_json.llm.provider=bailian`
- [x] 与 `SiliconFlowProvider` 抽共享 `openai_compatible_complete`（`api/ops/llm/providers/openai_compatible.py`）
- [x] `tests/ops_desk/test_llm_usage_metrics.py` — bailian factory + mock HTTP
- [x] `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` · `.env.example` 补全说明

---

## 官方文档（实现时 @ 引用）

| 文档 | URL |
| --- | --- |
| OpenAI 兼容 Chat（主） | https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions |
| 地域 Base URL | https://help.aliyun.com/zh/model-studio/regions/ |
| API Key | https://help.aliyun.com/zh/model-studio/get-api-key |
| 控制台 Chat API | https://bailian.console.aliyun.com/cn-beijing?tab=api#/api/?type=model&url=3016807 |

默认 Base URL：`https://dashscope.aliyuncs.com/compatible-mode/v1`

---

## 自检

```bash
OPS_DESK_SECRET= pytest tests/ops_desk/test_llm_usage_metrics.py -v
OPS_DESK_SECRET= pytest tests/ops_desk/ -q
OPS_DESK_SECRET= pytest tests -m "not intent_eval and not intent_benchmark" -q
```

---

## 非范围

- DashScope 原生 SDK · Responses API · 流式
- H4 Provider KV（另 task · 百炼 cache 字段实测后可 follow-up）
- 前端 Provider 切换 UI
