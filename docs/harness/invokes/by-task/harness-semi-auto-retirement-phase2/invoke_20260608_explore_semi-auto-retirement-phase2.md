# Invoke · explore · T1 · harness-semi-auto-retirement-phase2

| 字段 | 值 |
| --- | --- |
| **task_slug** | `harness-semi-auto-retirement-phase2` |
| **round** | T1 |
| **hat** | explore |
| **task** | `docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md` |
| **freeze_id** | `GOV-HARNESS-SEMI-AUTO-RETIRE-P2@2026-06-08` |
| **git_branch** | `task/harness-semi-auto-retirement-phase2-v1` |

## Gate

- HG-TASK-DRAFT: `approved`
- HG-CHAIN-P2-EXEC: `approved`

## §3 可复制 Prompt

```text
【角色】Harness explore · Phase 2 · 只读差分

【canonical 读序】
1. docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md
2. docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md
3. docs/harness/HARNESS_V2_PLAN.md §0.0 · §5.6
4. docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
5. .cursor/rules/05-harness-semi-auto.mdc · 06-harness-in-repo.mdc
6. docs/tasks/RECENT_TASK_SCHEDULE.md §0.0 · §1.3

【forbidden】api/** · tests/** · .github/** · 删历史 invoke/review

【交付】P2-1～P2-8 缺口表 · SPEC 是否仍写「待 B 轨」· §0.0 semi_auto 常模残留
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

## 交付

- `docs/harness/invokes/by-task/harness-semi-auto-retirement-phase2/explore_semi_auto_retirement_phase2_gap.md`

## 下一棒

harness-22-audit
