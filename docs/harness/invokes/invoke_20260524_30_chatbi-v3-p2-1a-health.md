## Invoke 快照（30 执行帽 · P2-1a health/ready）

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md` |
| git_branch | `task/chatbi-v3-p2-1a-health` |
| worktree_root | `ai-ink-brain-api-python` |
| test_strategy | `required` |
| semi_auto | `true` |
| audit_profile | `post_close` |

### 用户输入快照（§3 全文见下方 fenced code）

```text
你正在扮演本仓（ai-ink-brain-api-python）Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md
- docs/harness/HARNESS_V2_PLAN.md §5
- 本仓 AGENTS.md（合并前必绿）

输入：
- 主 task：docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md
- cwd / git：ai-ink-brain-api-python（分支 task/chatbi-v3-p2-1a-health）
- 验证：pytest tests -m "not intent_eval and not intent_benchmark"
- 审核：无（路径 B；可选 22 零阻塞）
- SPEC：docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md §4；母单 docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md

范围：实现 /api/py/live + /api/py/ready；test_strategy required；非范围见 task。
```
