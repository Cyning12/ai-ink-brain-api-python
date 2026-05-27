# Invoke · 22 任务审核 · R2 · gov-l2-phase-c-design

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_l2_phase_c_design_v1.md` |
> | task_slug | `gov-l2-phase-c-design` |
> | freeze_id | `GOV-L2-PHASE-C-DESIGN@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |
> | invoke_snapshot | `docs/harness/reviews/by-task/wiki-loop-p2-followup/task_governance_l2_phase_c_design_v1_audit_R1_20260527.md` |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 母 Loop：`task_harness_wiki_loop_p2_followup_v1.md` · `HG-LOOP-BATCH` = **approved**（母单真值）。
- **前置**：R1 `gov-t4-spec-active` 已在 `docs/tasks/done/`。
- 下一棒：**30**；落盘 review 后 commit（`HANDOFF_AUTO_COMMIT.md`）。

## §2 审查结论

**零阻塞。** Phase B manifest CI **done**；本 round 仅 L2 SPEC **§4.4 design**，不增 tools/pytest。

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R2** 的 **30 执行编码帽**。上一帽（22 任务审核）已结束。

【元信息】
- round: R2
- hat: 30
- task: docs/tasks/active/task_governance_l2_phase_c_design_v1.md
- task_slug: gov-l2-phase-c-design
- freeze_id: GOV-L2-PHASE-C-DESIGN@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1
- 母 task: docs/tasks/done/task_harness_wiki_loop_p2_followup_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-p2-followup/

### 30 帽交付
1. [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../../../../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) 增 **§4.4 Phase C（design）**：双向口径表 · 示例 3 条 · 未来实现 task 验收草案。
2. [`docs/tasks/templates/TASK_TEMPLATE.md`](../../../../tasks/templates/TASK_TEMPLATE.md)：`failure_paths` 节后链 §4.4（实现另 task）。
3. [`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](../../../../spec/governance/SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md) §2 R2 行同步。
4. task 范围项预勾；`git add` 本轮路径 → `git commit`（message 含 freeze_id）。
5. 落盘 **40** invoke（§3 ≥15 行 · C2）。

### 硬约束
- 不新增 `tools/*`、不改 `tests/`、不改 CI workflow、不改 `docs/harness/prompts/`。
- 不实现 Phase C 双向校验脚本（属 follow-up task · `test_strategy: required`）。

### VERIFY（40 须重跑）
```bash
rg -n '### 4\.4 Phase C' docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md
rg -n '§4\.4' docs/tasks/templates/TASK_TEMPLATE.md
test -f docs/_tech_graph/_test_manifest.json
python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); print(len(m['entries']))"
```
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：gov-l2-phase-c-design · R2
├── 分支：task/wiki-loop-p2-followup-v1
├── human_gate：HG-LOOP-BATCH approved（母单）
└── 下一棒：30 · §3 已落盘
```
