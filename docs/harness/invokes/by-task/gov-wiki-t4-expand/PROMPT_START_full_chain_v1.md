# 新 Agent 入口 · 单 task 全链（22→关账 · 仅粘贴一次）

> **用途**：`human_gate` 已 **approved** 后，**一条 user 消息**启动 **gov-wiki-t4-expand** 完整帽链。  
> **性质**：**单 task**（`SKILL-harness-task`）· **非** Loop Batch · 无 `HG-LOOP-BATCH` / `LOOP_MANIFEST`。  
> **分支（硬）**：`task/gov-wiki-t4-expand-v1` · Open **`ai-ink-brain-api-python/`**

| 项 | 值 |
|----|-----|
| **task** | `docs/tasks/active/task_governance_wiki_t4_expand_v2.md` |
| **task_slug** | `gov-wiki-t4-expand` |
| **freeze_id** | `GOV-T4-EXPAND@2026-05-27` |
| **SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` |
| **帽链真值** | [`PROMPT_TASK_22_to_CLOSE_v1.md`](./PROMPT_TASK_22_to_CLOSE_v1.md) §3 |
| **SKILL** | [`SKILL-harness-task.md`](../../../tasks/skills/SKILL-harness-task.md) · [`SKILL-docs-governance.md`](../../../tasks/skills/SKILL-docs-governance.md) |

---

## 1. 执行前自检

```bash
git fetch origin main
git checkout -b task/gov-wiki-t4-expand-v1 origin/main   # 或从含 task 草案的分支拉出
git branch --show-current   # 须 task/gov-wiki-t4-expand-v1

grep 'HG-TASK-DRAFT.*approved' docs/tasks/active/task_governance_wiki_t4_expand_v2.md
grep 'HG-AUDIT-R1.*approved' docs/tasks/active/task_governance_wiki_t4_expand_v2.md

test -f docs/tasks/active/task_governance_wiki_t4_expand_v2.md
test -f docs/coding_wiki/syntheses/query-rewrite-observability.md
test -f docs/harness/invokes/by-task/gov-wiki-t4-expand/PROMPT_TASK_22_to_CLOSE_v1.md
```

---

## 2. semi_auto（单 task · 无 cross-round）

```text
本 Epic 为单 task：22→30→40→50→关账 同会话连续执行，无需新对话。
每帽仍须：invoke §3 全文（≥15 行 · 元信息含 task_slug）+ 该帽工件 + git commit（HANDOFF_AUTO_COMMIT）。
禁止 stub：30/40/50 与 22 同级 invoke 质量（对齐 Loop C2 门禁 · 见 SKILL-harness-task）。
```

---

## 3. 可复制 Prompt（全文复制到 Claude Code / 新对话）

```text
你正在 ai-ink-brain-api-python 执行 **单 task** gov-wiki-t4-expand 帽链：**22 → 30 → 40 → 50 → 关账**（**跳过 10**）。

【必读 · 显式打开路径 · Claude Code 无 .mdc 自动加载】
- docs/tasks/active/task_governance_wiki_t4_expand_v2.md
- docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md
- docs/tasks/skills/SKILL-harness-task.md
- docs/tasks/skills/SKILL-docs-governance.md
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/invokes/by-task/gov-wiki-t4-expand/PROMPT_TASK_22_to_CLOSE_v1.md §3

【元信息】
- task_slug: gov-wiki-t4-expand
- task: docs/tasks/active/task_governance_wiki_t4_expand_v2.md
- freeze_id: GOV-T4-EXPAND@2026-05-27
- git_branch: task/gov-wiki-t4-expand-v1
- semi_auto: true
- test_strategy: not_applicable
- invoke 目录: docs/harness/invokes/by-task/gov-wiki-t4-expand/
- review 目录: docs/harness/reviews/by-task/gov-wiki-t4-expand/
- human_gate: HG-TASK-DRAFT approved · HG-AUDIT-R1 approved

【semi_auto】同会话连续 22→关账；每帽 invoke + commit 后再换帽。

【invoke 质量 · 硬】
- 各 invoke §3 ≥15 行；元信息表含 task_slug、freeze_id、git_branch
- 禁止仅写「交付摘要 + commit」式 stub

【commit 硬纪律】每帽结束 before 下一帽：git add → commit → 回复「已提交：<short-hash>」

【30 帽交付摘要】
- graph_nodes 扩面 2 篇：
  - docs/coding_wiki/syntheses/chatbi-v3-text2sql-tool-latency-obs.md
  - docs/coding_wiki/syntheses/tech-graph-gate-d-v2-tasks.md
- 仓内 ≥3 篇 synthesis 含 graph_nodes（含 Pilot query-rewrite-observability）
- 每个 graph_nodes[].id：python tools/tech_graph_graph_query.py neighbors <id> → exit 0
- CODING_WIKI.md T4 覆盖说明；RECENT §6.6 T4 行 + §8 修订
- 非范围：api/ tests/ workflow / _test_manifest 脚本

【50 + 关账】
- reinspect: docs/tasks/reinspect_results/reinspect_gov-wiki-t4-expand_YYYYMMDD_v1.md
- git mv task → docs/tasks/done/（与 done 头部同 commit）
- docs/tasks/_views/done.md 一行
- docs-governance hygiene H1–H5
- 关账后输出 HANDOFF_CLOSE_TRACE

【VERIFY】
rg -l '^graph_nodes:' docs/coding_wiki/syntheses/
python tools/tech_graph_manifest_check.py
python tools/tech_graph_graph_export.py --check

硬约束：docs-only · 不改 api/tests/prompts/CI · 禁止手改 graph.json

现在开始：确认分支 task/gov-wiki-t4-expand-v1，执行 **22 帽**（review + invoke_YYYYMMDD_22_*）。
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：单 task 全链 · Claude Code · SKILL-harness-task |
