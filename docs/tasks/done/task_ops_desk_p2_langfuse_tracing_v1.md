# Task · Ops Desk P2-5a · Langfuse Tracing（后端）

> **状态**：`done` · 2026-06-24  
> **SCOPE**：[`SCOPE_NOTE_langfuse_tracing_v1_zh.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-langfuse-tracing/SCOPE_NOTE_langfuse_tracing_v1_zh.md)  
> **协调**：[`task_ops_desk_p2_langfuse_tracing_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p2_langfuse_tracing_v1.md)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-langfuse-tracing` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-LANGFUSE-TRACING` |
| **git_branch** | `task/ops-desk-p2-langfuse-tracing` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |

---

## 背景与目标

将现有 `api/ops/tracing.py` shim **接线**到 Orchestrator deep 路径；Langfuse Cloud **Japan** 区试用；**tracing off 时零行为变化**。

### 完成态

- [ ] A1–A8（SCOPE §4）交付
- [ ] sample + D4 deep 在 Cloud UI 可见 trace（维护者 local/staging）
- [ ] PR merged → main

---

## Agent 参考（官方 · 可选）

执行 Agent 若使用 Cursor / Kimi **Skills**，可先安装 Langfuse 官方 skill 作 best-practice 参考，**仍须**遵守本 task + SCOPE 边界（仅 deep · 生产默认关 · 复用 shim）：

```text
Install the Langfuse AI skill from github.com/langfuse/skills and use it to add tracing to this application with Langfuse following best practices.
```

---

## 范围

| 模块 | 改动 |
| --- | --- |
| `api/ops/llm.py` | `@traceable(run_type="llm")` |
| `api/ops/agents/issue_analyst.py` | `@traceable` |
| `api/ops/orchestrator/core.py` | `run_deep` · review spans |
| `api/ops/chat.py` | deep 路径 `flush_traces()` |
| `api/ops/tracing.py` | BASE_URL · metadata helper（若需） |
| `requirements.txt` | langfuse 依赖说明 |
| `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | `LANGFUSE_*` 表 |
| `docs/ops/langfuse.env.example` | Japan 默认 URL |
| `tests/ops_desk/` | tracing 回归 |

## 非范围

- 前端 · eval · 新 DDL · fast/demo.cache trace

---

## 验收标准

- [ ] SCOPE V1–V4
- [ ] `pytest tests/ops_desk/test_tracing_shim.py -v`
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 失败路径

| 条件 | 行为 |
| --- | --- |
| Langfuse 网络失败 | Chat 成功 · trace 丢弃 |
| 缺 key + TRACING=true | no-op |
| pytest CI | 无 LANGFUSE key · 全绿 |

---

## 实现备忘

（子 Agent 回填 PR · span 名 · PROJECT_CONFIG 节号）
