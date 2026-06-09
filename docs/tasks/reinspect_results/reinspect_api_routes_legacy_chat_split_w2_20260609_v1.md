# 独立复检报告：W2 Legacy Chat 路由下沉

> **task_slug**: `api-routes-legacy-chat-split`  
> **freeze_id**: `CODING_BACKEND_L2@2026-06-09`  
> **复检日期**: 2026-06-09  
> **复检帽**: 50-independent-reinspect  
> **被检分支**: `task/api-routes-legacy-w2` (commit `3477405`..`46824a6`)

---

## 一、复检项清单与结果

| # | 复检项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | `api/routes/legacy_chat.py` 存在且 ruff 绿 | **PASS** | 文件存在 (`test -f`)；`ruff check api/routes/legacy_chat.py` → All checks passed |
| 2 | `api/index.py` 仍包含所有路由注册，handler body 已下沉 | **PASS** | `@app.post("/api/py/chat")` (L347)、`@app.get("/api/py/chat/history")` (L221)、`@app.get("/api/py/chat/suggested-questions")` (L436) 均存在；body 仅薄层 `await chat(...)` 转发，符合 P-01 薄路由 |
| 3 | `index.py` 行数 < 850 | **PASS** | `wc -l api/index.py` → 438 行（原 ~1197 行） |
| 4 | `api/routes/legacy_chat.py` 函数组织合理 | **PASS** | 按职责分组：日期提示(L71-101)、embedding 增强(L104-109)、anchor 检索(L135-187)、merge/hits(L190-215)、消息处理(L218-243)、system prompt(L246-256)、chat handler(L301-698)、chat_history(L701-762)、suggested_questions(L765-780) |
| 5 | `api/routes/legacy_chat.py` import 顺序合规 | **PASS** | 标准库 → 第三方 → 本仓相对导入；`from __future__` 置顶；无未使用 import（ruff 绿） |
| 6 | `api/index.py` import 顺序合规 | **PASS** | 标准库 → 第三方 → 本仓相对导入；`from __future__` 置顶；ruff 绿 |
| 7 | `api/rag_shared.py` 迁移函数完整、import 正确 | **PASS** | 迁移函数：`_rag_log`、`_short`、`_extract_title_from_context`、`fetch_keyword_hits`、`_fetch_keyword_hits_for_fallback`、`build_sources_payload`、`parse_match_threshold`、`strip_doc_context_prefix`；`api/index.py` L59-63 正确 `from .rag_shared import ...`；`code_retrieval.bind_index_symbols` (L142-151) 正确引用 `build_sources_payload_` 和 `parse_match_threshold_` |
| 8 | 循环依赖检查：`api/routes/legacy_chat.py` 可独立导入 | **PASS** | `python -c "from api.routes.legacy_chat import chat; print('OK')"` → OK |
| 9 | 循环依赖检查：`api/index.py` 可独立导入 | **PASS** | `python -c "from api.index import app; print('OK')"` → OK |
| 10 | `tests/test_legacy_chat_route.py` 覆盖关键路径 | **PASS** | 5 例通过：auth 401 (`test_chat_unauthorized`)、缺少 messages 400 (`test_chat_missing_messages`)、缺少 session_id 400 (`test_chat_missing_session_id`)、缺少 env 500 (`test_chat_missing_api_key`)、mock streaming 200 (`test_chat_mock_streaming`) |
| 11 | `tests/test_legacy_chat_history_route.py` 覆盖关键路径 | **PASS** | 3 例通过：auth 401 (`test_history_unauthorized`)、缺少 session_id 422 (`test_history_missing_session_id`，FastAPI Query(...) 无值产生 422 属于 validation error，行为正确)、mock 历史 200 (`test_history_mock`) |
| 12 | `tests/test_chat_suggested_questions_route.py` 仍通过 | **PASS** | 1 passed |
| 13 | 无 flaky test 风险（观察） | **PASS** | 测试均使用 TestClient + mock，无外呼真实 LLM/Supabase；无 `time.sleep`、无随机数据、无并发竞争 |
| 14 | 契约一致性：path/method/参数/返回类型 | **PASS** | diff 显示 `/api/py/chat` (POST)、`/api/py/chat/history` (GET)、`/api/py/chat/suggested-questions` (GET) 的 path/method 未变；参数签名（Query/Header/Request/BackgroundTasks）未变；返回类型（StreamingResponse/JSONResponse/dict）未变 |
| 15 | `_contract_manifest.json` 无需更新 | **PASS** | `git diff 911a4aa..HEAD -- _contract_manifest.json` 无输出（文件未修改） |
| 16 | 回归测试：`tests/test_rate_limit_routes.py` | **PASS** | 4 passed；`test_chat_route_returns_429_after_threshold` 通过，确认 `/api/py/chat` 路由注册未破坏 rate limit 中间件 |
| 17 | 回归测试：`tests/test_code_api_routes.py` | **PASS** | 6 passed；`code_retrieval.bind_index_symbols` 引用的 `build_sources_payload` 和 `parse_match_threshold` 已正确迁移至 `api/rag_shared.py`，无 breakage |
| 18 | 全量 pytest | **PASS** | `pytest tests -m "not intent_eval and not intent_benchmark"` → 347 passed, 1 skipped, 2 deselected |
| 19 | 全量 ruff | **PASS** | `ruff check api tests` → All checks passed |
| 20 | 单 PR 触及 `api/*.py` 数量 ≤ 8 | **PASS** | 共 4 个：`api/index.py`、`api/rag_shared.py`、`api/routes/__init__.py`、`api/routes/legacy_chat.py` |
| 21 | `human_gate` diff 审查 | **N/A** | task 文件中无 `human_gate`/`approved`/`pending` 标记；验收标准均为机器可检 checkbox，无需人签 gate |

---

## 二、发现的问题与建议

### 2.1 WARN：`_require_rag_history_auth` 在 `legacy_chat.py` 和 `index.py` 中重复定义

- **位置**：`api/routes/legacy_chat.py` L276-298 与 `api/index.py` L120-139
- **说明**：两个模块各自定义了同名函数 `_require_rag_history_auth`，逻辑基本一致。`legacy_chat.py` 的版本在 L296 通过 `from ..index import _require_auth` 回退到 index.py 的 auth 逻辑；`index.py` 的版本在 L139 直接调用本模块的 `_require_auth`。
- **影响**：当前无功能问题（`chat_history` 路由使用 `legacy_chat.py` 中的版本，其他路由使用 `index.py` 中的版本），但属于代码重复，未来维护时可能产生漂移。
- **建议**：W3-W8 模块化推进时，将 `_require_rag_history_auth` 和 `_require_auth` 统一提取到 `api/auth_utils.py` 或类似共享模块。

### 2.2 WARN：`_rag_log` 在 `api/rag_shared.py` 和 `api/routes/legacy_chat.py` 中重复定义

- **位置**：`api/rag_shared.py` L13-15 与 `api/routes/legacy_chat.py` L66-68
- **说明**：两个模块各自定义了同名函数 `_rag_log`，逻辑完全一致（检查 `rag_debug_enabled()` 后打印）。
- **影响**：当前无功能问题，但属于重复代码。
- **建议**：`legacy_chat.py` 可直接从 `rag_shared` import `_rag_log`，消除重复。属 hygiene 优化，非阻塞。

### 2.3 INFO：`legacy_chat.py` 中 `_require_auth` 的延迟导入

- **位置**：`api/routes/legacy_chat.py` L296-298 和 L308
- **说明**：函数内部使用 `from ..index import _require_auth` 进行延迟导入，这是为了避免顶层导入产生循环依赖的合理做法。
- **评估**：可接受。W3-W8 将 auth 工具提取到独立模块后，可改为顶层导入。

---

## 三、总体结论

**建议合并**。

- 所有验收项通过（21/21 PASS）。
- 无阻塞项。
- 2 项 WARN 均为代码重复/ hygiene 问题，不影响当前功能与契约，建议在 W3-W8 模块化后续阶段处理。
- 测试覆盖充分：新增 8 例 route-level 测试 + 全量 347 passed。
- ruff 全绿，无 lint 问题。
- 契约零变更，`_contract_manifest.json` 无需更新。

---

## 四、执行路线与 Commit 回溯

| Commit | 说明 |
|--------|------|
| `3477405` | refactor(api): W2 legacy chat 路由下沉至 api/routes/legacy_chat.py |
| `46824a6` | docs(harness): 40 W2 自检结论回填 — 全项 PASS |

**相关文件变更**：
- `api/index.py` — 移除 legacy chat handler body，改为薄层路由注册
- `api/rag_shared.py` — 新增共享函数（从 index.py 迁移）
- `api/routes/__init__.py` — 包入口（空文件）
- `api/routes/legacy_chat.py` — 新模块，含 chat/chat_history/chat_suggested_questions
- `tests/test_legacy_chat_route.py` — 新增 5 例测试
- `tests/test_legacy_chat_history_route.py` — 新增 3 例测试
