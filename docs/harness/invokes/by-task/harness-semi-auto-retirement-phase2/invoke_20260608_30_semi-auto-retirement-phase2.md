# Invoke · 30 · T1 · harness-semi-auto-retirement-phase2

| 字段 | 值 |
| --- | --- |
| **task_slug** | `harness-semi-auto-retirement-phase2` |
| **round** | T1 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md` |
| **freeze_id** | `GOV-HARNESS-SEMI-AUTO-RETIRE-P2@2026-06-08` |
| **git_branch** | `task/harness-semi-auto-retirement-phase2-v1` |

## Gate

- HG-TASK-DRAFT: `approved`
- HG-CHAIN-P2-EXEC: `approved`

## §3 可复制 Prompt

```text
【角色】Harness 30 · 纯 docs · 执行 task §范围 P2-1～P2-8

【读序】task · R1（无阻塞）· explore

【forbidden】api/** · tests/** · .github/** · git log/blame · 删 invokes/reviews/done 历史

【必须完成】
- SPEC 全面生效 · §0/§1 完成态
- HARNESS_V2_PLAN §0.0 + §5.6 deprecated 表述
- HANDOFF_SEMI_AUTO DEPRECATED 横幅
- 05/06 .mdc deprecated + 链式 pointer
- TASK_TEMPLATE · README · AGENTS · RECENT §0.0/§1.4
- governance/prompts README · MANIFEST Phase 2 行
- harness_task_validate task → OK

【禁止 git commit · Lead 负责】
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

## 下一棒

harness-40-check
