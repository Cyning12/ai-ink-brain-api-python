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

| Scenario ID | 条件 | 行为 |
| --- | --- | --- |
| F1 | Langfuse 网络失败 | Chat 成功 · trace 丢弃 |
| F2 | 缺 key + TRACING=true | no-op |
| F3 | pytest CI | 无 LANGFUSE key · 全绿 |

---

## 行为变更（Delta）

### ADDED
- `api/ops/llm.py`: `chat_completion` 增加 `@traceable(run_type="llm")`
- `api/ops/agents/issue_analyst.py`: `analyze_issue` 增加 `@traceable`
- `api/ops/orchestrator/core.py`: `run_deep` / `review_result` 增加 `@traceable`；`run_deep` 新增 `intent` 参数并写入 trace metadata
- `api/ops/chat.py`: deep 路径出口增加 `flush_traces()`
- `api/ops/tracing.py`: 新增 `update_current_span_metadata` helper；`@traceable` 支持 `capture_input` / `capture_output`
- `tests/ops_desk/test_tracing_shim.py`: 扩展回归测试

### MODIFIED
- `requirements.txt`: langfuse optional 安装说明
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`: 新增 `LANGFUSE_*` 环境变量表
- `docs/ops/langfuse.env.example`: Japan URL + 生产默认 false 注释

### REMOVED
- 无

---

## 实现备忘

- PR: https://github.com/Cyning12/ai-ink-brain-api-python/pull/202
- Merge SHA: `7a001274219ab8c41ca6e08e09de0b37101faa27`
- Cloud UI 截图：维护者在 local/staging 配置 `LANGFUSE_TRACING=true` + Japan keys 后，跑 `examples/ops_desk_langfuse_sample.py` 或 Demo D4 deep 后于 Langfuse Cloud Tracing 页截图。
