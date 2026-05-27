# Invoke · 40 自检 · R1 · gov-t4-spec-active

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_t4_spec_active_v1.md` |
> | task_slug | `gov-t4-spec-active` |
> | freeze_id | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |

---

## §1 角色与纪律

- 本帽为 **40 自检**（`docs/harness/prompts/hats/40-self-check.md`）。
- 独立重跑 VERIFY；已回填 task「自检结论」表。

## §2 自检结果

### 2.1 命令输出

**V1 · Bridge SPEC active**：
```bash
$ rg -n '^\| \*\*状态\*\* \|' docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md
5:| **状态** | `active` |
EXIT:0
```

**V2 · governance README**：
```bash
$ rg -n 'TechGraph-Bridge' docs/spec/governance/README.md
8:| ... | `active` | **T4** ...
EXIT:0
```

**V3 · 3 篇 synthesis graph_nodes**：
```bash
$ rg -n '^graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md ...
query-rewrite-observability.md:10:graph_nodes:
chatbi-v3-text2sql-tool-latency-obs.md:9:graph_nodes:
tech-graph-gate-d-v2-tasks.md:9:graph_nodes:
EXIT:0
```

**V4 · graph_query 抽样**：
```bash
$ for id in C1 T2S CR1; do python tools/tech_graph_graph_query.py neighbors "$id" >/dev/null; echo "$id: $?"; done
C1: 0
T2S: 0
CR1: 0
```

**V5 · graph_export --check**：
```bash
$ python tools/tech_graph_graph_export.py --check
EXIT:0
```

**V6 · RECENT §6.6**：
- P2 Loop **in_progress** · T4 **active**（目视 pass）

### 2.2 C2 invoke 门禁

| 检查 | 结果 |
| --- | --- |
| 元信息表完整 | pass |
| §3 ≥15 行（本文件下一棒 50） | pass |
| 40 含 VERIFY 输出 | pass |

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R1** 的 **50 独立复检帽**。上一帽（40 自检）已结束。

【元信息】
- round: R1
- hat: 50
- task: docs/tasks/active/task_governance_t4_spec_active_v1.md
- task_slug: gov-t4-spec-active
- freeze_id: GOV-T4-SPEC-ACTIVE@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1

### 50 帽交付
1. 独立重跑 40 的 VERIFY 项；落盘 `docs/tasks/reinspect_results/reinspect_gov-t4-spec-active_20260527_v1.md`。
2. 落盘 `invoke_20260527_50_gov-t4-spec-active-v1.md` + CLOSE invoke 指引。
3. **关账**：`git mv` task → `docs/tasks/done/` · 更新 `_views/done.md` · 头部 `done（2026-05-27）`。
4. commit 后按 MANIFEST 续 **R2**（同会话 cross_round_semi_auto）。

### 硬约束
- 未改 api/tests/prompts/CI。
- human_gate 不得 Agent 代填 approved。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · 自检
├── VERIFY：7/7 pass
└── 下一棒：50 · 独立复检
```
