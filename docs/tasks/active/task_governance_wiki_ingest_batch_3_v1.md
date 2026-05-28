# Task：治理 — Coding Wiki 批量 Ingest 第三批（5 slug · 单元 A · R3）

> **状态**：pending  
> **round**：**R3** · 母单 [`task_harness_wiki_loop_unit_a_v1.md`](task_harness_wiki_loop_unit_a_v1.md)  
> **SPEC**：[`SPEC-Governance-Wiki-Ingest-Batch-3-v1.md`](../spec/governance/SPEC-Governance-Wiki-Ingest-Batch-3-v1.md)

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Wiki ingest；§4.3 手工 lint；不改 pytest。 |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **semi_auto** | `true` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **task_slug** | `gov-wiki-ingest-batch-3` |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | pending | 22, 30 | **继承母单** |
| HG-INGEST-BATCH-3-SCOPE | pending | 30 | **继承母单** · 锁定 SPEC §1 五 slug |

---

## 背景与目标

Batch-2 后 syntheses **20** 篇。本 round 再 ingest **5 slug**，累计 **≥25**。

**完成态**：5 篇新页 · `index.md` / `log.md` · 新页优先补 `graph_nodes`（可与 R2 合并 commit，但 **验收** 以 syntheses 计数为准）。

---

## 范围（5 slug · 与 SPEC §1 一致）

| slug | 来源 task |
| --- | --- |
| `harness-wiki-loop-a1-a4` | `task_harness_wiki_loop_a1_a4_v1` |
| `harness-wiki-loop-bq3-recheck` | `task_harness_wiki_loop_bq3_recheck_v1` |
| `coding-wiki-ingest-test-strategy` | `task_coding_wiki_ingest_test_strategy_v1` |
| `governance-recent-schedule-wiki-sync` | `task_governance_recent_schedule_wiki_sync_v1` |
| `wiki-ctx-ab-multi-bq3-recheck` | `task_wiki_ctx_ab_multi_bq3_recheck_v1` |

## 非范围

- Batch-1/2 已有 slug 重做正文  
- `api/`、`tests/`、`tools/`

---

## 验收标准

- [ ] `HG-INGEST-BATCH-3-SCOPE` **approved**（母单）  
- [ ] `docs/coding_wiki/syntheses/` 文件数 **≥25**  
- [ ] R2 已在 `done/`  
- [ ] invoke C2 全绿 · **`done/`**

---

## 给 Cursor / Claude Code

`gov-wiki-ingest-batch-3`、`GOV-WIKI-INGEST-BATCH-3`、Loop R3
