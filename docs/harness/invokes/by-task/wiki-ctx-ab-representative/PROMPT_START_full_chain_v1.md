# 新 Agent 入口 · Wiki-CTX-AB 代表性扩面（22→关账）

> **用途**：6 slug · H-lean vs W · 前端 P1-4 **证据轨**  
> **分支**：`task/wiki-ctx-ab-representative-v1`

| 项 | 值 |
|----|-----|
| **task** | `docs/tasks/active/task_governance_wiki_ctx_ab_representative_v1.md` |
| **SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-CTX-AB-Representative-v1.md` |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |

---

## 1. 自检

```bash
git fetch origin main
git checkout -b task/wiki-ctx-ab-representative-v1 origin/main
grep 'HG-AB-REP-SLUGS.*approved' docs/tasks/active/task_governance_wiki_ctx_ab_representative_v1.md
ls docs/coding_wiki/syntheses/*.md | wc -l   # ≥15
```

---

## 2. 长链纪律

同会话 22→关账；30 帽可分批 commit（物化 / 填表 / 结论文）；禁止改 6 slug。

---

## 3. 可复制 Prompt

```text
你正在 ai-ink-brain-api-python 执行单 task wiki-ctx-ab-representative：**22 → 30 → 40 → 50 → 关账**。

【必读】
- docs/tasks/active/task_governance_wiki_ctx_ab_representative_v1.md
- docs/spec/governance/SPEC-Governance-Wiki-CTX-AB-Representative-v1.md
- docs/harness/experiments/wiki_ctx_ab_representative_v1/questions.md
- docs/harness/experiments/wiki_ctx_ab_v1/payloads/TEMPLATE-H-lean.md · TEMPLATE-W.md
- docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md（基线）
- docs/tasks/done/task_wiki_ctx_ab_multi_slug_v1.md（2 slug 先例）
- SKILL-harness-task · SKILL-docs-governance
- hats 22–50 · HANDOFF_*
- PROMPT_TASK_22_to_CLOSE_v1.md §3

【元信息】
task_slug: wiki-ctx-ab-representative
git_branch: task/wiki-ctx-ab-representative-v1
human_gate: 均已 approved（含 HG-AB-REP-SLUGS · HG-AB-REP-RUN）

【30 交付】
1. 物化 12 payloads：H-lean_<slug>.md · W_<slug>.md（6 slug 见 SPEC §2.1）
2. 每 slug Q1–Q4 × H-lean × W 填 scorecard.md
3. 聚合 T7（≥5/6 slug 降幅≥30%）· T8（≥5/6 slug ≥3/4）
4. conclusion_representative_zh.md（签收/局限/前端 P1-4 建议）
5. WIKI_REQUIREMENTS_COMPARISON #46 更新
非范围：前端仓 · api · 新 ingest

【VERIFY】
ls …/payloads/H-lean_*.md | wc -l  # 6
ls …/payloads/W_*.md | wc -l       # 6
test -f …/conclusion_representative_zh.md

【长链】同会话；F1–F4 可停。

现在开始 **22 帽**。
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：6 slug 代表性 AB 全链 |
