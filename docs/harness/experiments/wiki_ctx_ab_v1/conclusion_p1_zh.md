# Wiki-CTX-AB P1 — 结论文（accepted）

| 项 | 内容 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **phase** | P1 · H-full vs H-lean |
| **slug** | `harness-p1-docs-consolidation` |
| **date** | 2026-05-25 |
| **证据** | [`scorecard.md`](./scorecard.md) · [`payloads/H-full_*.md`](./payloads/) · [`payloads/H-lean_*.md`](./payloads/) |

---

## 1. 实验结论（签收）

| 测试项 | 结果 | 说明 |
| --- | --- | --- |
| T1 覆盖率 | **pass** | Q1–Q4 × 两臂，共 8 条回答已落盘 |
| T2–T5 正确性 | **pass** | 两臂均为 4/4；无幻觉 |
| T7 载荷效率 | **pass** | H-lean 15928→9896 字符，**降幅 37.9%**（≥30% 阈值） |
| T8 正确性不降 | **pass** | H-lean 4/4 = H-full 4/4 |

**P1 裁决**：**接受** — 在本 slug 上，**纪律消费（H-lean）** 在显著减少上下文的同时保持答题正确性。

---

## 2. 对路线图的影响（SPEC §3.1）

| 项 | 动作 |
| --- | --- |
| **T3 · 全仓 Harness taxonomy 推广** | **推荐执行**（工作区 `docs/harness/` + 前端 P1-4 可并行规划） |
| **T2 · P2（H-lean vs W）** | **不阻塞 T3**；待 `task_coding_wiki_pilot_v1` 同 slug ingest 后再跑 |
| **默认 Agent 读序** | P2 未结论前 **不** 写死「必须先 coding_wiki」 |

---

## 3. 局限与复现

- 单 slug、单 Epic（Harness P1 docs）；**不能** 外推 ChatBI 或图谱闸口。  
- H-lean 的 done task 为 **截断版**（不含 40/50 长回填）；见 payload `notes`。  
- 模型：`claude-opus-4-7`（见 scorecard）。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | P1 accepted；推荐 T3 |
