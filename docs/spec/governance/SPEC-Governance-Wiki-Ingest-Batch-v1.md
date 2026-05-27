# SPEC — 治理：Coding Wiki 批量 Ingest（v1 · 10 slug）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH@2026-05-27` |
| **Roadmap** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) · T1b/T1c 之后 **扩面** |
| **Schema** | [`docs/coding_wiki/CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) §4.1 Ingest · §4.3 Lint |
| **T4** | [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md)（已有 `graph_nodes` 的页 **保持/补全** frontmatter） |
| **执行 task** | [`task_governance_wiki_ingest_batch_v1.md`](../../tasks/active/task_governance_wiki_ingest_batch_v1.md) |

---

## 0. 完成态（一句话）

在 **不复制** L1 全文、**不改** `api/tests/workflow` 前提下，为 **10 个** 已锁定的高价值 `docs/tasks/done/` Epic 新增或补齐 `docs/coding_wiki/syntheses/<slug>.md`，同步 `index.md` · `log.md`，并通过 CODING_WIKI §4.3 lint 纪律。

---

## 1. 背景与目标

| 现状 | 目标 |
| --- | --- |
| syntheses **5** 页 · done task **70+** | 本批次后 syntheses **≥15** 页（含既有 5） |
| AB 仅单/双 slug | 扩大 **代表性** 载荷，支撑后续「扩面 AB」 |
| ingest 靠零散 task | **一批次** 锁定名单 + 统一 lint |

---

## 2. 锁定 ingest 名单（10 · 本批次硬交付）

> **已有 synthesis 的 done task 不要求重做**（见 §2.1）。下表为 **须新建或补齐** 的 10 项。

| # | done task（相对子仓根） | slug | 主题 |
| --- | --- | --- | --- |
| 1 | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md` | `governance-l2-manifest-ci` | L2 Phase B · manifest CI |
| 2 | `docs/tasks/done/task_governance_wiki_t4_expand_v2.md` | `governance-wiki-t4-expand` | T4 扩面 3 slug |
| 3 | `docs/tasks/done/task_governance_l2_r3_test_manifest_v1.md` | `governance-l2-r3-test-manifest` | Loop R3 manifest 草案 |
| 4 | `docs/tasks/done/task_harness_wiki_loop_t4_l2_v1.md` | `harness-wiki-loop-t4-l2` | T4+L2 Loop 母单 |
| 5 | `docs/tasks/done/task_wiki_ctx_ab_v1.md` | `wiki-ctx-ab-v1` | Wiki-CTX-AB P1+P2 |
| 6 | `docs/tasks/done/task_coding_wiki_pilot_v1.md` | `coding-wiki-pilot` | T1b pilot |
| 7 | `docs/tasks/done/task_chatbi_v3_p2_resilience_health_ready_v1.md` | `chatbi-v3-p2-health-ready` | P2-1a health/ready |
| 8 | `docs/tasks/done/task_harness_wiki_loop_c2_verify_v1.md` | `harness-wiki-loop-c2-verify` | Loop C2 |
| 9 | `docs/tasks/done/task_governance_wiki_t4_r1_pilot_v1.md` | `governance-wiki-t4-r1-pilot` | T4 R1 Pilot |
| 10 | `docs/tasks/done/task_wiki_ctx_ab_multi_slug_v1.md` | `wiki-ctx-ab-multi-slug` | Multi-slug AB |

### 2.1 已有 synthesis（本批次跳过正文重做）

| slug | 已有页 |
| --- | --- |
| `query-rewrite-observability` | ✅ |
| `chatbi-v3-text2sql-tool-latency-obs` | ✅ |
| `harness-p1-docs-consolidation` | ✅ |
| `tech-graph-gate-d-v2-tasks` | ✅ |
| `docs-tasks-reorg-move` | ✅ |

若上表 10 项中某 slug 文件 **已存在**（不应发生），30 帽 **仅** 补 index/log/缺段，并在 invoke 注明 **skip body**。

---

## 3. 每页最小内容（syntheses）

| 块 | 要求 |
| --- | --- |
| **frontmatter** | `CODING_WIKI.md` §3 最小集；`source_task` 指向 done 路径 |
| **摘要** | 背景 · 决策 · 验收要点（各 ≤5 行） |
| **pointer** | `→ docs/tasks/done/...` · 可选 `→ docs/harness/reviews/...` |
| **§测试变更** | 若 done task 涉 pytest/CI：**建议** 独立小节（T1c 纪律） |
| **graph_nodes** | 仅当 done task / T4 已定义：合法 `id` + `relation`；须 `graph_query neighbors <id>` exit 0 |
| **禁止** | 复制 invoke/review 全文 · 粘贴 SPEC 全文 · 绝对路径 |

---

## 4. 索引与 lint

| 文件 | 动作 |
| --- | --- |
| `docs/coding_wiki/index.md` | 10 行 syntheses 表 |
| `docs/coding_wiki/log.md` | `YYYY-MM-DD \| batch-ingest \| <slug> \| …` ×10 |
| `CODING_WIKI.md` | 可选：§7 试点 → 「扩面中」一句（非必须） |

**VERIFY（lint 批次）**：

```bash
for f in docs/coding_wiki/syntheses/*.md; do test -f "$f"; done
python -c "
import pathlib, re
root = pathlib.Path('docs/coding_wiki')
idx = (root/'index.md').read_text()
for slug in '''governance-l2-manifest-ci governance-wiki-t4-expand governance-l2-r3-test-manifest harness-wiki-loop-t4-l2 wiki-ctx-ab-v1 coding-wiki-pilot chatbi-v3-p2-health-ready harness-wiki-loop-c2-verify governance-wiki-t4-r1-pilot wiki-ctx-ab-multi-slug'''.split():
    assert slug in idx, slug
"
# 抽样 graph_nodes（若有）
python tools/tech_graph_manifest_check.py
```

---

## 5. 非范围

- 前端 `content/` Wiki mirror  
- 其余 done task 全量 ingest（>10）  
- `api/` · `tests/` · workflow  
- Harness prompts 正文  

---

## 6. 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | `source_task` 404 | lint **fail** · 修路径 |
| F2 | 复制 review 全文 | 50 **fail** · 改 pointer |
| F3 | `graph_nodes` id 非法 | `graph_query` fail → 修或删项 |
| F4 | 未更新 index | 50 **fail** |
| F5 | 擅自增删锁定名单 | 拒开工 · 须人改 SPEC/task |

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：10 slug 锁定表 · 扩面至 syntheses≥15 |

---

## 给 Cursor

`GOV-WIKI-INGEST-BATCH`、ingest、syntheses、index、log、批量、10 slug
