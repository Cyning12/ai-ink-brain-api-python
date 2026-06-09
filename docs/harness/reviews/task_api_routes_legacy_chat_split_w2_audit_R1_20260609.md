# 22 R1 审查 · W2 · api-routes-legacy-chat-split

| 字段 | 值 |
|------|-----|
| **task** | `docs/tasks/active/task_api_routes_legacy_chat_split_w2.md` |
| **slug** | `api-routes-legacy-chat-split` |
| **round** | R1 |
| **date** | 2026-06-09 |
| **reviewer** | Harness 22 |

---

## 审查清单

### 1. 范围合理性

**结果**：PASS

W2 仅移动三个路由：
- `POST /api/py/chat`
- `GET /api/py/chat/history`
- `GET /api/py/chat/suggested-questions`

未越界触及 admin（sync/ingest）、code（query/search）、unified、text2sql、chain_chat 等路由。符合 D1。

### 2. 共享函数判定

**结果**：PASS

| 函数 | 外部引用 | 判定 |
|------|----------|------|
| `build_sources_payload` | `code_retrieval.py` bind_index_symbols | 不可下沉 |
| `_rag_log` | `code_retrieval.py` bind_index_symbols | 不可下沉 |
| `fetch_keyword_hits` | `keyword_fallback.py` Callable 参数 | 不可下沉 |
| `_require_auth` | 多个路由使用 | 不可下沉 |
| `_try_chatbi_bearer_plain` | `_require_rag_history_auth` 专用 | 可下沉但建议留 index |
| `_require_rag_history_auth` | `chat_history` 专用 | 可下沉但建议留 index |

### 3. Chat 专属函数外部引用

**结果**：PASS

通过 `grep -rn` 全仓扫描：`_collect_date_hints`, `augment_query_for_embedding`, `_hint_to_slug`, `_row_chunk_index`, `fetch_date_anchor_hits`, `merge_hits_anchors_first`, `message_to_text`, `last_user_text`, `build_system_prompt` 均无 `api/` 或 `tests/` 外部引用。可安全随路由下沉。

### 4. 循环依赖风险

**结果**：WARN（需 30 帽处理）

若 `legacy_chat.py` 直接从 `index.py` import 共享函数（`build_sources_payload`, `_rag_log` 等），将产生循环导入：
- `index.py` → `from .routes.legacy_chat import chat`（路由注册）
- `legacy_chat.py` → `from ..index import build_sources_payload`（共享函数）

**建议方案**：将共享辅助函数迁移至 `api/rag_shared.py`（已有模块，天然共享层）：
- `_rag_log`
- `_short`
- `_extract_title_from_context`
- `build_sources_payload`
- `fetch_keyword_hits`
- `_fetch_keyword_hits_for_fallback`

`index.py` 和 `legacy_chat.py` 共同从 `rag_shared` import。`code_retrieval.bind_index_symbols` 调用在 `index.py` 中保持不变（`index.py` 从 `rag_shared` import 后仍有这些名字）。

### 5. 测试策略

**结果**：PASS

Task 要求拆前补：
- `tests/test_legacy_chat_route.py` — mock POST /api/py/chat（auth/400/500/200）
- `tests/test_legacy_chat_history_route.py` — mock GET /api/py/chat/history

`test_chat_suggested_questions_route.py` 已有，复用。符合 D2 先测后拆。

### 6. 行数目标

**结果**：可实现

- `index.py` 1197 行
- 下沉：chat handler (~410) + chat_history (~66) + chat_suggested_questions (~17) + chat 专属辅助函数 (~180) = ~673 行
- 共享函数迁移至 rag_shared.py：~80 行
- `index.py` 预期：1197 - 673 - 80 = ~444 行

实际会略高于 444（import 语句、路由注册装饰器保留），但肯定 <850，符合目标。

### 7. 契约不变

**结果**：PASS

Path / method / request body / response shape 均无变更。`_contract_manifest.json` 无需修改。符合 D3。

---

## 审查结论

**签收（PASS）** — 可进入 30 帽（实现）。

**30 帽前置条件**：
1. 先补测试（`test_legacy_chat_route.py` + `test_legacy_chat_history_route.py`）
2. 将共享辅助函数移至 `api/rag_shared.py`
3. 创建 `api/routes/legacy_chat.py` + `api/routes/__init__.py`
4. `index.py` 更新 import + 移除下沉函数
5. 单 PR 触及文件 ≤8 个（当前预计：index.py, rag_shared.py, legacy_chat.py, __init__.py, 2 个测试文件 = 6 个）

---

## 下一棒 30 帽可复制 Prompt

```text
你 = Harness 30（实现帽）子代理。遵循：
- docs/tasks/active/task_api_routes_legacy_chat_split_w2.md
- docs/standards/CODING_BACKEND_L2_v1_zh.md（P-01 薄路由 · P-03 env 真值）

任务：实现 W2 legacy chat 路由下沉。

### 步骤（严格顺序）

1. **先补测试**（先测后拆 · D2）
   - `tests/test_legacy_chat_route.py`：
     - test_chat_unauthorized：无 auth header → 401
     - test_chat_missing_messages：无 messages → 400
     - test_chat_missing_session_id：无 session_id → 400
     - test_chat_missing_api_key：未配置 SILICONFLOW_API_KEY → 500
     - test_chat_mock_streaming：mock OpenAI + Supabase → 200 + 验证 StreamingResponse
   - `tests/test_legacy_chat_history_route.py`：
     - test_history_unauthorized → 401
     - test_history_missing_session_id → 400
     - test_history_mock → 200 + 验证 messages 列表

2. **共享函数迁移**
   - 将以下函数从 `api/index.py` 移至 `api/rag_shared.py`：
     - `_rag_log(msg: str) -> None`
     - `_short(text: str, max_len: int) -> str`
     - `_extract_title_from_context(content: str) -> str | None`
     - `build_sources_payload(hits, *, top_k=10) -> dict`
     - `fetch_keyword_hits(sb, query_text, *, match_count=12) -> list[dict]`
     - `_fetch_keyword_hits_for_fallback(sb, query_text, match_count) -> list[dict]`
   - `api/index.py` 更新 import：`from .rag_shared import ...`
   - 确保 `code_retrieval.bind_index_symbols` 调用仍可用（index.py 中这些名字仍存在）

3. **创建 `api/routes/legacy_chat.py`**
   - import 需要的外部模块：FastAPI, OpenAI, BackgroundTasks, HTTPException, etc.
   - import 从 `rag_shared` 迁移的共享函数
   - import 从 `rag_env`, `rag_logging`, `hybrid_fusion`, `ingest_pipeline` 等已有模块
   - 定义 chat 专属辅助函数（`_collect_date_hints` 等）
   - 定义三个路由 handler：`chat`, `chat_history`, `chat_suggested_questions`
   - `_rag_log` 可在本模块重新定义（3 行），避免跨模块依赖

4. **创建 `api/routes/__init__.py`**
   - 包入口，暴露 `legacy_chat` 模块

5. **更新 `api/index.py`**
   - 从 `.routes.legacy_chat import chat, chat_history, chat_suggested_questions`
   - 移除下沉的函数定义
   - 保留 `@app.post("/api/py/chat")` 等注册装饰器（薄层）
   - 共享函数 import 改为从 `rag_shared`

6. **验证**
   - `ruff check api tests` 全绿
   - `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
   - 测试新增的两个 route 测试通过
   - 原有 `test_chat_suggested_questions_route.py` 通过
   - `test_rate_limit_routes.py` 通过（它测试 /api/py/chat）

### 纪律
- **禁止 git commit**；改完回报文件清单，由 Lead commit
- 单 PR 触及 `api/*.py` 文件 ≤8 个
- 契约不变：path / method / request body / response shape 不得变更
- 不修改 `_contract_manifest.json`
```

---

## 执行路线与 Commit 回溯

| 阶段 | 关键动作 | 落盘工件 | 对应 commit |
|------|----------|----------|-------------|
| explore | grep 影响面分析 | invoke_20260609_explore_* | api-python@8f781e7 |
| 22 R1 | 审查报告 + 下一棒 Prompt | reviews/task_*_audit_R1_* | —（本文件待 commit） |
