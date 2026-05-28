# 22 任务审核 — gov-wiki-t4-rollout · R1

| 项 | 值 |
| --- | --- |
| **task** | `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md` |
| **task_slug** | `gov-wiki-t4-rollout` |
| **freeze_id** | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| **round** | R2（单元 A） |
| **audit_profile** | post_close |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **human_gate** | HG-LOOP-BATCH approved（母单） |
| **review_date** | 2026-05-28 |

---

## 审查结论摘要

**零阻塞 · 可进入 30 执行帽**

本 task 为 T4 `graph_nodes` frontmatter 铺量，范围清晰（14 篇 synthesis），test_strategy: not_applicable 合理。R1 已在 `done/`。

---

## 已核对项

| # | 检查项 | 结论 | 说明 |
| --- | --- | --- | --- |
| 1 | human_gate | pass | 母单 HG-LOOP-BATCH = approved |
| 2 | 范围 | pass | 仅改 `docs/coding_wiki/syntheses/` frontmatter；不改 api/tests/tools |
| 3 | 前置 R1 | pass | `task_governance_wiki_docs_hygiene_v1.md` 已 `done/` |
| 4 | T4 SPEC | pass | `SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` active；§3 `graph_nodes` 规格清晰 |
| 5 | 铺量清单 | pass | 14 篇无 graph_nodes；6 篇已有（跳过） |
| 6 | failure_paths | pass | F1（id 不存在 graph_v2）→ graph_query 验证；F2（Wiki 替代影响分析）→ 22/50 阻塞 |

---

## 阻塞 / 非阻塞

**非阻塞**。

---

## 签收 / 关闭

**结论：可执行**

14 篇 synthesis 补 `graph_nodes`（种子 id 或 `[]` 标注纯叙事）。建议 30 执行时：
1. 优先用 `graph_query neighbors <id>` 验证 id 存在性
2. `relation` 用 §3.1 枚举（documents/evidence/triggers 等）
3. 每篇改后自核 frontmatter YAML 格式

---

## 下一棒可复制 Prompt

```text
执行 Wiki Loop 单元 A · R2 · 30→40→50→关账。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only · 禁止 api/tests/tools。

task: docs/tasks/active/task_governance_wiki_t4_rollout_v1.md
task_slug: gov-wiki-t4-rollout
freeze_id: GOV-WIKI-T4-ROLLOUT@2026-05-28
semi_auto: true

**范围（14 篇 synthesis 补 graph_nodes frontmatter）**

1. 读取每篇无 graph_nodes 的 synthesis（docs/coding_wiki/syntheses/*.md）
2. 根据内容判断：
   a) 有明确 L0 关联 → 补 `graph_nodes: [{id: ..., relation: ...}]`
   b) 纯叙事/概念页 → `graph_nodes: []` + 文内一句「纯叙事 · 无 L0 种子」
3. `graph_nodes[].id` 须用 `python tools/tech_graph_graph_query.py neighbors <id>` 验证存在性
4. `relation` 用 SPEC §3.1 枚举（documents / evidence / triggers / gates / archives / yields / branches / merges / signoff）

**铺量清单（当前无 graph_nodes）**
- wiki-ctx-ab-representative → 建议 `rag-unified-chat-stream` 或实验轨节点
- harness-wiki-loop-p2-followup → 建议 `flow-rag-recall`（叙事）
- governance-wiki-ingest-batch → 建议 `CR1`
- governance-wiki-agent-readorder → `[]` 纯叙事
- coding-wiki-t1c-test-archive → `[]` 纯叙事
- wiki-ctx-ab-v1 → 建议 `RAG`
- wiki-ctx-ab-multi-slug → 建议 `CR1`
- harness-wiki-loop-c2-verify → 建议 `E2E_DOC`
- coding-wiki-pilot → 建议 `RAG_DOC`
- chatbi-v3-p2-health-ready → 建议 `T2S`
- harness-p1-docs-consolidation → `[]` 纯叙事
- docs-tasks-reorg-move → `[]` 纯叙事
- governance-l2-r3-test-manifest → 对齐 manifest 锚点
- governance-l2-manifest-ci → 对齐 manifest 锚点

**执行纪律**
- 不改 synthesis 正文内容
- 不改 api/tests/tools
- 每篇改后用 `rg -n '^graph_nodes:'` 验证 frontmatter 格式
- 至少 3 次 `graph_query neighbors` 留证
- invoke C2：每帽 §3 ≥15 行
- 每帽 commit 后再戴下一帽
```
