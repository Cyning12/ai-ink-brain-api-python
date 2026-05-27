# Invoke · 关账 · R1 · gov-t4-spec-active

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | CLOSE |
> | task | `docs/tasks/done/task_governance_t4_spec_active_v1.md` |
> | task_slug | `gov-t4-spec-active` |
> | freeze_id | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |

---

## §1 关账结论

R1 **gov-t4-spec-active** 关账完成。T4 Bridge SPEC **active**；invoke C2 全绿；无阻塞。

---

## §2 执行路线与 Commit 回溯

| 序号 | 帽子 | 关键动作 | 落盘工件 | commit |
| --- | --- | --- | --- | --- |
| 1 | 22 | 零阻塞审查 | review + invoke_22 | `12fc851` |
| 2 | 30 | SPEC active + 排期 | governance + RECENT + task 范围 | `59f3060` |
| 3 | 40 | VERIFY 重跑 + 自检表 | invoke_40 + task 自检 | `e2ff23c` |
| 4 | 50 | 独立复检 15/15 | reinspect + invoke_50 | `f67f6c4` |
| 5 | CLOSE | git mv done + _views | done task + CLOSE invoke | （本 commit） |

```text
### api-python（task/wiki-loop-p2-followup-v1）
- CLOSE  docs(task): R1 关账 gov-t4-spec-active → done/
- f67f6c4 docs(harness): R1·50 独立复检
- e2ff23c docs(harness): R1·40 自检
- 59f3060 docs(governance): R1·30 T4 SPEC active
- 12fc851 docs(harness): R1·22 任务审核
```

---

## §3 续跑 R2（cross_round_semi_auto）

| 项 | 值 |
| --- | --- |
| **round** | R2 |
| **task** | `docs/tasks/active/task_governance_l2_phase_c_design_v1.md` |
| **task_slug** | `gov-l2-phase-c-design` |
| **freeze_id** | `GOV-L2-PHASE-C-DESIGN@2026-05-27` |
| **前置** | R1 已在 `done/` ✓ |
| **下一棒** | 22 → 30 → 40 → 50 → 关账（同 PROMPT_LOOP_22_to_CLOSE · round=R2） |

**R2 交付概要**（见 P2 SPEC §2）：L2 SPEC 增 Phase C 设计节 · failure_paths ↔ manifest 口径 · **不** 新增校验脚本。

---

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前：R1 CLOSE · done
├── 母 Loop：wiki-loop-p2-followup · in_progress
├── 分支：task/wiki-loop-p2-followup-v1
└── 下一 round：R2 · gov-l2-phase-c-design（semi_auto 续跑）
```
