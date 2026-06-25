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

见协调 task §失败路径 F1–F5。

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
