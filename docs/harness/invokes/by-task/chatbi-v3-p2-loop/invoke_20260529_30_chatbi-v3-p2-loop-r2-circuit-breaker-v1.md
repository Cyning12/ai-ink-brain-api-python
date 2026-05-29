# Invoke · 30 执行 · R2 · chatbi-v3-p2-loop-r2-circuit-breaker

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_chatbi_v3_p2_resilience_circuit_breaker_v1.md` |
| **task_slug** | `chatbi-v3-p2-loop-r2-circuit-breaker` |
| **freeze_id** | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| **git_branch** | `task/chatbi-v3-p2-loop-v1` |

---

## §3 可复制 Prompt 正文

```text
执行 ChatBI P2 Loop R2 · 30 · P2-1c 熔断。
task: docs/tasks/active/task_chatbi_v3_p2_resilience_circuit_breaker_v1.md
VERIFY: pytest tests/test_circuit_breaker.py && pytest tests -m "not intent_eval and not intent_benchmark"
交付: api/chatbi_circuit_breaker.py · rag_env/index 集成 · PROJECT_CONFIG env · 7 单测
semi_auto → 40
```
