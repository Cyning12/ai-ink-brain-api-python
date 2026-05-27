# 新 Agent 入口 · 单 task 全链（22→关账 · 仅粘贴一次）

> **用途**：**gov-wiki-ingest-batch** · **10 slug** 批量 ingest。  
> **性质**：单 task · **长链授权** · 30 帽可连续写 10 页。  
> **分支**：`task/gov-wiki-ingest-batch-v1`

| 项 | 值 |
|----|-----|
| **task** | `docs/tasks/active/task_governance_wiki_ingest_batch_v1.md` |
| **SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-Ingest-Batch-v1.md` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH@2026-05-27` |

---

## 1. 执行前自检

```bash
git checkout -b task/gov-wiki-ingest-batch-v1 origin/main
grep 'HG-INGEST-BATCH-SCOPE.*approved' docs/tasks/active/task_governance_wiki_ingest_batch_v1.md
ls docs/coding_wiki/syntheses/ | wc -l   # 预期 5
```

---

## 2. 长链纪律

```text
同会话 22→关账。30 帽交付 SPEC §2 全部 10 slug。
禁止擅自增删名单（F5）。关账前 syntheses ≥15。
```

---

## 3. 可复制 Prompt

```text
你正在 ai-ink-brain-api-python 执行单 task gov-wiki-ingest-batch：**22 → 30 → 40 → 50 → 关账**。

【必读】
- docs/tasks/active/task_governance_wiki_ingest_batch_v1.md
- docs/spec/governance/SPEC-Governance-Wiki-Ingest-Batch-v1.md（§2 锁定表）
- docs/coding_wiki/CODING_WIKI.md §4.1 · §4.3
- docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md（graph_nodes 时）
- SKILL-harness-task · SKILL-docs-governance
- hats 22–50 · HANDOFF_*
- PROMPT_TASK_22_to_CLOSE_v1.md §3

【元信息】
task_slug: gov-wiki-ingest-batch
git_branch: task/gov-wiki-ingest-batch-v1
human_gate: 均已 approved（含 HG-INGEST-BATCH-SCOPE）

【30 · 10 slug 硬交付】
governance-l2-manifest-ci · governance-wiki-t4-expand · governance-l2-r3-test-manifest
harness-wiki-loop-t4-l2 · wiki-ctx-ab-v1 · coding-wiki-pilot
chatbi-v3-p2-health-ready · harness-wiki-loop-c2-verify · governance-wiki-t4-r1-pilot · wiki-ctx-ab-multi-slug
+ index.md + log.md（10 行）
每页：frontmatter · 摘要 · pointer · 建议 §测试变更 · 禁止 review 全文
graph_nodes 若有：graph_query neighbors exit 0

【VERIFY】
ls docs/coding_wiki/syntheses/*.md | wc -l  # ≥15
python -c "… index 含 10 slug …"  # 见 task §VERIFY
python tools/tech_graph_manifest_check.py

【长链】同会话做完；仅 F5/非法 graph_nodes/越 scope 可停。

现在开始 **22 帽**。
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：10 slug 批量 ingest 全链 |
