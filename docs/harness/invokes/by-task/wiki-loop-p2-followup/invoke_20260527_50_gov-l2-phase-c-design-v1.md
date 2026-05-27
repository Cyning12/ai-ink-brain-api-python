# Invoke · 50 独立复检 · R2 · gov-l2-phase-c-design

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | 50 |
> | task | `docs/tasks/active/task_governance_l2_phase_c_design_v1.md` |
> | task_slug | `gov-l2-phase-c-design` |
> | freeze_id | `GOV-L2-PHASE-C-DESIGN@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |
> | reinspect | `docs/tasks/reinspect_results/reinspect_gov-l2-phase-c-design_20260527_v1.md` |

---

## §1 角色与纪律

- 本帽为 **50 独立复检**（`docs/harness/prompts/hats/50-independent-reinspect.md`）。
- 落盘 `reinspect_*`；与 40 命令输出 **独立重跑**（已写入 reinspect 扩写版）。

## §2 复检结论

**建议合并。** 6/6 + human_gate 审查 **pass**（见 reinspect 文件）。

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R2 关账**（非 META）。

【元信息】
- round: R2 · hat: CLOSE
- task_slug: gov-l2-phase-c-design
- freeze_id: GOV-L2-PHASE-C-DESIGN@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1

### 关账交付
1. 确认 task 头 `done（2026-05-27）` · 验收 `[x]`。
2. `git mv docs/tasks/active/task_governance_l2_phase_c_design_v1.md docs/tasks/done/`（若尚未 mv）。
3. 更新 `docs/tasks/_views/done.md`。
4. 落盘/更新 `invoke_20260527_CLOSE_gov-l2-phase-c-design-v1.md`（CLOSE_TRACE 含分帽 commit）。
5. commit。

### 续跑 R3（cross_round_semi_auto）
- task: `docs/tasks/active/task_governance_wiki_ingest_batch_2_v1.md`
- 母单 `HG-INGEST-BATCH-2-SCOPE` = **approved**（启动 R3·30 前复读母单表）
- 下一棒：R3 · **22** 任务审核
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：50 · 独立复检
├── 结论：建议合并
└── 下一棒：R2 CLOSE → R3·22
```
