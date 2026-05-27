# Invoke · 关账 · R2 · wiki-t4-r2-l0-align

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | CLOSE |
> | task | `docs/tasks/done/task_governance_wiki_t4_r2_l0_align_v1.md` |
> | task_slug | `wiki-t4-r2-l0-align` |
> | freeze_id | `GOV-T4-R2-L0-ALIGN@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |
> | cross_round_semi_auto | true |

---

## §1 关账结论

R2 T4 L0 对齐关账完成。全部 T4 相关验收通过；drift_check 为已知历史债务，非 R2 范围。

## §2 执行路线与 Commit 回溯

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 22 任务审核 | review + invoke 落盘 | `reviews/by-task/wiki-loop-t4-l2/*` | api-python@2f6431e |
| 2 | 30 执行编码 | VERIFY 全量重跑 + drift 记录 | `invoke_20260527_30_*` | api-python@e34aa6b |
| 3 | 40 自检 | VERIFY 5/6 pass + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | api-python@769b65e |
| 4 | 50 独立复检 | 重跑 VERIFY + 复检报告 + CLOSE_TRACE | `reinspect_*_20260527_v1.md` + `invoke_20260527_50_*` | api-python@018f76c |
| 5 | **关账** | git mv → done/ + _views 更新 | `done/task_*` + `_views/done.md` | api-python@576c3a7 |

### 分仓 Commit 索引

```text
### api-python（ai-ink-brain-api-python）
- 576c3a7 docs(task): R2 关账 — wiki-t4-r2-l0-align → done/ + _views 更新
- 018f76c docs(harness): 50 R2 独立复检 + CLOSE_TRACE
- 769b65e docs(harness): 40 R2 自检 + task 回填 + 50 下一棒 Prompt
- e34aa6b docs(harness): 30 R2 执行编码 invoke + 40 下一棒 Prompt
- 2f6431e docs(harness): 22 R2 任务审核落盘 + invoke
```

## §3 续跑 R3

按 LOOP_MANIFEST 与 cross_round_semi_auto 授权，R2 关账后同会话续 R3。

**R3 任务**：`docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md`
**R3 slug**：`gov-l2-r3-test-manifest`
**R3 freeze_id**：`GOV-L2-R3-TEST-MANIFEST@2026-05-27`

### R3 启动 Prompt

```text
你正在执行 Wiki Loop T4+L2 **R3** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/tasks/skills/SKILL-harness-loop-batch.md
- docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md
- semi_auto: true
- **commit（硬）**：每帽结束须 git commit（HANDOFF_AUTO_COMMIT）
- **invoke C2（硬）**：§3 ≥15 行 · 元信息含 task_slug · R3 与 R1 同级

【元信息】
- round: R3
- task: docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md
- task_slug: gov-l2-r3-test-manifest
- freeze_id: GOV-L2-R3-TEST-MANIFEST@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1
- 母 task: docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-t4-l2/
- cross_round_semi_auto: true

### R3 开工前检查
- [ ] R1 已在 `done/`（`docs/tasks/done/task_governance_wiki_t4_r1_pilot_v1.md`）
- [ ] R2 已在 `done/`（`docs/tasks/done/task_governance_wiki_t4_r2_l0_align_v1.md`）
- [ ] 读取 R3 task 全文 + 关联 SPEC
- [ ] 确认无 pending human_gate 阻塞

### 步骤 1 · 22
落盘 invoke：docs/harness/invokes/by-task/wiki-loop-t4-l2/invoke_YYYYMMDD_22_gov-l2-r3-test-manifest-v1.md
review：docs/harness/reviews/by-task/wiki-loop-t4-l2/task_<basename>_audit_R1_YYYYMMDD.md

### 步骤 2–4 · 30 / 40 / 50
按 R3 task §范围 交付；可新增 `_test_manifest.json`；不改 api/tests/prompts。
reinspect：docs/tasks/reinspect_results/reinspect_gov-l2-r3-test-manifest_YYYYMMDD_v1.md

### 步骤 5 · 关账
git mv → done/ · _views · RECENT §6.6 **done** 行
续跑：无（R3 为最后子 round）→ META 关账

硬约束：分支 task/gov-spec-t4-l2-v1 · 先 T4 后 L2 · C2 全绿
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：CLOSE · R2 关账
├── task：task_governance_wiki_t4_r2_l0_align_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：git mv → done/ + _views 更新 + CLOSE invoke 落盘
├── 下一棒：R3 · 22 任务审核（gov-l2-r3-test-manifest）
├── 推荐：—（按 MANIFEST 自动续跑）
└── 阻塞：无
```
