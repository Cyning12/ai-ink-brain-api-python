# SPEC — 治理：Wiki 推广线 Phase P2 后续（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `GOV-WIKI-P2-FOLLOWUP@2026-05-27` |
| **Roadmap** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §5.2 · **P1-4 并行 / 后端 P2 Loop** |
| **Loop 母单** | [`task_harness_wiki_loop_p2_followup_v1.md`](../../tasks/active/task_harness_wiki_loop_p2_followup_v1.md) |
| **SKILL** | [`SKILL-harness-loop-batch.md`](../../tasks/skills/SKILL-harness-loop-batch.md) · **第五轮** · 推广 P2 后续 |

---

## 0. 完成态（一句话）

在后端仓以 **单 PR · 三 round Loop** 收口推广线 **P2 剩余 docs 项**：T4 bridge SPEC **draft→active**、L2 **Phase C 设计落盘**（非全量双向校验实现）、Ingest **第二批 5 slug**；与 **前端 P1-4**（工作区）**并行、解耦**。

---

## 1. 为何可在一个 Loop 内完成

| 判据 | 结论 |
| --- | --- |
| **先例** | 第四轮 T4+L2 Loop（R1→R3 + META）已验证 **docs-only 多 round 单 PR** |
| **本轮范围** | 三子 task 均 **`test_strategy: not_applicable`** · **禁止** 改 `api/`、`tests/`（除既有 manifest 只读引用）、`docs/harness/prompts/` 帽子正文、CI workflow |
| **Phase C 边界** | R2 仅 **SPEC § 扩展 + 验收口径 + 可选 task 模板**；**双向 failure_paths 工具实现** 另开 **非 Loop** task（涉 pytest 时 `required`） |
| **不适合 Loop 的项** | 任何 **改 api/tests/CI**、前端 parity、跨仓双 PR — **须拆出** |

**结论**：**可以**在一个 `harness-loop-batch` Loop 内完成本 SPEC 三 round；执行前 **`HG-LOOP-BATCH` 须人批 `approved`**。

---

## 2. 三 round 分工

| round | task_slug | freeze_id | 交付 |
| --- | --- | --- | --- |
| **R1** | `gov-t4-spec-active` | `GOV-T4-SPEC-ACTIVE@2026-05-27` | [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) **`draft→active`** · RECENT §6.6 T4 行 · Pilot/扩面 pointer  hygiene |
| **R2** | `gov-l2-phase-c-design` | `GOV-L2-PHASE-C-DESIGN@2026-05-27` | [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) 增 **Phase C** 设计节 · failure_paths ↔ manifest **口径** · **不** 新增校验脚本 |
| **R3** | `gov-wiki-ingest-batch-2` | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` | **5 slug** synthesis（累计 syntheses **≥20**）· `index.md` / `log.md` · lint |

**顺序（硬）**：**R1 → R2 → R3 → META**

---

## 3. R3 Ingest 候选 slug（草案 · R1 关账前可微调）

须来自 **done task**、且 **未** 出现在 Batch-1（见 [`SPEC-Governance-Wiki-Ingest-Batch-v1.md`](./SPEC-Governance-Wiki-Ingest-Batch-v1.md) §2）：

| # | 候选 slug | 来源 task（示意） |
| --- | --- | --- |
| 1 | `wiki-ctx-ab-representative` | `task_governance_wiki_ctx_ab_representative_v1` |
| 2 | `governance-wiki-agent-readorder` | `task_governance_wiki_agent_readorder_v1` |
| 3 | `governance-wiki-ingest-batch` | `task_governance_wiki_ingest_batch_v1` |
| 4 | `harness-wiki-loop-p2-followup` | 本 Loop META（关账后补页或 R3 前占位 synthesis 骨架） |
| 5 | `coding-wiki-concepts-harness` | T1c / 概念页 pointer（按 R3 task 锁定） |

**R3 启动前**：母单 [`task_harness_wiki_loop_p2_followup_v1.md`](../../tasks/active/task_harness_wiki_loop_p2_followup_v1.md) `human_gate` 中 `HG-INGEST-BATCH-2-SCOPE` 须 **approved** 并锁定上表（允许 ±1 替换，须写 invoke 理由）。

---

## 4. Loop 执行真值

| 项 | 路径 |
| --- | --- |
| **git_branch** | `task/wiki-loop-p2-followup-v1` |
| **MANIFEST** | [`docs/harness/invokes/by-task/wiki-loop-p2-followup/LOOP_MANIFEST.md`](../../harness/invokes/by-task/wiki-loop-p2-followup/LOOP_MANIFEST.md) |
| **全链启动** | [`PROMPT_START_loop_p2_followup_full_chain_v1.md`](../../harness/invokes/by-task/wiki-loop-p2-followup/PROMPT_START_loop_p2_followup_full_chain_v1.md) |
| **22→关账** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/wiki-loop-p2-followup/PROMPT_LOOP_22_to_CLOSE_v1.md) |

---

## 5. 非范围

- 前端 P1-4（→ 工作区 task）
- L2 Phase C **自动化实现**（pytest / 新 tools · 另 task）
- Wiki lint **CI 门禁**（可 P3 单独立项）

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：P2 三 round Loop 编排 + Phase C 设计边界 |

---

## 给 Cursor

`P2 followup`、`wiki-loop-p2-followup`、`GOV-WIKI-P2-FOLLOWUP`、`harness-loop-batch` 第五轮
