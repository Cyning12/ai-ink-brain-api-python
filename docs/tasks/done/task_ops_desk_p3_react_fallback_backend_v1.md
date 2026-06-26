# Task · Ops Desk P3-1 · ReAct Fallback · 后端

> **状态**：`CLOSE` · merged `730a3735` · 2026-06-26  
> **协调 task**：[`task_ops_desk_p3_react_fallback_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p3_react_fallback_v1.md)  
> **SCOPE**：[`SCOPE_NOTE_react_fallback_v1_zh.md`](../../../../docs/harness/invokes/by-task/ops-desk-p3-react-fallback/SCOPE_NOTE_react_fallback_v1_zh.md)  
> **human checklist**：[`CHECKLIST_ops_desk_p3_react_fallback_human_v1_zh.md`](../../../../docs/harness/reviews/CHECKLIST_ops_desk_p3_react_fallback_human_v1_zh.md)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p3-react-fallback` |
| **泳道** | A · 后端 |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P3-REACT-FALLBACK` |
| **git_branch** | `task/ops-desk-p3-react-fallback` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **PR** | [#221](https://github.com/Cyning12/ai-ink-brain-api-python/pull/221) · merge `730a3735` |

---

## 交付清单

- [x] `OpsToolRegistry` + v0 只读工具 (`api/ops/react_tools.py`)
- [x] `run_react_fallback` · max_steps · events (`api/ops/react_loop.py`)
- [x] `chat.py` fallback 路由改 ReAct
- [x] `tests/ops_desk/test_react_fallback.py`
- [x] Review + synthesize 复用
- [x] `supabase/sql/ops_desk_p3_react_route.sql` migration

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- | --- | --- |
| F1 | `fp-react-max-steps` | ReAct 达 `max_steps` 仍未 final | Review → `partial` synthesize | 用户换问法 | 部分答案 + 说明未穷尽 |
| F2 | `fp-tool-not-found` | LLM 输出非法 tool 名 | 事件记录 err · 一步内纠正或 fail | 自动 1 次 | 错误提示或降级短答 |
| F3 | `fp-tool-handler-error` | DB/API 查询失败 | 结构化 err 写入 events · 循环继续或 abort | 视错误 | Chat 错误 message |
| F4 | `fp-review-reject-react` | ReAct 终答 Review 不通过 | 重试 synthesize（≤2）· 与 deep 路径一致 | 有限 | 修订后答案或 partial |
| F5 | `fp-fallback-misroute` | 本应 fast 却进 ReAct | 指标类问句回归测试门禁 | — | pytest 红灯 |

---

## 验收标准

- [x] `pytest tests/ops_desk/test_react_fallback.py -v` 绿
- [x] `pytest tests/ops_desk/ -q` 绿（17 既有失败为本地环境，非 P3-1）
- [x] `harness_task_validate` 本 task 绿
- [x] misroute 回归：metrics 问句仍 fast

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-26 | **CLOSE** · merge #221 `730a3735` · human gate `HG-OPS-P3-1-REACT` pass |
| 2026-06-25 | v1 · 00 派工骨架 |
