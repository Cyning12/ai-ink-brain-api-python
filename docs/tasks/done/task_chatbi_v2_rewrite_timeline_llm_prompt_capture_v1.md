# Task：ChatBI V2 — RAG 改写过程上链与 LLM Prompt 全量可观测

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


> **状态**：`done（2026-05-11 验收通过）`  
> **范围**：`ai-ink-brain-api-python` — V2 Agent SSE/JSON、`tools`、`intent_agent`、`query_rewrite`  
> **关联规格**：`docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md`（chain 事件、RAG 子步）  
> **配对前端任务**：`ai-ink-brain/content/tasks/active/task_frontend_unified_chat_v2_rewrite_llm_prompt_debug_v1.md`  
> **真值表**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（增补 env 时请同步该文件）

---

## 背景与目标

1. **Rewrite 上链**：V2 在 `rag_search` 路径与 V1 对齐，在 Timeline 上可见 **`tool.call.start/end`**，且 `payload.tool` 为 **`rag.rewrite`**，结束帧携带 **`rewritten_query`**；随后再发 **`rag_search`** 的 start/end，主工具 end 的 **`output`** 含 **`answer`** 与 **`rewritten_query`**（若存在）。  
2. **LLM Prompt 采集**：在显式开关下，将本轮请求内发往各子模型的 **完整 messages**（Intent、RAG 改写/生成、Text2SQL、Direct 等）以结构化事件透出，便于多轮核对「实际入模」内容。  
3. **V2 文档闭环**：本后端任务单已归档至 **`docs/tasks/done/`**；配对前端任务仍见 `ai-ink-brain/content/tasks/active/task_frontend_unified_chat_v2_rewrite_llm_prompt_debug_v1.md`（若前端亦收口，按该仓 `content/tasks/README.md` 同步 `git mv` 与 `_views/done.md`）。关联规格继续在 `docs/spec/` 维护。

---

## 范围

- [x] `api/query_rewrite.py`：`REWRITE_SYSTEM_INSTRUCTION`、`build_rewrite_llm_messages()`；改写调用与消息构造集中。  
- [x] `api/agent.py`：`rag_search` 步内先发 `rag.rewrite` 再发 `rag_search`；`tool.execute(..., debug_llm_prompts=...)`；SQL 重试路径同样透传；可选 emit **`agent.debug.llm_prompts`**（`scope` + `items[]`）。  
- [x] `api/intent_agent.py`：`decide_intent_v2(..., capture_llm_prompts)`；成功时 `raw_response.llm_prompts`；缓存条目不持久化大 payload。  
- [x] `api/tools.py`：`rag_search_execute` / `text2sql_execute` / `direct_answer_execute` 支持 `debug_llm_prompts`，RAG 改写结果含 `rewritten`、`rewrite_latency_ms`、可选 `llm_prompts`。  
- [x] `api/unified_chat.py`：`_debug_llm_prompts_enabled`（**`CHATBI_V2_DEBUG_LLM_PROMPTS`** 或 **`body.debug_llm_prompts === true`**）；JSON 与 SSE（增量 + batch replay）与 Agent 对齐。

## 非范围

- 前端 Timeline UI 细节（见配对前端任务）。  
- 降低 Prompt 体积或采样策略（后续若需另起任务）。

---

## 依赖与引用

| 项 | 说明 |
|----|------|
| env | `CHATBI_V2_DEBUG_LLM_PROMPTS`：`1` / `true` / `yes` / `on` 时全局开启 prompt 透出 |
| body | `debug_llm_prompts: true`（与 env 二选一即可生效） |
| chain 类型 | `tool`=`rag.rewrite`；`agent.debug.llm_prompts`（payload：`scope`、`items`；工具侧可含 `tool`、`step_number`） |

---

## 验收标准

- [x] `CHATBI_USE_AGENT=true`，走 RAG：SSE 中在 `rag_search` 的 `tool.call.start` 之前出现 **`rag.rewrite`** 的 start/end，且 end 含 **`rewritten_query`**。  
- [x] 开启 `debug_llm_prompts`（body 或 env）：至少出现 **`agent.debug.llm_prompts`**（Intent 一次；若工具链有多段 LLM，可按 step 多次），`items[].messages` 为发往模型的完整消息列表。  
- [x] `pytest tests/test_intent_cache.py tests/test_unified_chat_backend_v2_agent.py tests/test_unified_chat_sse_incremental_vnext.py` 通过。

---

## 实现备忘（回填）

| 模块 | 说明 |
|------|------|
| `_tech_graph` | 若流程图含 RAG 子步，增量同步 `10_flow_*`（如有） |

---

## 给 Cursor

验收、非范围、依赖、图谱、`_tech_graph`、`rag.rewrite`、`agent.debug.llm_prompts`、`CHATBI_V2_DEBUG_LLM_PROMPTS`、`debug_llm_prompts`、任务归档、`docs/tasks/done`、`_views/done.md`
