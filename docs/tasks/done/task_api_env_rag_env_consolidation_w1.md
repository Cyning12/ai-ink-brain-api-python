# W1 · `rag_env` 收敛（index 顶层 env 迁入 helper）

> **状态**：done（PR [#146](https://github.com/Cyning12/ai-ink-brain-api-python/pull/146) · 2026-06-09）
> **epic**：`standards-engineering/api-modularization`  
> **manifest_ref**：W1 · task_standards_backend_api_modularization_manifest_v1.md  
> **test_strategy**：`required`  
> **非范围**：MANIFEST 表内未列出的 `api/*.py` 文件  

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-env-rag-env-consolidation` |
| **git_branch** | `task/api-env-rag-env-w1` |
| **orchestration** | Cursor Task 链 |
| **chain_prompt** | `PROMPT_cursor_task_chain_serial_v1_T1_standards-backend-api-modularization-w1-w8_zh.md` |
| **test_strategy** | `required` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

---

## 背景与目标

L2 **P-03** 要求 env 读取经 `api/rag_env.py`；`index.py` 顶层仍有 6 组模块级 `os.getenv` 及 3 处函数内散落读取（`API_KEY`、`SILICONFLOW_API_KEY`、debug 开关）。

**完成态**：

- [x] `index.py` **零** `os.getenv` / `os.environ`
- [x] 新增/复用 `rag_env` helper 覆盖：`CONTENT_DEFAULT_YEAR`、`SILICONFLOW_CHAT_MODEL`、`MAX_X_SOURCES_HEADER_CHARS`、`DEBUG_RAG`/`RAG_DEBUG`/`NODE_ENV`、`API_KEY`、可选 `SILICONFLOW_API_KEY`
- [x] `tests/test_rag_env_helpers_w1.py` 锁定 helper 默认与 override 行为
- [x] `ruff check` + pytest 绿；对外 HTTP 契约不变

---

## 范围

- `api/rag_env.py` — 新增 helper
- `api/index.py` — 移除顶层 env 常量，改 import helper
- `tests/test_rag_env_helpers_w1.py` — 行为单测

## 非范围

- `unified_chat.py` / `tools.py` 等其它模块 env 散落（W4～W8 或 defer）
- 路由拆分、HTTP path 变更
- `_tech_graph` 拓扑变更（无对外契约变化）

---

## 行为变更（Delta）

### MODIFIED（内部）

- `index.py` 模块级 SiliconFlow / year / header 常量 → `rag_env` helper 调用
- `_rag_debug_enabled` 逻辑迁入 `rag_env.rag_debug_enabled()`

### ADDED

- `rag_env`: `content_default_year()`, `siliconflow_chat_model()`, `max_x_sources_header_chars()`, `rag_debug_enabled()`, `api_key_optional()`, `siliconflow_api_key_optional()`

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-index-getenv-remains | 合并后 `index.py` 仍含 `os.getenv` | 50 阻塞 |
| F2 | fp-bind-symbols-break | `code_retrieval.bind_index_symbols` 传参类型/值漂移 | pytest 红 |

---

## 验收标准

- [x] `rg 'os\.getenv|os\.environ' api/index.py` 无匹配
- [x] pytest + ruff 绿
- [x] diff 仅 `rag_env.py` + `index.py` + tests + harness 文档

### 自检结论（40 帽 · 2026-06-09）

- `ruff check api tests` — 绿
- `pytest tests -m "not intent_eval and not intent_benchmark"` — 339 passed
- `python tools/harness_task_validate.py` — OK
