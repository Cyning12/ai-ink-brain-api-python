# SPEC — 治理：Wiki 单元 A / B 拆解与双 PR 执行（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `GOV-WIKI-UNIT-AB@2026-05-28` |
| **执行分支（统一）** | `task/wiki-unit-ab-plan-v1` |
| **执行平台备注** | 本批 **Claude Code（cc）** 执行；关账后须跑 [`skill_cross_platform_v1`](../../harness/experiments/skill_cross_platform_v1/README.md) 通用 SKILL 测评 |
| **Roadmap** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) · P2 Loop **done** 后的运维扩面 |

---

## 0. 完成态（一句话）

在 **同一 git 分支** 上分 **两个 PR** 交付：**单元 A**（docs-only · Loop R1→R3）与 **单元 B**（L2 Phase C 实现 · `required`）；规划工件本 SPEC + `docs/tasks/active/` 母/子 task；**不** 在同一 PR 混 `api/tests` 与批量 Wiki ingest。

---

## 1. 为何拆成 A / B

| 单元 | 内容 | `test_strategy` | PR |
| --- | --- | --- | --- |
| **A** | 文档 hygiene + T4 `graph_nodes` 铺量 + Batch-3 ingest | `not_applicable` | **PR-A**（先合） |
| **B** | `_test_manifest` 双向校验脚本 + pytest | `required` | **PR-B**（A 合入 `main` 后继续同分支） |

依据：[`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](./SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md) §1（Phase C **实现** 另 task）；[`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) §4.4。

---

## 2. 单元 A — Loop 第六轮（docs-only）

| round | task_slug | task 文件 | freeze_id |
| --- | --- | --- | --- |
| **R1** | `gov-wiki-docs-hygiene` | [`task_governance_wiki_docs_hygiene_v1.md`](../../tasks/done/task_governance_wiki_docs_hygiene_v1.md) | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| **R2** | `gov-wiki-t4-rollout` | [`task_governance_wiki_t4_rollout_v1.md`](../../tasks/done/task_governance_wiki_t4_rollout_v1.md) | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| **R3** | `gov-wiki-ingest-batch-3` | [`task_governance_wiki_ingest_batch_3_v1.md`](../../tasks/done/task_governance_wiki_ingest_batch_3_v1.md) | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **META** | `wiki-loop-unit-a` | [`task_harness_wiki_loop_unit_a_v1.md`](../../tasks/done/task_harness_wiki_loop_unit_a_v1.md) | `WIKI-LOOP-UNIT-A@2026-05-28` |

**SPEC**：Batch-3 名单 [`SPEC-Governance-Wiki-Ingest-Batch-3-v1.md`](./SPEC-Governance-Wiki-Ingest-Batch-3-v1.md)  
**Harness**：[`docs/harness/invokes/by-task/wiki-loop-unit-a/`](../../harness/invokes/by-task/wiki-loop-unit-a/LOOP_MANIFEST.md)

**完成指标（A）**：

- syntheses **≥25**（当前 20 + Batch-3 **5**）
- 尚无 `graph_nodes` 的 synthesis **全部** 补种子 id（或显式 `graph_nodes: []` + 文内说明「纯叙事」）
- `WIKI_REQUIREMENTS_COMPARISON` / P2 SPEC 路径 / RECENT §6.6 与 done 状态一致

---

## 3. 单元 B — L2 Phase C 实现

| 项 | 值 |
| --- | --- |
| **task** | [`task_governance_l2_phase_c_impl_v1.md`](../../tasks/done/task_governance_l2_phase_c_impl_v1.md) |
| **freeze_id** | `GOV-L2-PHASE-C-IMPL@2026-05-28` |
| **范围** | `tools/tech_graph_test_manifest_check.py` 双向模式 · pytest · `99_spec` VERIFY 行 · **禁止** 改 Wiki 为 coverage 真值 |

**完成指标（B）**：§4.4.4 C1–C3；`pytest` 绿；50 复检落盘。

---

## 4. 双 PR · 同分支纪律（cc 执行）

```text
分支（全程）：task/wiki-unit-ab-plan-v1
Open Folder：ai-ink-brain-api-python/
```

| 步骤 | 动作 | 状态 |
| --- | --- | --- |
| 1 | 人批母单 A：`HG-LOOP-BATCH` · `HG-INGEST-BATCH-3-SCOPE` | **done** |
| 2 | cc 跑 **单元 A** → **PR-A** → `main` | **done** · [#79](https://github.com/Cyning12/ai-ink-brain-api-python/pull/79) |
| 3 | `git pull origin main`（同分支 `task/wiki-unit-ab-plan-v1`） | **done** |
| 4 | 人批单元 B：`HG-TASK-DRAFT` → `HG-AUDIT-R1`（22 后）→ `HG-REINSPECT`（50 后） | **done** |
| 5 | cc 跑 **单元 B** → **PR-B** → `main` | **done** · [#80](https://github.com/Cyning12/ai-ink-brain-api-python/pull/80) |
| 5b | Phase C CI：`check-failure-paths` Required | **done** · [#81](https://github.com/Cyning12/ai-ink-brain-api-python/pull/81) |
| 6 | **SKILL 测评** | A：[`wiki-loop-unit-a_claude-code_20260528`](../../harness/experiments/skill_cross_platform_v1/cases/wiki-loop-unit-a_claude-code_20260528/) · B：[`gov-l2-phase-c-impl_claude-code_20260528`](../../harness/experiments/skill_cross_platform_v1/cases/gov-l2-phase-c-impl_claude-code_20260528/) **done** |
| 7 | **叙事收口**（本 SPEC / Roadmap / RECENT / 对比表） | **done** · [`task_governance_wiki_unit_ab_closeout_v1.md`](../../tasks/done/task_governance_wiki_unit_ab_closeout_v1.md) |

**PR-A diff 白名单（硬）**：`docs/coding_wiki/`、`docs/spec/governance/`、`docs/tasks/`、`docs/harness/invokes/`、`docs/tasks/RECENT_TASK_SCHEDULE.md`（若 R1 改）  
**禁止 PR-A 含**：`api/`、`tests/`（除 invoke 引用）、`tools/`、`.github/workflows/`

**PR-B diff**：`tools/`、`tests/`、`docs/_tech_graph/_test_manifest.json`（若扩条目）、`docs/_tech_graph/99_spec.md`

---

## 5. 非范围

- 前端 `ai-ink-brain/` 改动  
- `coding_wiki_lint.py` CI Required（可 **P3** 另单）  
- 将单元 A/B **合并为单 PR**

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-28 | v1：A/B 拆解 · 同分支双 PR · cc + SKILL 测评备注 |
| 2026-05-28 | v1.1：PR-A #79 done · 单元 B 执行入口与 C2 抽样表 |
| 2026-05-28 | v1.2：PR-B #80 · Phase C CI #81 · SKILL B 臂 case · 收口 task **done** |

---

## 给 Cursor / Claude Code

`GOV-WIKI-UNIT-AB`、`wiki-loop-unit-a`、`gov-l2-phase-c-impl`、`task/wiki-unit-ab-plan-v1`、双 PR、cc、skill_cross_platform
