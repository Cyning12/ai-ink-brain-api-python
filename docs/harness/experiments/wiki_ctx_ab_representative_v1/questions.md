# Wiki-CTX-AB Representative — Gold 题集（6 slug）

| 项 | 值 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **phase** | P2 扩面 · **H-lean vs W** |
| **slug 名单** | 见 SPEC §2.1（6 个） |

> 每 slug 跑 **Q1–Q4** × **H-lean**、**W** 各一次。答案仅允许对应 `payloads/H-lean_<slug>.md` 或 `payloads/W_<slug>.md` 内信息。

---

## 通用题面（每 slug 替换 `<slug>` / done task 名）

### Q1 — 本 Epic 两项核心交付

> 本 Epic（`source_task` 指向的 done task）在 **范围** 内必须完成的两项交付是什么？各一句话并带路径。

**要点**：从 synthesis 或 H-lean 载荷中 **两项** 范围项；路径在 `docs/` 下。

### Q2 — test_strategy

> 该 Epic 的 `test_strategy` 取值？`test_strategy_note` 一句话原因。

**要点**：`not_applicable` / `recommended` / `required` 之一 + 与文档/代码变更相关理由。

### Q3 — freeze_id 与关账日

> `freeze_id`？关账日期（YYYY-MM-DD）？

**要点**：与 synthesis frontmatter 或 done 头部一致。

### Q4 — 域外陷阱（按 slug 变体）

| slug | 陷阱问法 |
| --- | --- |
| `harness-p1-docs-consolidation` | P1-1 工作区 reviews 是否在本 Epic **范围**？ |
| `tech-graph-gate-d-v2-tasks` | 是否允许 **手改 graph.json** 完成闸口？ |
| `chatbi-v3-p2-health-ready` | 本 Epic 是否要求改 **前端** UI？ |
| `governance-l2-manifest-ci` | 是否可用 **Wiki** 替代 `_test_manifest` CI？ |
| `wiki-ctx-ab-v1` | P2 实验是否证明可 **外推 ChatBI 实现**？ |
| `harness-wiki-loop-t4-l2` | 子 round 是否可 **跳过 invoke 落盘**？ |

**要点**：依据 synthesis / task 非范围 · 答 **否/不在** + 一句依据。

---

## scorecard 填表键

`scorecard.md` 列：`slug` · `arm` · `Qn` · `pass` · `payload_chars` · `notes`

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：6 slug × Q1–Q4 |
