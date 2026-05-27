# Invoke · 30 执行编码 · R2 · gov-l2-phase-c-design

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_l2_phase_c_design_v1.md` |
> | task_slug | `gov-l2-phase-c-design` |
> | freeze_id | `GOV-L2-PHASE-C-DESIGN@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **30 执行编码**（`docs/harness/prompts/hats/30-execute-code.md`）。
- 交付 **设计文档 only**；与 P2 SPEC §2 R2 边界一致。

## §2 交付摘要

| 文件 | 变更 |
| --- | --- |
| `SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` | §4.4 Phase C design · §4.3 表 Phase C 行 · 修订 v1.2 |
| `TASK_TEMPLATE.md` | `failure_paths` → §4.4 pointer |
| `SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md` | §2 R2 交付描述 |
| `task_governance_l2_phase_c_design_v1.md` | 范围 `[x]` |

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R2** 的 **40 自检帽**。上一帽（30 执行编码）已结束。

【元信息】
- round: R2
- hat: 40
- task: docs/tasks/active/task_governance_l2_phase_c_design_v1.md
- task_slug: gov-l2-phase-c-design
- freeze_id: GOV-L2-PHASE-C-DESIGN@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1

### 40 帽交付
1. 独立重跑 VERIFY（须有命令与 exit code）：
   - `rg '### 4.4 Phase C'` L2 SPEC
   - `rg '§4.4' TASK_TEMPLATE`
   - `_test_manifest.json` JSON 解析 · entries 数
   - `git diff` 确认无 api/tests/workflows 变更
2. 回填 task「### 自检结论（执行者）」表。
3. 落盘 **50** invoke + `reinspect_gov-l2-phase-c-design_20260527_v1.md`（扩写验收表）。
4. commit 后再执行 50。

### 硬约束
- 禁止凭记忆勾选。
- 不跑新增 pytest（本 round not_applicable）。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：30 · 执行编码
├── 交付：L2 §4.4 + TASK_TEMPLATE
└── 下一棒：40 · 自检
```
