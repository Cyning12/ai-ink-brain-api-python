# Task · Ops Desk P2-4 · Thinking Chain v2（后端）

> **状态**：`done` · PR [#201](https://github.com/Cyning12/ai-ink-brain-api-python/pull/201) merged 2026-06-23  
> **SCOPE**：[`SCOPE_NOTE_thinking_chain_v2_v1_zh.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-thinking-chain-v2/SCOPE_NOTE_thinking_chain_v2_v1_zh.md)  
> **协调**：[`task_ops_desk_p2_thinking_chain_v2_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p2_thinking_chain_v2_v1.md)  
> **依赖**：P1-a orchestrator ✅ · P1-4 demo cache ✅

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-thinking-chain-v2-backend` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-THINKING-CHAIN-V2-BE` |
| **git_branch** | `task/ops-desk-p2-thinking-chain-v2-backend` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

---

## 背景与目标

升级 Deep 路径：**Review 反馈重试** · **citation url 归一化（V2）** · **expanded event payload** · **FALLBACK 澄清**。

### 完成态

- [x] citation url 在 Review 前对齐 DB `html_url`
- [x] `analyze_issue` 支持 `review_feedback` 注入
- [x] `agent.tool.result` payload 含 reasoning/suggestion/confidence/citations
- [x] FALLBACK 无 issue 号时 fast 澄清（非 silent #545 deep）
- [x] `tests/ops_desk/test_thinking_chain_p2.py` pass
- [x] PR merged → main

---

## 范围 / 非范围

| 范围 | 非范围 |
| --- | --- |
| `api/ops/orchestrator/core.py` · `run_deep` · Review 链 | Langfuse · 新 DDL |
| `api/ops/orchestrator/issue_analyst.py` · feedback · url normalize | LangGraph 全替 |
| `api/ops/chat.py` · FALLBACK 路由 | 前端 UI |
| `tests/ops_desk/test_thinking_chain_p2.py` | — |

---

## 行为变更（Delta）

### ADDED

- **Requirement**：Thinking Chain v2 Deep 路径
  - **Scenario**：`fp-tc-v2-review-retry` — Review fail 后注入 feedback 重试 analyze
  - **Scenario**：`fp-tc-v2-fallback-fast` — 无 issue 号 FALLBACK → fast 澄清

### MODIFIED

- **Requirement**：`agent.tool.result` expanded payload（reasoning · citations · confidence）

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- | --- | --- |
| F1 | `fp-tc-llm-json-fail` | LLM JSON 解析失败 | `partial` · error 写入 events | 有限 | partial 状态 |
| F2 | `fp-tc-issue-missing` | issue 不存在 | Review V1 fail → 重试上限 → partial | 有限 | partial + 事件 |
| F3 | `fp-tc-review-exhausted` | Review 全 fail 达上限 | 仍 synthesize · status=partial | 否 | partial 答案 |

---

## 验收标准

- [x] Demo D4：Review 不因 V2 url fail（或 retry 后 pass）
- [x] mock Review V3 fail → 第二轮 prompt 含 feedback
- [x] FALLBACK「你好」→ fast · 无 deep run
- [x] `pytest tests/ops_desk/test_thinking_chain_p2.py -v` 绿
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 绿

---

## 实现备忘

PR #201 · orchestrator Review 重试 · citation V2 url · FALLBACK fast 路由 · `test_thinking_chain_p2.py`
