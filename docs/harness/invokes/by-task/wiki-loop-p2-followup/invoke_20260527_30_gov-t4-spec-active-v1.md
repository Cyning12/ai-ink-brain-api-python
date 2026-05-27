# Invoke · 30 执行编码 · R1 · gov-t4-spec-active

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_t4_spec_active_v1.md` |
> | task_slug | `gov-t4-spec-active` |
> | freeze_id | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **30 执行编码**（`docs/harness/prompts/hats/30-execute-code.md`）。
- 上一帽 22 零阻塞；本 round **docs-only**。
- 交付后 **commit**，再落盘 40 invoke。

## §2 交付摘要

| 文件 | 变更 |
| --- | --- |
| `SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` | `active` · freeze_id · §9.1 扩面索引 |
| `docs/spec/governance/README.md` | T4 行 active |
| `RECENT_TASK_SCHEDULE.md` §6.6 | P2 Loop in_progress · T4 active |
| `SPEC-Governance-Wiki-Harness-Roadmap-v1.md` | §2/§4/§5.1/§5.2 同步 |
| `task_governance_t4_spec_active_v1.md` | 范围项勾选 |

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R1** 的 **40 自检帽**。上一帽（30 执行编码）已结束。

【元信息】
- round: R1
- hat: 40
- task: docs/tasks/active/task_governance_t4_spec_active_v1.md
- task_slug: gov-t4-spec-active
- freeze_id: GOV-T4-SPEC-ACTIVE@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-p2-followup/

### 40 帽交付
1. **独立重跑** VERIFY（须有命令与 exit code）：
   - Bridge SPEC 头表 `active`
   - governance README T4 active
   - 3 篇 synthesis `graph_nodes:` 存在
   - `graph_query neighbors` 抽样 C1 T2S CR1 exit 0
   - `python tools/tech_graph_graph_export.py --check` exit 0
2. 回填 task「### 自检结论（执行者）」表。
3. 落盘 50 invoke（§3 ≥15 行）+ commit。

### 硬约束
- 禁止凭记忆勾选；无输出不 pass。
- 不改 api/tests/prompts/CI。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：30 · 执行编码
├── 下一棒：40 · 自检
└── VERIFY：交由 40 重跑
```
