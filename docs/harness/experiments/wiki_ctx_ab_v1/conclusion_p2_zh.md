# Wiki-CTX-AB P2 — 结论文（accepted）

| 项 | 内容 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **phase** | P2 · H-lean vs W |
| **slug** | `harness-p1-docs-consolidation` |
| **date** | 2026-05-26 |
| **model** | `composer-2.5`（temperature `0`） |
| **证据** | [`scorecard.md`](./scorecard.md) §P2 · [`payloads/H-lean_*.md`](./payloads/) · [`payloads/W_*.md`](./payloads/) |

---

## 1. 实验结论（签收）

| 测试项 | 结果 | 说明 |
| --- | --- | --- |
| T1 覆盖率 | **pass** | Q1–Q4 × H-lean × W，共 8 条已落盘 scorecard §P2 |
| T2–T5 正确性 | **pass** | 两臂均为 **4/4**；无载荷外幻觉 |
| T6 无幻觉 | **pass** | 8 条均未编造载荷外路径或 freeze_id |
| T7 载荷效率 | **pass** | W 2096 vs H-lean 9896 字符，**降幅 78.8%**（≥30% 阈值） |
| T8 正确性不降 | **pass** | W 4/4 = H-lean 4/4 |

**P2 裁决**：**接受** — 在本 slug 上，**仅 Wiki（W）** 在相对 H-lean 再显著缩小上下文的同时，四题 gold 要点全部命中。

---

## 2. SPEC §3.1 两问（硬性）

| 问题 | 结论 |
| --- | --- |
| W 相对 H-lean 是否再省 token（≥30%）？ | **是**。9896 → 2096，降幅 **78.8%**。 |
| 正确性是否不降？ | **是**。W 与 H-lean 均为 4/4 pass。 |

---

## 3. 默认 Agent 读序（路线图）

| 项 | 动作 |
| --- | --- |
| **推荐默认先读** | **是** — 关账类 / 已 ingest 的 done task：Agent **默认先读** `docs/coding_wiki/index.md`，再按 slug 打开对应 `docs/coding_wiki/syntheses/<slug>.md` |
| **与 P1 关系** | P1 已推荐 T3 Harness taxonomy；P2 **不阻塞** T3，并 **补充** Wiki 默认读序 |
| **纪律** | W 臂仍 **禁止** 为答题回读 `docs/harness/`、`docs/tasks/done/` 全文；日常实现真值仍以 L0 图谱 + L1 task 为准（见 synthesis `llm-wiki-layers` 指针） |

---

## 4. 局限与复现

- 单 slug、单 Epic（Harness P1 docs）；**不能** 外推 ChatBI 或图谱闸口。  
- W 载荷 **不含** `RECENT_TASK_SCHEDULE` 全文；Q4 依赖 synthesis 中「P1-1 另 task / 工作区 pointer」表述，与 H-lean 依据 task 非范围 **等价**。  
- 复现：按 [`PROMPT_third_party_agent_wiki_ctx_ab_p2.md`](./PROMPT_third_party_agent_wiki_ctx_ab_p2.md) §0–§3，每臂每题独立会话。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | P2 accepted；推荐 coding_wiki 默认读序 |
