# 新 Agent 入口 · 单 task 全链（22→关账 · 仅粘贴一次）

> **用途**：**gov-wiki-agent-readorder** · 后端 Agent Coding Wiki **必读链常模化**。  
> **性质**：单 task · **长链授权** · 非 Loop Batch。  
> **分支**：`task/gov-wiki-agent-readorder-v1` · Open **`ai-ink-brain-api-python/`**

| 项 | 值 |
|----|-----|
| **task** | `docs/tasks/active/task_governance_wiki_agent_readorder_v1.md` |
| **SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md` |
| **freeze_id** | `GOV-WIKI-AGENT-READORDER@2026-05-27` |
| **帽链** | [`PROMPT_TASK_22_to_CLOSE_v1.md`](./PROMPT_TASK_22_to_CLOSE_v1.md) §3 |

---

## 1. 执行前自检

```bash
git fetch origin main
git checkout -b task/gov-wiki-agent-readorder-v1 origin/main
grep 'approved' docs/tasks/active/task_governance_wiki_agent_readorder_v1.md | head -5
test -f docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md
```

---

## 2. 长链纪律（人已预批闸）

```text
同会话 22→关账；每帽 invoke §3 ≥15 行 + commit。
无新 pending 人闸前禁止停。
关账前 ST1–ST6。
```

---

## 3. 可复制 Prompt

```text
你正在 ai-ink-brain-api-python 执行单 task gov-wiki-agent-readorder：**22 → 30 → 40 → 50 → 关账**（跳过 10）。

【必读】
- docs/tasks/active/task_governance_wiki_agent_readorder_v1.md
- docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md
- docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md §3
- docs/tasks/skills/SKILL-harness-task.md · SKILL-docs-governance.md
- docs/harness/prompts/hats/22 … 50 · HANDOFF_SEMI_AUTO · HANDOFF_AUTO_COMMIT · HANDOFF_CLOSE_TRACE
- docs/harness/invokes/by-task/gov-wiki-agent-readorder/PROMPT_TASK_22_to_CLOSE_v1.md §3

【元信息】
task_slug: gov-wiki-agent-readorder
git_branch: task/gov-wiki-agent-readorder-v1
semi_auto: true · test_strategy: not_applicable
human_gate: HG-TASK-DRAFT · HG-AUDIT-R1 · HG-READORDER-WORDING 均已 approved

【30 交付】
- AGENTS.md 必读链插入 Coding Wiki（SPEC §2.3）
- 推荐 .cursor/rules/11-coding-wiki-readorder.mdc + gen_agents_md.py
- CODING_WIKI.md §7 一句同步
- 非范围：ingest 批量 · api · tests · 前端

【VERIFY】
rg -n 'coding_wiki|Coding Wiki' AGENTS.md
python tools/tech_graph_manifest_check.py

【长链】禁止跳帽；仅 F* / manifest fail / 越 scope 可停。

现在开始 **22 帽**。
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：读序常模化全链 |
