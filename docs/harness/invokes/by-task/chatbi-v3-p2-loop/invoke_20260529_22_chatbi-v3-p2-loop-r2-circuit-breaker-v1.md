# Invoke · 22 任务审核 · R2 · chatbi-v3-p2-loop-r2-circuit-breaker

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_chatbi_v3_p2_resilience_circuit_breaker_v1.md` |
| **task_slug** | `chatbi-v3-p2-loop-r2-circuit-breaker` |
| **freeze_id** | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| **git_branch** | `task/chatbi-v3-p2-loop-v1` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 ChatBI P2 Loop **R2** 帽链：**22 → 30 → 40 → 50（required）**，严格遵循 HANDOFF_SEMI_AUTO、SKILL-harness-loop-batch。

【元信息】
- round: R2
- task: docs/tasks/active/task_chatbi_v3_p2_resilience_circuit_breaker_v1.md
- task_slug: chatbi-v3-p2-loop-r2-circuit-breaker
- freeze_id: SPEC-ChatBI-V3-Resilience-Ops@2026-05-11
- git_branch: task/chatbi-v3-p2-loop-v1
- 母 task: docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md
- 前置：R1 #0b/#W1 已在 done/（commit 24f2df9）

开帽前：
python tools/harness_human_gate_check.py --task docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md
python tools/harness_human_gate_check.py --task docs/tasks/active/task_chatbi_v3_p2_resilience_circuit_breaker_v1.md

【R2 交付】
- api/chatbi_circuit_breaker.py + rag_env/index 集成
- tests/test_circuit_breaker*.py
- PROJECT_CONFIG env 行 · _manifest 增量
- 50 reinspect 必落盘

硬约束：test_strategy required · 单 PR · 50 必做
```
