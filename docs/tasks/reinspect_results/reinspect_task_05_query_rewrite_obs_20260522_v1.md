# 三方复检：task_05 Rewrite 可观测性（v1）

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `docs/tasks/active/task_05_query_rewrite_observability.md` |
| **git_branch** | `task/query-rewrite-obs` |
| **commit** | （合并前填写 `git rev-parse --short HEAD`） |
| **复检日期** | 2026-05-22 |
| **invoke_snapshot** | `docs/harness/invokes/by-task/task05-query-rewrite-obs/invoke_20260522_50_task05-reinspect.md` |

---

## 验收表

| 验收项 | pass/fail | 证据 | 备注 |
|--------|-----------|------|------|
| `metadata.match.query_compare` 字段齐全 | pass | `api/index.py` L739–751；`api/rag_logging.py` | 实现已合 main |
| task_04/文件名/日期 丢失判定 | pass | `tests/test_query_rewrite_compare_anchor.py` 4 passed | 单测 |
| `DEBUG_RAG=1` 摘要 | pass | `api/index.py` L780–788 `_rag_log("query_compare …")` | 未跑集成；代码路径存在 |
| 不影响流式/sources | pass | 对比仅写 metadata，融合仍用 rewrite 路 | 设计一致 |

---

## 阻塞合并项

- **Harness 人工闸**：`HG-AUDIT-R1`、`HG-REINSPECT` 仍为 `pending` — **须人** 改 `approved` 后方可标 task `done` 与合并 PR（Agent 不得代填）。

无代码阻塞项。

---

## 结论

**建议合并**（在人工闸通过后）：试点目标「子仓首份新 R1 + 单测 + 50 落盘」已满足；业务实现已在 `main`，本分支增量为 Harness 文档批 + task_05 对齐 + 单测。

---

## 给需求帽回填

无。
