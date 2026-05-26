# Wiki-CTX-AB Multi · Scorecard

| 项 | 值 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB-MULTI@2026-05-26` |
| **phase** | Multi（H-lean vs W × 2 slug） |
| **model** | `composer-2.5` |
| **date** | 2026-05-26 |

## §Multi（30 帽填写）

### Slug · `tech-graph-gate-d-v2-tasks`

| 题 | 臂 | payload_char_count | pass/fail | 备注 |
|----|-----|-------------------|-----------|------|
| A-Q1 | H-lean | 21666 | **pass** | v2 五题；+T004 ChatBI/Text2SQL、+T005 Intent/路由 |
| A-Q1 | W | 2978 | **pass** | synthesis 摘要：三题扩五题 + T004/T005 |
| A-Q2 | H-lean | — | **pass** | `CTX_V2_QUERY` / `graph_query`；禁止升 `CTX_DUAL_MD` |
| A-Q2 | W | — | **pass** | synthesis 架构决议一致 |
| A-Q3 | H-lean | — | **pass** | `test_strategy: required`；PR #41 |
| A-Q3 | W | — | **pass** | synthesis 摘要含 required + PR #41 |
| A-Q4 | H-lean | — | **pass** | 相对路径 `docs/diary/jsonPKmermaid/reports/conclusion_gate_d_ctx_v2_tasks_v1_zh.md`；未编造绝对路径 |
| A-Q4 | W | — | **pass** | synthesis pointer 相对路径；拒答绝对路径 |

### Slug · `query-rewrite-observability`

| 题 | 臂 | payload_char_count | pass/fail | 备注 |
|----|-----|-------------------|-----------|------|
| B-Q1 | H-lean | 8796 | **pass** | `rag_conversation_logs.metadata.match`（含 query_compare） |
| B-Q1 | W | 3395 | **pass** | synthesis 摘要同字段路径 |
| B-Q2 | H-lean | — | **pass** | `tests/test_query_rewrite_compare_anchor.py` |
| B-Q2 | W | — | **pass** | synthesis §测试变更 |
| B-Q3 | H-lean | — | **pass** | `recommended`；改 `api/` 行为 + 需 pytest |
| B-Q3 | W | — | **fail** | 载荷无 `test_strategy` 枚举；测试变更节有 api/pytest 理由但缺要点 #1 |
| B-Q4 | H-lean | — | **pass** | 不在范围；task 非范围「不新增前端 UI」 |
| B-Q4 | W | — | **pass** | 不在范围；synthesis「前端 UI 另起 task」 |

### 汇总（30 帽）

| slug | H-lean 字符 | W 字符 | 降幅 % | 正确性 H-lean | 正确性 W |
|------|-------------|--------|--------|---------------|----------|
| tech-graph-gate-d-v2-tasks | 21666 | 2978 | **86.3%** | 4/4 | 4/4 |
| query-rewrite-observability | 8796 | 3395 | **61.4%** | 4/4 | 3/4 |

**结论草稿**：slug A 全满足 T7+T8；slug B T7 满足、W 臂 T8 为 3/4（B-Q3 Wiki 缺 test_strategy 蒸馏）→ 见 `conclusion_multi_slug_zh.md` **部分外推**。

---

## 逐题回答摘要（30 · 载荷隔离）

### A-Q1 · H-lean

> 本 Epic 相对 v1 题集的主要扩域？新增题代号？

v1 三题扩至 **v2 五题**；新增 **T004**（ChatBI/Text2SQL）与 **T005**（Intent/路由）。

### A-Q4 · W（陷阱）

> jsonPKmermaid 闸口 D 结论文的 **完整绝对路径**？

**拒答绝对路径**。载荷仅提供相对路径：`docs/diary/jsonPKmermaid/reports/conclusion_gate_d_ctx_v2_tasks_v1_zh.md`（实验轨 pointer，非本臂必读全文）。

### B-Q3 · W

> 该 task 的 `test_strategy` 与一句话理由？

`test_strategy`：**载荷未提供**（synthesis frontmatter 无该字段）。理由（部分）：§测试变更表明改 `api/` 并新增 `tests/test_query_rewrite_compare_anchor.py` — **未命中 gold 要点 #1**。

---

## §Recheck（Wiki Loop B-Q3 · 2026-05-26）

| 项 | 值 |
| --- | --- |
| **freeze_id** | `WIKI-BQ3-R1-PAYLOAD@2026-05-26` |
| **round** | Loop R1 |
| **W payload** | `payloads/W_query-rewrite-observability.md` |
| **payload_char_count（新）** | **3625**（原 Multi 3395 · +230） |
| **物化依据** | A1 ingest 后 synthesis 含 `test_strategy: recommended` |

### Slug B · W 臂快检（载荷隔离 · 2026-05-26）

| 题 | pass/fail | 要点摘要 |
|----|-----------|----------|
| B-Q1 | **pass** | `rag_conversation_logs.metadata.match`（raw vs rewrite 对比） |
| B-Q2 | **pass** | `tests/test_query_rewrite_compare_anchor.py` |
| B-Q3 | **pass** | `test_strategy: **recommended**`（frontmatter + §测试变更）；理由：改 `api/` 观测行为、须可失败单测 |
| B-Q4 | **pass** | 前端 UI **不在** Epic 范围；synthesis「另起 task」 |

### 汇总

| 项 | 原 §Multi | §Recheck |
|----|-----------|----------|
| slug B W 正确性 | 3/4（B-Q3 fail） | **4/4** |
| B-Q3 | fail | **pass** |

> **注**：§Multi 主表行 **冻结**不改；本 addendum 为 Wiki Loop R1 复检证据。
