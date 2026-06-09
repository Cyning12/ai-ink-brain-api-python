# Invoke · 22 · W2 · api-routes-legacy-chat-split

## 元信息

| 字段 | 值 |
|------|-----|
| **task** | `docs/tasks/active/task_api_routes_legacy_chat_split_w2.md` |
| **slug** | `api-routes-legacy-chat-split` |
| **hat** | `22` |
| **git_branch** | `task/api-routes-legacy-w2` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

## 指令（§3 可复制 Prompt）

你 = Harness 22（审查帽）子代理。**只读 · 禁止修改 api/ 或 tests/ 任何文件**。

审查对象：`docs/tasks/active/task_api_routes_legacy_chat_split_w2.md` + `api/index.py` 拆分可行性。

### 审查清单（R1）

1. **范围合理性**：W2 仅移动 chat/chat_history/chat_suggested_questions 三个路由，未越界触及 admin/code/unified 路由
2. **共享函数判定**：`build_sources_payload` 被 `code_retrieval.py` bind、`fetch_keyword_hits` 被 `keyword_fallback.py` 引用 — 确认不可下沉
3. **chat 专属函数**：`_collect_date_hints`, `augment_query_for_embedding`, `fetch_date_anchor_hits`, `merge_hits_anchors_first`, `message_to_text`, `last_user_text`, `build_system_prompt` — 确认无外部引用
4. **循环依赖风险**：`legacy_chat.py` 需要 `index.py` 的共享函数 — 需通过参数注入或从 `rag_env`/`rag_logging` 等已有模块 import，不可直接 `from . import index`
5. **测试策略**：task 要求拆前补 `test_legacy_chat_route.py` + `test_legacy_chat_history_route.py` — 确认合理
6. **行数目标**：index.py ~1197 → ~850（W2 单目标）— 确认可实现
7. **契约不变**：path/method/请求体/响应体无变更 — 确认

### 输出要求

- 审查报告：`docs/harness/reviews/task_api_routes_legacy_chat_split_w2_audit_R1_20260609.md`
- 结论：**签收** / **阻塞**（列阻塞项）
- 若签收：含下一棒 30 帽的可复制 Prompt
