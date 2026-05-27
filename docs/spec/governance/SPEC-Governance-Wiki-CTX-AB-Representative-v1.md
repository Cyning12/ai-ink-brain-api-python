# SPEC — 治理：Wiki-CTX-AB 代表性扩面（P2 多 slug · v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **Roadmap** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) · 推广至前端 P1-4 的 **证据轨** |
| **前置实验** | P2 单 slug [`conclusion_p2_zh.md`](../harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md) · Multi 2 slug [`task_wiki_ctx_ab_multi_slug_v1.md`](../tasks/done/task_wiki_ctx_ab_multi_slug_v1.md) |
| **前置推广** | Agent 读序 **done** · Ingest **15 syntheses** **done** |
| **对比表** | [`docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md) §6 #46 |
| **执行 task** | [`task_governance_wiki_ctx_ab_representative_v1.md`](../tasks/active/task_governance_wiki_ctx_ab_representative_v1.md) |

---

## 0. 完成态（一句话）

在 **6 个代表性 slug** 上复跑 **对照实验二（H-lean vs W）**，产出可审计 `scorecard` + `conclusion_representative_zh.md`；若 **聚合签收** 通过，则形成 **前端 Harness parity / Coding Wiki 大包** 的定量依据（**不**在本 SPEC 内执行前端）。

---

## 1. 背景与目标

| 痛点 | 本 SPEC 应对 |
| --- | --- |
| P2 仅 1 slug、Multi 仅 2 slug | **6 slug** 跨 Harness / 图谱 / ChatBI / 治理 / Loop |
| 无法向工作区/前端推广 | 结论文 **显式** 链 P1-4 立项条件 |
| ingest 后 W 载荷已齐 | 直接用 `docs/coding_wiki/syntheses/<slug>.md` |

**非目标**：跑 P1（H-full vs H-lean）；改 `api/`；在前端仓落盘。

---

## 2. 对照设计（锁定）

| 项 | 约定 |
| --- | --- |
| **阶段** | **P2 扩面** · 臂 **B** = H-lean · 臂 **C** = W（仅 Wiki） |
| **题集** | 每 slug **Q1–Q4**（见 [`questions.md`](../harness/experiments/wiki_ctx_ab_representative_v1/questions.md)） |
| **物化** | `docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads/` · 参照 v1 [`payloads/TEMPLATE-*.md`](../harness/experiments/wiki_ctx_ab_v1/payloads/) |
| **纪律** | W 臂 **禁止** 回读 `docs/harness/invokes/`、`docs/tasks/done/` 全文；H-lean 按 by-task 纪律 |

### 2.1 锁定 slug（6 · 不可增删）

| # | slug | 域 | synthesis 须存在 |
| --- | --- | --- | --- |
| 1 | `harness-p1-docs-consolidation` | Harness P1 | ✅ |
| 2 | `tech-graph-gate-d-v2-tasks` | 图谱闸口 D | ✅ |
| 3 | `chatbi-v3-p2-health-ready` | ChatBI P2-1a | ✅ |
| 4 | `governance-l2-manifest-ci` | L2 manifest | ✅ |
| 5 | `wiki-ctx-ab-v1` | Wiki-CTX 元实验 | ✅ |
| 6 | `harness-wiki-loop-t4-l2` | Loop T4+L2 | ✅ |

---

## 3. 签收阈值（聚合 · 硬性）

| ID | 指标 | 通过线 |
| --- | --- | --- |
| **T7** | W 相对 H-lean 字符降幅 | **每 slug ≥30%**，且 **≥5/6** slug 达标 |
| **T8** | 正确性 | **每 slug ≥3/4** gold 要点；**≥5/6** slug 达标 |
| **T6** | 无幻觉 | 6 slug 均无载荷外路径/freeze_id 编造 |
| **T-AGG** | 聚合裁决 | T7+T8 同时满足 → **accepted（部分外推）**；否则 **rejected** 或 **附条件** |

**部分外推声明（结论文必写）**：

- **可外推**：关账回顾类、docs/治理类、已 ingest Epic 的跨会话理解。  
- **不可外推**：未 ingest 的 ChatBI 实现细节、生产运行时、前端 Next/BFF（须 P1-4 另验）。

---

## 4. 交付物

| 路径 | 内容 |
| --- | --- |
| `docs/harness/experiments/wiki_ctx_ab_representative_v1/questions.md` | Gold 题 + 要点 |
| `…/payloads/H-lean_<slug>.md` ×6 | 物化载荷 |
| `…/payloads/W_<slug>.md` ×6 | 物化载荷 |
| `…/scorecard.md` | 6×4×2 填表 + 统计 |
| `…/conclusion_representative_zh.md` | 签收 / 局限 / **前端 P1-4 建议** |
| `docs/tasks/reinspect_results/reinspect_wiki-ctx-ab-representative_*` | 50 复检 |

---

## 5. 与前端大包的关系（证据链）

```text
本 SPEC 签收 accepted
  → 建议立项：工作区/ai-ink-brain P1-4 Harness parity（模板 + rules + 可选 content/harness）
  → 结论文附录：引用 scorecard 聚合降幅、正确性表
  → 非自动执行前端（须独立 task + 人批）
```

---

## 6. VERIFY

```bash
test -f docs/harness/experiments/wiki_ctx_ab_representative_v1/scorecard.md
test -f docs/harness/experiments/wiki_ctx_ab_representative_v1/conclusion_representative_zh.md
ls docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads/H-lean_*.md | wc -l   # 6
ls docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads/W_*.md | wc -l        # 6
```

---

## 7. 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | 擅自改 6 slug | 停 · 人改 SPEC |
| F2 | W 臂偷读 done 全文 | 该 slug **invalid** · 重跑 |
| F3 | <5/6 达标仍写 accepted | 50 **fail** |
| F4 | 无 scorecard 物化字符数 | 40 **fail** |

---

## 8. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：6 slug 代表性 P2 扩面 · 前端 P1-4 证据轨 |

---

## 给 Cursor

`WIKI-CTX-AB-REP`、代表性扩面、H-lean、W、scorecard、前端 parity 证据
