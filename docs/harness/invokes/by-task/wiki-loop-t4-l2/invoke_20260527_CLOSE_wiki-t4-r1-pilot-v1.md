# Invoke · 关账 · R1 · wiki-t4-r1-pilot

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | CLOSE |
> | task | `docs/tasks/done/task_governance_wiki_t4_r1_pilot_v1.md` |
> | task_slug | `wiki-t4-r1-pilot` |
> | freeze_id | `GOV-T4-R1-PILOT@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |
> | cross_round_semi_auto | true |

---

## §1 关账结论

R1 T4 Pilot 关账完成。全部验收通过，无阻塞。

## §2 执行路线与 Commit 回溯

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 30 执行编码 | graph_nodes + CODING_WIKI + 99_spec + RECENT | 4 文件修改 | api-python@f2f7505 |
| 2 | 22 任务审核 | review + invoke 落盘 | `reviews/by-task/wiki-loop-t4-l2/task_*_audit_R1_*.md` | api-python@b1afaf6 |
| 3 | 30 invoke | invoke 落盘 + 40 Prompt | `invoke_20260527_30_*` | api-python@e4a58d3 |
| 4 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | api-python@915566e |
| 5 | 50 独立复检 | 重跑 VERIFY + 复检报告 + CLOSE_TRACE | `reinspect_*_20260527_v1.md` + `invoke_20260527_50_*` | api-python@cd835ad |
| 6 | **关账** | git mv → done/ + _views 更新 | `done/task_*` + `_views/done.md` | api-python@e833d07 |

### 分仓 Commit 索引

```text
### api-python（ai-ink-brain-api-python）
- e833d07 docs(task): R1 关账 — wiki-t4-r1-pilot → done/ + _views 更新
- cd835ad docs(harness): 50 R1 独立复检 + CLOSE_TRACE
- 915566e docs(harness): 40 R1 自检 + task 回填 + 50 下一棒 Prompt
- e4a58d3 docs(harness): 30 R1 执行编码 invoke + 40 下一棒 Prompt
- f2f7505 docs(governance): R1 T4 Pilot 交付 — graph_nodes + CODING_WIKI + RECENT
- b1afaf6 docs(harness): 22 R1 任务审核落盘 + invoke
```

## §3 续跑 R2

按 LOOP_MANIFEST 与 cross_round_semi_auto 授权，R1 关账后同会话续 R2。

**R2 任务**：`docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md`
**R2 slug**：`wiki-t4-r2-l0-align`
**R2 freeze_id**：`GOV-T4-R2-L0-ALIGN@2026-05-27`

### R2 启动 Prompt

```text
你正在执行 Wiki Loop T4+L2 **R2** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/tasks/skills/SKILL-harness-loop-batch.md
- docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md
- semi_auto: true
- **commit（硬）**：每帽结束须 git commit（HANDOFF_AUTO_COMMIT）
- **invoke C2（硬）**：§3 ≥15 行 · 元信息含 task_slug · R2 与 R1 同级

【元信息】
- round: R2
- task: docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md
- task_slug: wiki-t4-r2-l0-align
- freeze_id: GOV-T4-R2-L0-ALIGN@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1
- 母 task: docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-t4-l2/
- cross_round_semi_auto: true

### R2 开工前检查
- [ ] R1 task 已在 `done/`（`docs/tasks/done/task_governance_wiki_t4_r1_pilot_v1.md`）
- [ ] 读取 R2 task 全文 + 关联 SPEC
- [ ] 确认无 pending human_gate 阻塞

### 步骤 1 · 22
落盘 invoke：docs/harness/invokes/by-task/wiki-loop-t4-l2/invoke_YYYYMMDD_22_wiki-t4-r2-l0-align-v1.md
review：docs/harness/reviews/by-task/wiki-loop-t4-l2/task_<basename>_audit_R1_YYYYMMDD.md

### 步骤 2–4 · 30 / 40 / 50
按 R2 task §范围 交付；不改 api/tests/prompts。
reinspect：docs/tasks/reinspect_results/reinspect_wiki-t4-r2-l0-align_YYYYMMDD_v1.md

### 步骤 5 · 关账
git mv → done/ · _views
续跑：R3 active path ≠ 无 且 cross_round 授权 → 下一 round

硬约束：分支 task/gov-spec-t4-l2-v1 · 先 T4 后 L2 · C2 全绿
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：CLOSE · R1 关账
├── task：task_governance_wiki_t4_r1_pilot_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：git mv → done/ + _views 更新 + CLOSE invoke 落盘
├── 下一棒：R2 · 22 任务审核（wiki-t4-r2-l0-align）
├── 推荐：—（按 MANIFEST 自动续跑）
└── 阻塞：无
```
