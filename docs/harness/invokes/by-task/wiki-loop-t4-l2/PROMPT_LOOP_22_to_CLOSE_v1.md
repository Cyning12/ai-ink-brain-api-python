# 启动 Prompt · Loop 执行 · 22 → 关账（v1 · 无 10）

> **单 round 模板** · 先读 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) 替换 §3 占位符。  
> **全链首次启动**：[`PROMPT_START_loop_t4_l2_full_chain_v1.md`](./PROMPT_START_loop_t4_l2_full_chain_v1.md)（【授权】**仅**在该文件）。  
> **Batch-10**：[`invoke_20260527_10_batch_t4_l2_v1.md`](./invoke_20260527_10_batch_t4_l2_v1.md) 已落盘 task。

---

## 1. 执行前替换表（粘贴 §3 前必改）

| 占位符 | R1 | R2 | R3 | META |
|--------|----|----|-----|------|
| `{{LOOP_ROUND}}` | R1 | R2 | R3 | META |
| `{{TASK_PATH}}` | `…/task_governance_wiki_t4_r1_pilot_v1.md` | `…/task_governance_wiki_t4_r2_l0_align_v1.md` | `…/task_governance_l2_r3_test_manifest_v1.md` | `…/task_harness_wiki_loop_t4_l2_v1.md` |
| `{{TASK_SLUG}}` | `wiki-t4-r1-pilot` | `wiki-t4-r2-l0-align` | `gov-l2-r3-test-manifest` | `wiki-loop-t4-l2` |
| `{{FREEZE_ID}}` | `GOV-T4-R1-PILOT@2026-05-27` | `GOV-T4-R2-L0-ALIGN@2026-05-27` | `GOV-L2-R3-TEST-MANIFEST@2026-05-27` | `WIKI-LOOP-T4-L2@2026-05-27` |
| `{{GIT_BRANCH}}` | `task/gov-spec-t4-l2-v1` | 同左 | 同左 | 同左 |
| `{{NEXT_TASK_PATH}}` | R2 active path | R3 active path | `无` | `无` |
| `{{PLACEHOLDER_ID}}` | `无` | `无` | `无` | `无` |
| `{{PREV_DONE_TASK}}` | `无` | R1 `done/` path | R2 `done/` path | 三轮均 `done/` |

---

## 2. 回合特例

| round | 22 开工前额外步骤 |
|-------|-------------------|
| **R1** | 母 `HG-LOOP-BATCH` = approved；Pilot = `query-rewrite-observability` |
| **R2** | R1 须在 `done/`；**禁止** 交付 `_test_manifest` |
| **R3** | R2 须在 `done/`；**本 round** RECENT §6.6 → done + `_views` + README 验收行 |
| **META** | 三轮子 task 均在 `done/`；关账母单 + `REPORT_completion_*` |

---

## 3. 可复制 Prompt 正文

```text
你正在执行 Wiki Loop T4+L2 **{{LOOP_ROUND}}** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/tasks/skills/SKILL-harness-loop-batch.md
- docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md（R1/R2）
- docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md（R3）
- semi_auto: true
- **commit（硬）**：每帽结束须 git commit（HANDOFF_AUTO_COMMIT）
- **invoke C2（硬）**：§3 ≥15 行 · 元信息含 task_slug · R2+ 与 R1 同级

【元信息】
- round: {{LOOP_ROUND}}
- task: {{TASK_PATH}}
- task_slug: {{TASK_SLUG}}
- freeze_id: {{FREEZE_ID}}
- git_branch: {{GIT_BRANCH}}
- 母 task: docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-t4-l2/

（步骤 0：{{PLACEHOLDER_ID}} = 无 → 跳过）

### 步骤 1 · 22
落盘 invoke：docs/harness/invokes/by-task/wiki-loop-t4-l2/invoke_YYYYMMDD_22_{{TASK_SLUG}}-v1.md
review：docs/harness/reviews/by-task/wiki-loop-t4-l2/task_<basename>_audit_R1_YYYYMMDD.md

### 步骤 2–4 · 30 / 40 / 50
按 {{TASK_PATH}} §范围 交付；R3 可新增 _test_manifest.json；不改 api/tests/prompts。
reinspect：docs/tasks/reinspect_results/reinspect_{{TASK_SLUG}}_YYYYMMDD_v1.md

### 步骤 5 · 关账
git mv → done/ · _views · **仅 R3 或 META**：RECENT §6.6 done
续跑：{{NEXT_TASK_PATH}} ≠ 无 且 cross_round 授权 → 下一 round

### 步骤 7 · 仅 META
REPORT_completion → docs/harness/invokes/by-task/wiki-loop-t4-l2/REPORT_completion_YYYYMMDD_v1.md

硬约束：分支 {{GIT_BRANCH}} · 先 T4 后 L2 · C2 全绿
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：T4+L2 · 3 round + META |
