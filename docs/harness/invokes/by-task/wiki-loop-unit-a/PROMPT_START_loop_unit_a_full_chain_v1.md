# 新 Agent 入口 · 单元 A 全链（cc · R1→META · 仅粘贴一次）

> **用途**：母单 `docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md` 中 **`HG-LOOP-BATCH` = `approved`**（文件内可见，非对话声明）后，一条 user 消息启动 R1，并授权同会话续跑 R2→R3→META。  
> **分支（硬）**：`task/wiki-unit-ab-plan-v1` · Open **`ai-ink-brain-api-python/`**  
> **平台**：**Claude Code** — 须显式 `@` 下列 SKILL（无 `.mdc` 自动注入）

| 项 | 值 |
|----|-----|
| **母 task** | `docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md` |
| **Unit AB SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md` |
| **SKILL** | `docs/tasks/skills/SKILL-harness-loop-batch.md` · **第六轮** · **§执行铁律** |
| **MANIFEST** | `./LOOP_MANIFEST.md` |

---

## 1. 执行前自检（Gate · 非 0 则禁止粘贴 §3）

```bash
git branch --show-current   # 须 task/wiki-unit-ab-plan-v1

# 母单闸须为 approved（pending 则停，勿开工）
grep -E 'HG-LOOP-BATCH.*approved' docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md \
  || { echo 'BLOCK: HG-LOOP-BATCH not approved on mother task'; exit 1; }

# R3 前另验（R1/R2 可跳过本行）
# grep -E 'HG-INGEST-BATCH-3-SCOPE.*approved' docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md

test -f docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md
test -f docs/harness/invokes/by-task/wiki-loop-unit-a/PROMPT_LOOP_22_to_CLOSE_v1.md
```

---

## 2. 【授权】跨 round semi_auto（会话级 · 只出现一次）

> **前提**：§1 Gate 自检已通过（母单 `HG-LOOP-BATCH` = **approved**）。

```text
【授权】semi_auto 跨 round：R1 关账后无需停；按 LOOP_MANIFEST 执行 R2→R3→META。
每帽仍须：invoke §3 全文落盘 + git commit（HANDOFF_AUTO_COMMIT）。
顺序硬约束：R1→R2→R3；R3 启动前母单 HG-INGEST-BATCH-3-SCOPE 须为文件内 approved（非口头）。
本 Epic 交付 PR-A（docs-only）；禁止改 api/tests/tools。
关账后建议新增 skill_cross_platform_v1 case：wiki-loop-unit-a_claude-code_<date>（含 ST0 Gate）。
```

---

## 3. 可复制 Prompt（全文复制到新对话 · cc）

```text
【步骤 0 · Gate 验证 — 未通过则仅输出阻塞状态栏并结束，禁止 22/30/invoke】
1. 打开 docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md（R1 子 task）
2. 打开 docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md（母 task · 继承闸真值）
3. 扫描两文件 human_gate：任一 relevant gate 为 pending 且 blocks 含 22 → 硬停（HANDOFF_SEMI_AUTO §2.3 · SKILL-harness-loop-batch §执行铁律）

【步骤 1 起 · 仅 Gate 通过后】
你正在执行 Wiki Loop 单元 A（第六轮）**R1** 帽链：22 → 30 → 40 → 50 → 关账（无 10）。

必读（请用 @ 或 Read 打开）：
- docs/tasks/skills/SKILL-harness-loop-batch.md（含 §执行铁律）
- docs/tasks/skills/SKILL-docs-governance.md
- docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/invokes/by-task/wiki-loop-unit-a/LOOP_MANIFEST.md
- docs/harness/invokes/by-task/wiki-loop-unit-a/PROMPT_LOOP_22_to_CLOSE_v1.md

【元信息】
- round: R1
- task: docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md
- mother_task: docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md
- task_slug: gov-wiki-docs-hygiene
- git_branch: task/wiki-unit-ab-plan-v1
- freeze_id: GOV-WIKI-DOCS-HYGIENE@2026-05-28
- semi_auto: true

R1 关账后继续 R2→R3→META（见 MANIFEST）。R3 前须母单 HG-INGEST-BATCH-3-SCOPE 为文件内 approved。
```
