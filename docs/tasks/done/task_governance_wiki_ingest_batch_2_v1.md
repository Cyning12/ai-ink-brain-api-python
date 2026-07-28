# Task：治理 — Coding Wiki 批量 Ingest 第二批（5 slug · P2 Loop · R3）

> **状态**：done（2026-05-27 · GOV-WIKI-INGEST-BATCH-2@2026-05-27）  
> **round**：**R3** · 母单 [`task_harness_wiki_loop_p2_followup_v1.md`](task_harness_wiki_loop_p2_followup_v1.md)  
> **SPEC**：[`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](../spec/governance/SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md) §3 · Batch-1 [`SPEC-Governance-Wiki-Ingest-Batch-v1.md`](../spec/governance/SPEC-Governance-Wiki-Ingest-Batch-v1.md)

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Wiki ingest；lint 用 CODING_WIKI §4；不改 pytest。 |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` |
| **semi_auto** | `true` |
| **git_branch** | `task/wiki-loop-p2-followup-v1` |
| **task_slug** | `gov-wiki-ingest-batch-2` |
| **wiki_delta** | `docs/coding_wiki` |
| **wiki_delta_note** | 存量迁移 · 本 task 触及 docs/coding_wiki（2.18 wiki_delta） |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **pending** | 22, 30 | **继承母单** · **R2 须在 done/** |
| HG-INGEST-BATCH-2-SCOPE | **pending** | 30 | **继承母单** · **锁定** §3 slug 表 · R3·30 前须 approved |

> 改 `pending`/`approved` **只改母单** [`task_harness_wiki_loop_p2_followup_v1.md`](task_harness_wiki_loop_p2_followup_v1.md) `human_gate` 表。

---

## 背景与目标

Batch-1 后 syntheses **15** 篇。本 round 再 ingest **5 slug**，累计 **≥20**，优先 **治理线 done task**（AB-REP、读序、ingest 元 task 等）。

**完成态**：5 篇新 synthesis · `index.md` / `log.md` · lint 通过。

---

## 范围（5 slug · 与 P2 SPEC §3 草案一致 · R3 30 前锁定）

| slug | 来源 task |
| --- | --- |
| `wiki-ctx-ab-representative` | `task_governance_wiki_ctx_ab_representative_v1` |
| `governance-wiki-agent-readorder` | `task_governance_wiki_agent_readorder_v1` |
| `governance-wiki-ingest-batch` | `task_governance_wiki_ingest_batch_v1` |
| `harness-wiki-loop-t4-l2` | `task_harness_wiki_loop_t4_l2_v1` |
| `coding-wiki-t1c-test-archive` | `task_coding_wiki_t1c_test_archive_v1` |

## 非范围

- Batch-1 已 ingest slug **重复**  
- 前端 task ingest  

---

## 验收标准

- [x] `HG-INGEST-BATCH-2-SCOPE` **approved**（母单）  
- [x] syntheses 文件数 **≥20**（20）  
- [x] invoke C2 全绿 · task **`done/`**  

---

## 给 Cursor

`gov-wiki-ingest-batch-2`、`GOV-WIKI-INGEST-BATCH-2`、Loop R3
