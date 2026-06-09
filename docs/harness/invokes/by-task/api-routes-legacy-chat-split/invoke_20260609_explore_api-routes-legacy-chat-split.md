# Invoke · explore · W2 · api-routes-legacy-chat-split

## 元信息

| 字段 | 值 |
|------|-----|
| **task** | `docs/tasks/active/task_api_routes_legacy_chat_split_w2.md` |
| **slug** | `api-routes-legacy-chat-split` |
| **hat** | `explore` |
| **git_branch** | `task/api-routes-legacy-w2` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

## 指令（§3 可复制 Prompt）

你 = Harness 22（审查帽）子代理。只读分析，禁止修改 api/ 或 tests/ 任何文件。

任务：审查 `api/index.py` 中 legacy chat/retrieve 路由的拆分可行性。

### 分析范围

1. **路由列表**：
   - `POST /api/py/chat`（~410 行，696–1105）
   - `GET /api/py/chat/history`（~66 行，521–586）
   - `GET /api/py/chat/suggested-questions`（~17 行，1180–1197）

2. **辅助函数归属判定**：
   - **共享（留在 index.py）**：`fetch_keyword_hits`, `_fetch_keyword_hits_for_fallback`, `build_sources_payload`, `_rag_log`, `_short`, `_extract_title_from_context`, `_require_auth`, `_try_chatbi_bearer_plain`, `_require_rag_history_auth`
   - **chat 专属（随路由下沉）**：`_collect_date_hints`, `augment_query_for_embedding`, `_hint_to_slug`, `_row_chunk_index`, `fetch_date_anchor_hits`, `merge_hits_anchors_first`, `message_to_text`, `last_user_text`, `build_system_prompt`

3. **跨模块引用验证**：
   - `code_retrieval.py` 通过 `bind_index_symbols` 绑定了 `build_sources_payload` 和 `_rag_log`
   - `keyword_fallback.py` 接受 `fetch_keyword_hits` 作为 Callable 参数
   - 确认无循环依赖风险

4. **测试覆盖**：
   - 现有：`test_chat_suggested_questions_route.py`（已有）
   - 缺失：`/api/py/chat` POST、`/api/py/chat/history` GET 的 route-level mock 测试
   - 须补 `tests/test_legacy_chat_route.py`、`tests/test_legacy_chat_history_route.py`

### 输出要求

- 报告：函数归属判定是否正确
- 报告：是否有遗漏的跨模块引用
- 报告：拆分后 `index.py` 预期行数（~850）
- 报告：`api/routes/legacy_chat.py` 预期导入清单
- 结论：是否可进入 30 帽（实现）
