# Task · Ops Desk P3-1 · ReAct Fallback · 后端

> **状态**：`ready` · 2026-06-25  
> **协调 task**：[`task_ops_desk_p3_react_fallback_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p3_react_fallback_v1.md)  
> **SCOPE**：[`SCOPE_NOTE_react_fallback_v1_zh.md`](../../../../docs/harness/invokes/by-task/ops-desk-p3-react-fallback/SCOPE_NOTE_react_fallback_v1_zh.md)

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

---

## 交付清单

- [ ] `OpsToolRegistry` + v0 只读工具
- [ ] `run_react_fallback` · max_steps · events
- [ ] `chat.py` fallback 路由改 ReAct
- [ ] `tests/ops_desk/test_react_fallback.py`
- [ ] Review + synthesize 复用
- [ ] PROJECT_CONFIG / 图谱增量（若改路由）

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

- [ ] `pytest tests/ops_desk/test_react_fallback.py -v` 绿
- [ ] `pytest tests/ops_desk/ -q` 绿
- [ ] `harness_task_validate` 本 task 绿
- [ ] misroute 回归：metrics 问句仍 fast

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-25 | v1 · 00 派工骨架 |
