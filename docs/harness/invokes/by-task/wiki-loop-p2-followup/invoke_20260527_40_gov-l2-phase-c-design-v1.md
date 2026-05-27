# Invoke · 40 自检 · R2 · gov-l2-phase-c-design

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_l2_phase_c_design_v1.md` |
> | task_slug | `gov-l2-phase-c-design` |
> | freeze_id | `GOV-L2-PHASE-C-DESIGN@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |

---

## §1 角色与纪律

- 本帽为 **40 自检**（`docs/harness/prompts/hats/40-self-check.md`）。
- 禁止凭记忆声称「测过」；无命令输出不勾选。

## §2 自检结果

### 2.1 命令输出

**V1 · §4.4 存在**：
```bash
$ rg -n '### 4\.4 Phase C' docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md
152:### 4.4 Phase C（design · `GOV-L2-PHASE-C-DESIGN@2026-05-27`）
EXIT:0
```

**V2 · TASK_TEMPLATE pointer**：
```bash
$ rg -n '§4\.4' docs/tasks/templates/TASK_TEMPLATE.md
83:> **L2 Phase C（设计）**：`F#` 与 `_test_manifest.json` ...
EXIT:0
```

**V3 · _test_manifest.json**：
```bash
$ python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); print('entries', len(m['entries']))"
entries 12
EXIT:0
```

**V4 · docs-only diff**：
```bash
$ git diff --name-only bdde202..HEAD | rg '^(api/|tests/|\.github/workflows/)' || echo 'no api/tests/ci'
no api/tests/ci
EXIT:0
```

### 2.2 验收表

| 检查项 | 结果 |
| --- | --- |
| §4.4 可读、可立项 | **pass** |
| 示例映射 ≥2 | **pass**（§4.4.3 三行） |
| 未改 tools/CI | **pass** |
| R1 前置 done | **pass** |

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R2** 的 **50 独立复检帽**。上一帽（40 自检）已结束。

【元信息】
- round: R2
- hat: 50
- task: docs/tasks/active/task_governance_l2_phase_c_design_v1.md
- task_slug: gov-l2-phase-c-design
- freeze_id: GOV-L2-PHASE-C-DESIGN@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1

### 50 帽交付
1. 独立重跑 40 VERIFY；更新 `docs/tasks/reinspect_results/reinspect_gov-l2-phase-c-design_20260527_v1.md`（逐项证据）。
2. 落盘本 invoke §3 关账 Prompt。
3. **关账**：`git mv` → `docs/tasks/done/` · `_views/done.md` · `invoke_*_CLOSE_*`。
4. commit 后按 cross_round_semi_auto 启动 **R3·22**。

### 硬约束
- human_gate 不得 Agent 代填 approved。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · 自检
├── VERIFY：4/4 pass
└── 下一棒：50
```
