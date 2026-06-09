> **epic**：`standards-engineering/api-modularization`
> **manifest_ref**：W2 · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**：`required`
> **非范围**：MANIFEST 表内未列出的 `api/*.py` 文件

---

# W2 · Legacy Chat 路由下沉

> **状态**：active（执行中）
> **slug**：`api-routes-legacy-chat-split`
> **git_branch**：`task/api-routes-legacy-w2`
> **风险**：Medium
> **freeze_id**：`CODING_BACKEND_L2@2026-06-09`

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-routes-legacy-chat-split` |
| **git_branch** | `task/api-routes-legacy-w2` |
| **orchestration** | Claude Code Harness 链 |
| **chain_prompt** | `PROMPT_claude_chain_serial_v1_T1_standards-backend-api-modularization-w2-w8_zh.md` |
| **test_strategy** | `required` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

---

## 目标

将 `api/index.py` 中 legacy chat/retrieve 路由抽至 `api/routes/legacy_chat.py`；`index.py` 仅保留路由注册（薄层 · P-01）。

### 下沉范围

| 路由 | 方法 | 行数（HEAD） |
|------|------|-------------|
| `/api/py/chat` | POST | ~410 行（696–1105） |
| `/api/py/chat/history` | GET | ~66 行（521–586） |
| `/api/py/chat/suggested-questions` | GET | ~17 行（1180–1197） |

### 辅助函数下沉判定

**随路由下沉**（chat/retrieve 专属）：
- `_collect_date_hints`, `augment_query_for_embedding`, `_hint_to_slug`
- `_row_chunk_index`, `fetch_date_anchor_hits`, `merge_hits_anchors_first`
- `message_to_text`, `last_user_text`, `build_system_prompt`
- `token_stream`（内嵌生成器，随 `chat` handler）
- `save_log_after_stream`（异步背景任务，随 `chat` handler）

**留在 `index.py`**（共享）：
- `fetch_keyword_hits`, `_fetch_keyword_hits_for_fallback`, `build_sources_payload`
- `_rag_log`, `_short`, `_extract_title_from_context`
- `_require_auth`, `_try_chatbi_bearer_plain`, `_require_rag_history_auth`
- `_build_live_payload`, `_component_status`, `_build_ready_components`
- `app` 实例、`register_rate_limit_middleware`

---

## 行为变更（Delta）

### ADDED
- `api/routes/legacy_chat.py` — 新模块，含 chat/chat_history/chat_suggested_questions handler
- `api/routes/__init__.py` — 包入口（若尚不存在）

### MODIFIED
- `api/index.py` — 移除下沉的 handler body，改为 `from .routes.legacy_chat import chat, chat_history, chat_suggested_questions` + `@app.*` 注册

### 不变
- 所有对外 HTTP path / method / request body / response shape
- `_contract_manifest.json` 无变更

---

## 先测后拆（D2）

拆前须补/锁行为测试：

| 路由 | 测试文件 | 覆盖 |
|------|----------|------|
| `/api/py/chat` POST | `tests/test_legacy_chat_route.py` | auth 401、缺少 messages 400、缺少 session_id 400、缺少 env 500、mock streaming 200 |
| `/api/py/chat/history` GET | `tests/test_legacy_chat_history_route.py` | auth 401、缺少 session_id 400、mock 历史 200 |
| `/api/py/chat/suggested-questions` GET | 已有 `tests/test_chat_suggested_questions_route.py` | 复用，无需新增 |

**测试策略**：FastAPI TestClient route-level mock；不外呼真实 LLM/Supabase。

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-mega-refactor | 单 PR 触及 >8 个 `api/*.py` | **拒合并** |
| F2 | fp-contract-break | 路由 path/method 变更 | **blocked** — 契约不变（D3） |
| F3 | fp-test-gap | 拆前无 route-level 测试锁定行为 | **22 阻塞** — 先补测试 |
| F4 | fp-shared-func-orphan | `build_sources_payload` 等共享函数被误移，导致 code_retrieval  breakage | **40 阻塞** |

---

## 验收标准

- [x] `api/routes/legacy_chat.py` 存在且 ruff 绿
- [x] `api/index.py` 仍包含所有路由注册（@app.post/get），但 handler body 已下沉
- [x] `index.py` 行数从 ~1197 降至 ~<850（W2 单一目标；最终 <400 需 W3～W8 完成）
- [x] `tests/test_legacy_chat_route.py` 通过（mock streaming）
- [x] `tests/test_legacy_chat_history_route.py` 通过
- [x] `tests/test_chat_suggested_questions_route.py` 仍通过
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [x] `ruff check api tests` 全绿
- [x] 单 PR 触及 `api/*.py` 数量 ≤8

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-09 | v1：W2 task 初稿 — legacy chat 路由下沉 |

---

### 自检结论（40）

| # | 验收项 | 结果 | 命令输出要点 |
|---|--------|------|-------------|
| 1 | `api/routes/legacy_chat.py` 存在且 ruff 绿 | **PASS** | `test -f` → EXISTS；`ruff check` → All checks passed |
| 2 | `api/index.py` 仍包含所有路由注册，handler body 已下沉 | **PASS** | `@app.post("/api/py/chat")` 等注册存在；body 仅薄层 `await chat(...)` 转发 |
| 3 | `index.py` 行数 <850 | **PASS** | `wc -l` → 438 行（目标 <850） |
| 4 | `tests/test_legacy_chat_route.py` 通过 | **PASS** | 5 passed（401/400/400/500/200 mock streaming） |
| 5 | `tests/test_legacy_chat_history_route.py` 通过 | **PASS** | 3 passed（401/400/200 mock） |
| 6 | `tests/test_chat_suggested_questions_route.py` 仍通过 | **PASS** | 1 passed |
| 7 | `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿 | **PASS** | 347 passed, 1 skipped, 2 deselected |
| 8 | `ruff check api tests` 全绿 | **PASS** | All checks passed |
| 9 | 单 PR 触及 `api/*.py` 数量 ≤8 | **PASS** | 共 4 个：`api/index.py`, `api/rag_shared.py`, `api/routes/__init__.py`, `api/routes/legacy_chat.py` |
| 10 | 契约不变 | **PASS** | path/method/request/response 无变更；`_contract_manifest.json` 未修改 |

**总体结论**：通过，无阻塞项。

**建议**：Lead 可 CLOSE 本 task 并合并 PR。
