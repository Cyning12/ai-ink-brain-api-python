# 新 Agent 入口 · R1 全链 Loop（22→META · 仅粘贴一次）

> **用途**：`HG-LOOP-BATCH` = **approved** 后，**一条 user 消息**启动 R1，并 **授权同会话** 按 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) 续跑 R2→R3→META。  
> **分支（硬）**：`task/gov-spec-t4-l2-v1` · Open **`ai-ink-brain-api-python/`**

| 项 | 值 |
|----|-----|
| **母 task** | `docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md` |
| **当轮** | R1 · 见 MANIFEST 第一行 |
| **Loop 真值** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) §3 |
| **SKILL** | [`docs/tasks/skills/SKILL-harness-loop-batch.md`](../../../tasks/skills/SKILL-harness-loop-batch.md) · 第四轮 · **T4+L2** |

---

## 1. 执行前自检

```bash
git branch --show-current   # 须 task/gov-spec-t4-l2-v1
grep -n 'HG-LOOP-BATCH.*approved' docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md
test -f docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md
test -f docs/harness/invokes/by-task/wiki-loop-t4-l2/PROMPT_LOOP_22_to_CLOSE_v1.md
test -f docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md
```

---

## 2. 【授权】跨 round semi_auto（会话级 · 只出现一次）

```text
【授权】semi_auto 跨 round：R1 关账后无需停、无需人开新对话；按 LOOP_MANIFEST 依次执行 R2→R3→META 关账。
每帽仍须：invoke §3 全文落盘 + 该帽工件 + git commit（见 HANDOFF_AUTO_COMMIT）。
cross-round 续跑 R2+ 时 invoke 质量与 R1·22 同级（§3 ≥15 行 · 非 stub；见 SKILL §invoke 质量门禁）。
顺序硬约束：先 T4（R1→R2）再 L2（R3）；禁止 R3 先于 R2 开工。
```

---

## 3. 可复制 Prompt（全文复制到**新对话**）

```text
你正在执行 Wiki Loop T4+L2 **R1** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/tasks/skills/SKILL-harness-loop-batch.md
- docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md
- semi_auto: true

【元信息】
- round: R1
- task: docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md
- task_slug: wiki-t4-r1-pilot
- freeze_id: GOV-T4-R1-PILOT@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1
- 母 task: docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-t4-l2/
- cross_round_semi_auto: true
- pilot_synthesis: docs/coding_wiki/syntheses/query-rewrite-observability.md

【授权】semi_auto 跨 round：R1 关账后按 MANIFEST 续 R2→R3→META。每帽 invoke + commit。

【commit 硬纪律】每帽结束 before 下一帽：git add → commit → 回复 `已提交：@ <short-hash>`。

（其余步骤与 docs/harness/invokes/by-task/wiki-loop-t4-l2/PROMPT_LOOP_22_to_CLOSE_v1.md §3 相同；替换表 round=R1；步骤 0 跳过；META 后步骤 7 落盘 REPORT_completion。）

硬约束：单 PR · 不改 api/tests/prompts/CI · Pilot 仅 query-rewrite-observability · T4 先于 L2
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：第四 Loop T4+L2 全链启动 |
