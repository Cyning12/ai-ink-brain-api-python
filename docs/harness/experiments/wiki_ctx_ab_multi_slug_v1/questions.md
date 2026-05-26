# Wiki-CTX-AB Multi · Gold 题集（v1 · 10 帽草案）

| 项 | 值 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB-MULTI@2026-05-26` |
| **对照** | H-lean vs W（同 P2 方法论） |
| **slug 数** | 2（人闸 `HG-AB-MULTI-SLUGS` 锁定） |

> **跑法**：每 slug、每题、每臂 **独立会话**；仅允许对应 `payloads/H-lean_<slug>.md` 或 `payloads/W_<slug>.md`。答案要点 pass/fail 填入 `scorecard.md` §Multi。  
> **22 帽**：可修订题干/要点，**不得** 改 slug 名单（除非人改闸）。

---

## Slug A · `tech-graph-gate-d-v2-tasks`

**done task**：`docs/tasks/done/task_engineering_tech_graph_gate_d_v2_tasks_v1.md`  
**Wiki**：`docs/coding_wiki/syntheses/tech-graph-gate-d-v2-tasks.md`

### A-Q1 — 扩域目标

**提问**

> 本 Epic（闸口 D v2）相对 v1 题集的主要扩域是什么？用一句话说明新增题代号。

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | 三题扩至 **五题**（或 v2 五题） |
| 2 | 新增含 **T004**（ChatBI/Text2SQL）与/或 **T005**（Intent/路由）表述 |

### A-Q2 — machine 默认

**提问**

> 关账后 **machine 默认** 消费图谱应使用什么？明确写出 **禁止** 升为默认的一项。

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | **`CTX_V2_QUERY` / `graph_query` 子图**（或等价） |
| 2 | **禁止** 将 **`CTX_DUAL_MD`**（或 Mermaid 双轨整包）升为 machine 默认 |

### A-Q3 — test_strategy 与关账 PR

**提问**

> 该 done task 的 `test_strategy` 取值？关账合并 PR 编号（若载荷有）？

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | `test_strategy` = **`required`** |
| 2 | PR **#41**（或 synthesis/task 中写的 #41） |

### A-Q4 — 实验轨结论文路径（陷阱）

**提问**

> jsonPKmermaid 闸口 D 结论文的 **完整绝对路径** 是什么？

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | **拒答/载荷未提供** — W 臂载荷 **不含** diary 全文；H-lean 若仅 pointer 相对路径则答 **相对路径** `docs/diary/jsonPKmermaid/reports/conclusion_gate_d_ctx_v2_tasks_v1_zh.md`，**禁止编造** `/Users/...` |
| 2 | 若答案出现载荷外路径细节 → **幻觉** |

---

## Slug B · `query-rewrite-observability`

**done task**：`docs/tasks/done/task_05_query_rewrite_observability.md`  
**Wiki**：`docs/coding_wiki/syntheses/query-rewrite-observability.md`

### B-Q1 — 可观测写入点

**提问**

> `query_compare`（raw vs rewrite）写入 Supabase 日志的字段路径是什么？

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | `rag_conversation_logs.metadata.match`（或 `metadata` 下 `match` 含 query_compare 语义） |

### B-Q2 — 新增单测

**提问**

> 本 Epic 新增的 pytest 文件路径是什么？（一句）

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | `tests/test_query_rewrite_compare_anchor.py` |

### B-Q3 — test_strategy

**提问**

> 该 task 的 `test_strategy` 与一句话理由？

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | **`required`**（或 task 头部实际值） |
| 2 | 理由含：改 **`api/`** 行为 / 需可失败自动化测试（表述不必逐字） |

> **footnote（post-A1 · 2026-05-26）**：synthesis 现蒸馏 `test_strategy: recommended`（非 gold 字面 `required`）；gold 允许「task 实际值」→ §Recheck B-Q3 **pass**。

### B-Q4 — 前端 UI（陷阱）

**提问**

> 双查询并行融合的前端 UI 是否在本 Epic **范围** 内？依据？

**标准答案要点**

| # | 要点 |
| --- | --- |
| 1 | **不在** 范围内 |
| 2 | 依据：task **非范围** 或 synthesis「前端 UI **另起 task**」 |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | 10 帽草案 · 2 slug × 4 题 |
