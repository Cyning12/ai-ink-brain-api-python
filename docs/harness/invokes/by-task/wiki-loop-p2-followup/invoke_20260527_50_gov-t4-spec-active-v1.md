# Invoke · 50 独立复检 · R1 · gov-t4-spec-active

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 50 |
> | task | `docs/tasks/active/task_governance_t4_spec_active_v1.md` |
> | task_slug | `gov-t4-spec-active` |
> | freeze_id | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **50 独立复检**（`docs/harness/prompts/hats/50-independent-reinspect.md`）。
- 落盘 `docs/tasks/reinspect_results/reinspect_gov-t4-spec-active_20260527_v1.md`。
- 下一棒：**关账**（git mv + _views）。

## §2 复检结论

**15/15 pass · 建议合并。** 详见 reinspect 文件。

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R1 关账**（非 META）。

【元信息】
- round: R1 · hat: CLOSE
- task_slug: gov-t4-spec-active
- freeze_id: GOV-T4-SPEC-ACTIVE@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1

### 关账交付
1. `git mv docs/tasks/active/task_governance_t4_spec_active_v1.md docs/tasks/done/`
2. 头部改为 `done（2026-05-27 · GOV-T4-SPEC-ACTIVE@2026-05-27）`
3. 更新 `docs/tasks/_views/done.md` 追加一行
4. 落盘 `invoke_20260527_CLOSE_gov-t4-spec-active-v1.md`（含 CLOSE_TRACE + R2 续跑指针）
5. commit

### 续跑（cross_round_semi_auto）
按 LOOP_MANIFEST 启动 **R2**：`task_governance_l2_phase_c_design_v1.md` · `gov-l2-phase-c-design` · 22 帽链。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：50 · 独立复检
├── reinspect：reinspect_gov-t4-spec-active_20260527_v1.md
└── 下一棒：R1 关账 → R2
```
