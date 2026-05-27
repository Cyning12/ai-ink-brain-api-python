# Invoke · 22 任务审核 · R1 · gov-t4-spec-active

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_t4_spec_active_v1.md` |
> | task_slug | `gov-t4-spec-active` |
> | freeze_id | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 母 Loop：`task_harness_wiki_loop_p2_followup_v1.md` · `HG-LOOP-BATCH` = **approved**（母单真值）。
- 下一棒：**30 执行编码**；落盘 review 后 **commit** 再切换（`HANDOFF_AUTO_COMMIT.md`）。

## §2 审查结论

**零阻塞。** 扩面 3 篇 synthesis 已含合法 `graph_nodes`；Bridge SPEC 可升格 **active**。详见 `docs/harness/reviews/by-task/wiki-loop-p2-followup/task_governance_t4_spec_active_v1_audit_R1_20260527.md`。

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R1** 的 **30 执行编码帽**。上一帽（22 任务审核）已结束；本帽只按下文执行。

【元信息】
- round: R1
- hat: 30
- task: docs/tasks/active/task_governance_t4_spec_active_v1.md
- task_slug: gov-t4-spec-active
- freeze_id: GOV-T4-SPEC-ACTIVE@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1
- 母 task: docs/tasks/active/task_harness_wiki_loop_p2_followup_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-p2-followup/
- cross_round_semi_auto: true

### 30 帽交付
1. [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../../../../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md)：`状态` **draft→active** · `freeze_id` → `GOV-T4-SPEC-ACTIVE@2026-05-27` · 修订记录 · §9 链出 ≥3 扩面 synthesis（含 `graph_nodes`）。
2. [`docs/spec/governance/README.md`](../../../../spec/governance/README.md)：T4 行 **active**。
3. [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../../../../tasks/RECENT_TASK_SCHEDULE.md) §6.6：P2 Loop → **in_progress** · T4 → **active**（保留 T4+L2 / expand done 行）。
4. [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../../../../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)：§2 / §4 / §5.1 T4 与 §5.2 P2 Loop 状态同步。
5. task 验收 `- [ ]` 预勾（40 最终确认）；`git add` 本轮路径 → `git commit`（message 含 freeze_id）。
6. 落盘 **40** invoke（§3 ≥15 行）。

### 硬约束
- 不改 api/、tests/、docs/harness/prompts/、CI workflow。
- 只读对照 `graph_query`（勿改 tools）。

### VERIFY（40 须重跑）
```bash
rg -n '^\\| \\*\\*状态\\*\\* \\|.*active' docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md
rg -n 'SPEC-Governance-Wiki-TechGraph-Bridge' docs/spec/governance/README.md
rg -n 'graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md docs/coding_wiki/syntheses/chatbi-v3-text2sql-tool-latency-obs.md docs/coding_wiki/syntheses/tech-graph-gate-d-v2-tasks.md
for id in C1 T2S CR1; do python tools/tech_graph_graph_query.py neighbors "$id" >/dev/null; echo "$id: $?"; done
python tools/tech_graph_graph_export.py --check
```
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_t4_spec_active_v1.md · audit_profile：post_close（继承）
├── 分支：task/wiki-loop-p2-followup-v1
├── human_gate：HG-LOOP-BATCH approved（母单）
├── 本棒交付：review + invoke 落盘
└── 下一棒：30 · 已落盘 §3 Prompt
```
