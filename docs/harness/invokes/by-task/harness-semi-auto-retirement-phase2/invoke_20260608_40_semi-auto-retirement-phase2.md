# Invoke · 40 · T1 · harness-semi-auto-retirement-phase2

| 字段 | 值 |
| --- | --- |
| **task_slug** | `harness-semi-auto-retirement-phase2` |
| **round** | T1 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md` |
| **freeze_id** | `GOV-HARNESS-SEMI-AUTO-RETIRE-P2@2026-06-08` |
| **git_branch** | `task/harness-semi-auto-retirement-phase2-v1` |

## Gate

- HG-TASK-DRAFT: `approved`
- HG-CHAIN-P2-EXEC: `approved`

## §3 可复制 Prompt

```text
【角色】Harness 40 · docs-only 自检

【验证】
- rg -n 'DEPRECATED|deprecated|全面生效' docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md .cursor/rules/05-harness-semi-auto.mdc
- rg -n '待 B 轨' docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md  # 应无匹配
- python tools/harness_task_validate.py docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md

【跳过】pytest · 50（not_applicable · task 明示）

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

## 下一棒

CLOSE（Lead）
