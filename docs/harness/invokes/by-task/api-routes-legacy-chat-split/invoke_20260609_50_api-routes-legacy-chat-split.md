# Invoke · 50 · W2 · api-routes-legacy-chat-split

## 元信息

| 字段 | 值 |
|------|-----|
| **task** | `docs/tasks/active/task_api_routes_legacy_chat_split_w2.md` |
| **slug** | `api-routes-legacy-chat-split` |
| **hat** | `50` |
| **git_branch** | `task/api-routes-legacy-w2` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

## 执行摘要

50 复检帽已完成。21/21 项 PASS，2 项 WARN（非阻塞）：
1. `_require_rag_history_auth` 重复定义 — defer W3-W8
2. `_rag_log` 重复定义 — **已修复**（legacy_chat.py 改从 rag_shared import）

复检报告落盘：`docs/tasks/reinspect_results/reinspect_api_routes_legacy_chat_split_w2_20260609_v1.md`

验证：ruff 全绿，pytest 347 passed。
