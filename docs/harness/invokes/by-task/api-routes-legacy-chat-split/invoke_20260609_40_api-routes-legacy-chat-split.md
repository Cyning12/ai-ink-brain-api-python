# Invoke · 40 · W2 · api-routes-legacy-chat-split

## 元信息

| 字段 | 值 |
|------|-----|
| **task** | `docs/tasks/active/task_api_routes_legacy_chat_split_w2.md` |
| **slug** | `api-routes-legacy-chat-split` |
| **hat** | `40` |
| **git_branch** | `task/api-routes-legacy-w2` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

## 执行摘要

40 自检帽已完成。验收标准 10/10 全部 PASS：
- `api/routes/legacy_chat.py` 存在且 ruff 绿
- `index.py` 438 行（目标 <850）
- 新增 8 个测试全部通过
- 全量 pytest 347 passed，原有测试无回归
- 单 PR 触及 4 个 `api/*.py` 文件（≤8）
- 契约不变

Task 文件已回填「自检结论（40）」小节。
