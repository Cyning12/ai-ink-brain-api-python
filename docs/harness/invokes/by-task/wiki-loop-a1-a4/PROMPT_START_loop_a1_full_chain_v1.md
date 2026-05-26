# 新 Agent 入口 · A1 全链 Loop（22→META · 仅粘贴一次）

> **用途**：`HG-LOOP-BATCH` = **approved** 后，**一条 user 消息**启动 A1，并 **授权同会话** 按 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) 续跑 A2→A3→A4→META。  
> **禁止** 把下文【授权】写进 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) 模板（模板只描述 **单 round**；跨 round 仅本入口 + 首份 invoke 快照）。  
> **分支（硬）**：`task/wiki-loop-a1-a4-v1` · Open **`ai-ink-brain-api-python/`**

| 项 | 值 |
|----|-----|
| **母 task** | `docs/tasks/done/task_harness_wiki_loop_a1_a4_v1.md` |
| **当轮** | A1 · 见 MANIFEST 第一行 |
| **Loop 真值** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) §3（A1 占位符已替换于 §2） |
| **commit 通则** | [`HANDOFF_AUTO_COMMIT.md`](../../../prompts/handoff/HANDOFF_AUTO_COMMIT.md) — **每帽交付后须 commit**，禁止只改盘不提交 |

---

## 1. 执行前自检

```bash
git branch --show-current   # 须 task/wiki-loop-a1-a4-v1
grep -n 'HG-LOOP-BATCH.*approved' docs/tasks/done/task_harness_wiki_loop_a1_a4_v1.md
test -f docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md || test -f docs/tasks/done/task_coding_wiki_ingest_test_strategy_v1.md
```

---

## 2. 【授权】跨 round semi_auto（会话级 · 只出现一次）

> 粘贴 §3 时 **须保留** 本段；Agent 落盘 **A1·22 invoke** 时将其写入 invoke 元信息表 `cross_round_semi_auto: true`。  
> **断点续跑**：读 **首份** 含该字段的 invoke，或用户明示「从 round=X 续跑全链」，**不必**每 round 重复粘贴。

```text
【授权】semi_auto 跨 round：A1 关账后无需停、无需人开新对话；按 LOOP_MANIFEST 依次执行 A2→A3→A4→META 关账。
每帽仍须：invoke §3 全文落盘 + 该帽工件（review/reinspect/task）+ git commit（见 HANDOFF_AUTO_COMMIT）。
cross-round 续跑 A2+ 时 invoke 质量 **与 A1·22 同级**（§3 ≥15 行 · 非 stub；见 SKILL §invoke 质量门禁）。
```

---

## 3. 可复制 Prompt（全文复制到**新对话**）

```text
你正在执行 Wiki Loop **A1** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/05-harness-semi-auto.mdc、06-harness-in-repo.mdc、07-git-workflow.mdc
- semi_auto: true（无 pending 闸时可同会话连跑）

【元信息】
- round: A1
- task: docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md
- task_slug: wiki-a1-ingest-test-strategy
- freeze_id: CODING-WIKI-A1-TEST-STRATEGY@2026-05-26
- git_branch: task/wiki-loop-a1-a4-v1
- 母 task: docs/tasks/done/task_harness_wiki_loop_a1_a4_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-a1-a4/
- cross_round_semi_auto: true

【授权】semi_auto 跨 round：A1 关账后无需停、无需人开新对话；按 LOOP_MANIFEST 依次执行 A2→A3→A4→META 关账。每帽仍须 invoke 落盘 + commit。

【invoke C2】A2+ 各帽 invoke 质量 = A1·22 同级；§3 ≥15 行、元信息表含 task_slug、非「交付摘要」（SKILL §invoke 质量门禁）。

【commit 硬纪律】每一帽（22/30/40/50/关账）结束 before 下一帽：git add 本轮路径 → commit（HEREDOC message）→ 回复末尾一行 `已提交：@ <short-hash>`。禁止跨帽堆积未提交改动。

（其余步骤与 docs/harness/invokes/by-task/wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md §3 相同；A1 步骤 0 跳过。关账后按 MANIFEST 自动续 A2，勿要求用户再贴 Prompt。）

硬约束：Open ai-ink-brain-api-python/ · 分支 task/wiki-loop-a1-a4-v1 · 单 PR 纪律 · 不改 api/tests/prompts/CI
```

> 完整逐步细则以 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) §3 为准；上框为 **A1 全链启动** 最小载荷 + 授权 + commit 强调。

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1：自 PROMPT_LOOP 迁出跨 round【授权】；全链只粘贴一次 |
| 2026-05-26 | v1.1：第三批 · invoke C2 / A2+ 不断质 |
