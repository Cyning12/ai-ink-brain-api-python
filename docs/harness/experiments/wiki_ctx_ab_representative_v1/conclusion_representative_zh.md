# Wiki-CTX-AB Representative — 结论文（accepted · 部分外推）

| 项 | 内容 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **phase** | P2 扩面 · H-lean vs W × **6 slug** |
| **date** | 2026-05-27 |
| **model** | `composer` |
| **证据** | [`scorecard.md`](./scorecard.md) · [`payloads/`](./payloads/) |
| **基线** | P2 [`conclusion_p2_zh.md`](../wiki_ctx_ab_v1/conclusion_p2_zh.md) · Multi [`conclusion_multi_slug_zh.md`](../wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md) |

---

## 1. 聚合签收（SPEC §3）

| 测试项 | 结果 | 说明 |
| --- | --- | --- |
| T7 载荷效率 | **pass** | **6/6** slug W 相对 H-lean 降幅 **60.8%–77.3%**（均 ≥30%） |
| T8 正确性 | **pass** | **6/6** slug ≥3/4；**5/6** slug W 臂 **4/4** |
| T6 无幻觉 | **pass** | 无载荷外路径 / freeze_id 编造 |
| **T-AGG** | **accepted（部分外推）** | T7+T8 同时满足 |

**不推翻** P2 单 slug 与 Multi 2 slug 结论；本实验 **强化**「多域代表性 slug 上 Wiki 默认读序可显著省上下文且多数四题全中」。

---

## 2. 每域摘要

| slug | 域 | T7 | W 正确性 | 备注 |
| --- | --- | --- | --- | --- |
| harness-p1-docs-consolidation | Harness P1 | 64.7% | 4/4 | 与 P2 gold slug 同域复现 |
| tech-graph-gate-d-v2-tasks | 图谱闸口 D | 77.3% | 4/4 | 与 Multi slug A 一致 |
| chatbi-v3-p2-health-ready | ChatBI P2 探针 | 61.2% | 4/4 | ingest 含 `test_strategy` |
| governance-l2-manifest-ci | L2 manifest CI | 60.8% | 4/4 | Wiki vs manifest 分工题全中 |
| wiki-ctx-ab-v1 | Wiki 元实验 | 73.6% | 4/4 | Q4 陷阱（外推 ChatBI）命中 |
| harness-wiki-loop-t4-l2 | Loop T4+L2 | 65.4% | **3/4** | W-Q2：母单 `test_strategy` 未入 synthesis |

---

## 3. 局限（部分外推声明）

**可外推**

- 关账回顾、docs/治理类、**已 ingest** Epic 的跨会话理解。  
- 六域中 **五域** W 臂四题全中；载荷降幅稳定 **>60%**（除最大 H-lean 闸口 D 体外仍 >77% W 侧）。

**不可外推**

- 未 ingest 的运行时细节、生产配置、**前端 Next/BFF**（须 **P1-4** 独立 task）。  
- ChatBI **实现级**排障（本批仅 P2-1a 探针 Epic）。  
- Loop 母单类 Epic：ingest 须含 **`test_strategy` 枚举**（见 `harness-wiki-loop-t4-l2` W-Q2）。

---

## 4. 前端 P1-4 Harness parity 建议（证据链 · 非自动执行）

| 项 | 建议 |
| --- | --- |
| **立项条件** | 本结论文 **accepted** + [`scorecard.md`](./scorecard.md) 聚合表 → 工作区 / `ai-ink-brain` **P1-4** 独立 task + 人批 |
| **范围建议** | 前端 `content/harness/` 或 `docs/harness/` 模板 + rules：**默认读序** 对齐 `docs/coding_wiki/index` + synthesis（**禁止** W 臂回读全量 L1 done） |
| **定量附件** | PR 描述引用：6 slug 降幅 **60.8%–77.3%**；5/6 slug W **4/4** |
| **与后端关系** | 后端 Agent 读序已 **done**（`gov-wiki-agent-readorder`）；前端 parity **不**重复 ingest，须自有 gold slug 集 |

---

## 5. 复现

```bash
# 物化（代表实验目录）
for s in harness-p1-docs-consolidation tech-graph-gate-d-v2-tasks \
  chatbi-v3-p2-health-ready governance-l2-manifest-ci wiki-ctx-ab-v1 \
  harness-wiki-loop-t4-l2; do
  python tools/wiki_ctx_ab_materialize_w.py --slug "$s" \
    --out-dir docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads \
    --freeze-id WIKI-CTX-AB-REP@2026-05-27
  python tools/wiki_ctx_ab_materialize_h_lean.py --slug "$s" \
    --out-dir docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads \
    --freeze-id WIKI-CTX-AB-REP@2026-05-27
done
```

按 [`questions.md`](./questions.md) 每题每臂独立会话；W 臂 **禁止** `docs/harness/invokes/`、`docs/tasks/done/` 全文。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：6 slug 代表性扩面 accepted（部分外推） |
