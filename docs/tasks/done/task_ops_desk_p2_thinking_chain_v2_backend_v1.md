# Task · Ops Desk P2-4 · Thinking Chain v2（后端）

> **状态**：`active`  
> **SCOPE**：[`SCOPE_NOTE_thinking_chain_v2_v1_zh.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-thinking-chain-v2/SCOPE_NOTE_thinking_chain_v2_v1_zh.md)  
> **协调**：[`task_ops_desk_p2_thinking_chain_v2_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_thinking_chain_v2_v1.md)  
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

---

## 背景与目标

升级 Deep 路径：**Review 反馈重试** · **citation url 归一化（V2）** · **expanded event payload** · **FALLBACK 澄清**。

### 完成态

- [ ] citation url 在 Review 前对齐 DB `html_url`
- [ ] `analyze_issue` 支持 `review_feedback` 注入
- [ ] `agent.tool.result` payload 含 reasoning/suggestion/confidence/citations
- [ ] FALLBACK 无 issue 号时 fast 澄清（非 silent #545 deep）
- [ ] `tests/ops_desk/test_thinking_chain_p2.py` pass
- [ ] PR merged → main

---

## 范围

| 模块 | 改动 |
| --- | --- |
| `api/ops/orchestrator/core.py` | `run_deep` · `review_result` 调用链 |
| `api/ops/orchestrator/issue_analyst.py`（或同级） | feedback prompt · url normalize |
| `api/ops/chat.py` | FALLBACK 路由 |
| `tests/ops_desk/` | 新测 + 回归 demo/orchestrator |

## 非范围

- Langfuse · 新 DDL · LangGraph 全替 · 前端 UI

---

## 验收标准

- [ ] Demo D4：Review 不因 V2 url fail（或 retry 后 pass）
- [ ] mock Review V3 fail → 第二轮 prompt 含 feedback
- [ ] FALLBACK「你好」→ fast · 无 deep run
- [ ] `pytest tests/ops_desk/test_thinking_chain_p2.py -v` 绿
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 绿

---

## 失败路径

| 条件 | 行为 |
| --- | --- |
| LLM JSON 解析失败 | `partial` · error 写入 events |
| issue 不存在 | Review V1 fail → 重试上限 → partial |
| Review 全 fail 达上限 | 仍 synthesize · status=partial |

---

## 实现备忘

（子 Agent 回填 PR · 文件列表 · 图谱变更点）
