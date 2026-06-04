# Invoke · 30 执行编码 · chatbi_intent_hints_step2_v1 · 2026-06-04

| 字段 | 值 |
| --- | --- |
| **hat_code** | 30 |
| **task_slug** | `chatbi_intent_hints_step2_v1` |
| **task_path** | `docs/tasks/active/task_chatbi_intent_hints_step2_v1.md` |
| **git_branch** | `task/chatbi-intent-hints-step2-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **audit_review** | `docs/harness/reviews/by-task/chatbi_intent_hints_step2_v1/task_chatbi_intent_hints_step2_v1_audit_R1_20260604.md` |

## §3 快照（30 开帽 · 人签 HG-AUDIT-R1 后执行）

```text
30 执行帽 · U2 Step2 — router 同步 + LLM 仲裁
- 交付 S2-1～S2-6（intent_hints / intent_router / intent_agent / yaml / env / tests）
- VERIFY：pytest 聚焦 + 全集 · harness_task_validate
- 禁止 api/graph/*
```

## 执行摘要

| 交付 | 状态 |
| --- | --- |
| S2-1 `rag_rule_hits_from_hints` 等 | done · `api/intent_hints.py` |
| S2-2 router 合并 | done · `api/intent_router.py` |
| S2-3 `apply_hints_arbitration` | done · `api/intent_agent.py` |
| S2-4 yaml + env + PROJECT_CONFIG | done |
| S2-5 router Portfolio 单测 | done · +3 cases |
| S2-6 仲裁单测 | done · `tests/test_intent_hints_arbitration.py` |

**下一棒**：40 自检 → 50 独立复检落盘
