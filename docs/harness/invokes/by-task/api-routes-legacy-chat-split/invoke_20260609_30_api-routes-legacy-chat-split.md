# Invoke · 30 · W2 · api-routes-legacy-chat-split

## 元信息

| 字段 | 值 |
|------|-----|
| **task** | `docs/tasks/active/task_api_routes_legacy_chat_split_w2.md` |
| **slug** | `api-routes-legacy-chat-split` |
| **hat** | `30` |
| **git_branch** | `task/api-routes-legacy-w2` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

## 执行摘要

30 帽已完成实现。修改文件 6 个：
- `api/index.py` — 1197 → 438 行，薄层注册
- `api/rag_shared.py` — 迁入共享辅助函数
- `api/routes/legacy_chat.py` — 新增，含 3 个路由 handler
- `api/routes/__init__.py` — 新增，包入口
- `tests/test_legacy_chat_route.py` — 新增 5 例
- `tests/test_legacy_chat_history_route.py` — 新增 3 例

验证：ruff 全绿，pytest 347 passed（+8），原有测试无回归。
