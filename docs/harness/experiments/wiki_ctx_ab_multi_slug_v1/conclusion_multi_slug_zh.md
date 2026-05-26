# Wiki-CTX-AB Multi slug — 结论文（accepted · 部分外推）

| 项 | 内容 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB-MULTI@2026-05-26` |
| **phase** | Multi · H-lean vs W × 2 slug |
| **slugs** | `tech-graph-gate-d-v2-tasks`、`query-rewrite-observability` |
| **date** | 2026-05-26 |
| **model** | `composer-2.5` |
| **证据** | [`scorecard.md`](./scorecard.md) §Multi · [`payloads/`](./payloads/) |
| **P2 基线（只读）** | [`wiki_ctx_ab_v1/conclusion_p2_zh.md`](../wiki_ctx_ab_v1/conclusion_p2_zh.md) |

---

## 1. 每 slug 裁决（SPEC 两问）

### Slug A · `tech-graph-gate-d-v2-tasks`（图谱 / 闸口 D）

| 问题 | 结论 |
| --- | --- |
| W 相对 H-lean 是否再省 token（≥30%）？ | **是**。21666 → 2978，降幅 **86.3%**。 |
| 正确性是否不降？ | **是**。W 4/4 = H-lean 4/4。 |

**slug A 签收**：**全满足** — 与 P2 单 slug 结论方向一致。

### Slug B · `query-rewrite-observability`（RAG 可观测）

| 问题 | 结论 |
| --- | --- |
| W 相对 H-lean 是否再省 token（≥30%）？ | **是**。8796 → 3395，降幅 **61.4%**。 |
| 正确性是否不降？ | **否（W 3/4）**。B-Q3：`test_strategy` 枚举未蒸馏进 synthesis；W 臂只能答「载荷未提供」。 |

**slug B 签收**：**T7 pass · T8 部分 fail** — 属 Wiki ingest 缺口，**不**否定 slug A 与 P2 单 slug 结论。

---

## 2. 汇总：默认 coding_wiki 读序可否外推？

| 项 | 结论 |
| --- | --- |
| **两 slug 均 T7+T8 全 pass？** | **否** — 1/2 slug W 臂 4/4 |
| **是否仍推荐默认读序？** | **是（附条件）** — 两域均显著省 token；图谱 slug 四题全中；RAG slug 缺口为 **元数据字段**（`test_strategy`），T1c 已示范 §测试变更 + decisions 补洞 |
| **与 P2 关系** | **不推翻** P2 accepted；本实验 **补充**「多域可复现降幅，但 ingest 须含 task 头关键枚举」 |

---

## 3. 局限（对照 P2 §4）

- 仅 **2** slug；未覆盖 ChatBI 实现类大 Epic。  
- W 臂 **禁止** 回读 L1 done task — `query-rewrite-observability` 的 `test_strategy: recommended` 未入 synthesis → B-Q3 失分 **可预期**。  
- H-lean 仍含 done task 全文，字符量随 Epic 规模波动（闸口 D 21k vs rewrite 8.8k）。  
- 复现：按 [`questions.md`](./questions.md) + `payloads/H-lean_*.md` / `W_*.md`，每题每臂独立会话。

---

## 4. 后续建议（非本 task 范围）

- ingest 规范：`api/` 类 Epic 的 synthesis **frontmatter 或摘要** 应含 `test_strategy`（或 pointer 至 `concepts/test-strategy-ink-backend` **正文**内联）。  
- 可选另开 task 增第三 slug 或补跑 B-Q3 修复后复检。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | Multi accepted · 部分外推 · 推荐默认读序附 ingest 条件 |
