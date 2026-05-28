# Task：Wiki Loop 单元 A — 单 PR 编排母单（第六轮 · docs-only）

> **状态**：done（2026-05-28）  
> **关联 SPEC**：[`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](../spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md)  
> **关联 SKILL**：[`SKILL-harness-loop-batch.md`](../skills/SKILL-harness-loop-batch.md)（第六轮）  
> **执行备注**：**Claude Code（cc）** · 分支 **`task/wiki-unit-ab-plan-v1`** · 与单元 B **同分支、分两 PR**（本单 → **PR-A**）

> 落盘规则：R1→R3 子 task 均 `done/` 后 META 关账；`git mv` 本单 → `docs/tasks/done/`；更新 `_views/done.md` · RECENT §6.6。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；子 task 纯 docs；母单不直接改 `api/tests/tools`。 |
| **freeze_id** | `WIKI-LOOP-UNIT-A@2026-05-28` |
| **gates_before_code** | `["human_gate", "failure_paths", "R1→R2→R3", "R3 ingest 名单人批"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **task_slug** | `wiki-loop-unit-a` |
| **executor** | `claude-code`（关账后见 §SKILL 测评） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | approved | 22-R1, 30, 40, 50 | **人** 批后启动 R1；子 task 继承 |
| HG-INGEST-BATCH-3-SCOPE | approved | 22-R3, 30 | **R3 前** 锁定 Batch-3 五 slug · [`SPEC-Governance-Wiki-Ingest-Batch-3-v1.md`](../spec/governance/SPEC-Governance-Wiki-Ingest-Batch-3-v1.md) §1 |

> **子 task 继承**：R1/R2 仅继承 `HG-LOOP-BATCH`；R3 另受 `HG-INGEST-BATCH-3-SCOPE` 约束。**改 status 以本母单为准**。

---

## 子 task 顺序（硬 · R1→R2→R3→META）

| 序 | round | task 路径 | task_slug | freeze_id |
|----|-------|-----------|-----------|-----------|
| 1 | **R1** | [`task_governance_wiki_docs_hygiene_v1.md`](task_governance_wiki_docs_hygiene_v1.md) | `gov-wiki-docs-hygiene` | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| 2 | **R2** | [`task_governance_wiki_t4_rollout_v1.md`](task_governance_wiki_t4_rollout_v1.md) | `gov-wiki-t4-rollout` | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| 3 | **R3** | [`task_governance_wiki_ingest_batch_3_v1.md`](task_governance_wiki_ingest_batch_3_v1.md) | `gov-wiki-ingest-batch-3` | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| 4 | **META** | 本文件 | `wiki-loop-unit-a` | `WIKI-LOOP-UNIT-A@2026-05-28` |

**Manifest**：[`docs/harness/invokes/by-task/wiki-loop-unit-a/LOOP_MANIFEST.md`](../../harness/invokes/by-task/wiki-loop-unit-a/LOOP_MANIFEST.md)

---

## PR-A 边界（硬）

| 允许 | 禁止 |
|------|------|
| `docs/coding_wiki/`、`docs/spec/governance/`、`docs/tasks/`、`docs/harness/invokes/` | `api/`、`tools/`、`tests/`、`.github/workflows/` |
| `docs/tasks/RECENT_TASK_SCHEDULE.md`（R1 同步行） | `docs/harness/prompts/` 帽子正文 |

**PR-A 合并后**：`git pull origin main` 于 **`task/wiki-unit-ab-plan-v1`**，再开单元 B（**不换分支名**）。

---

## SKILL 测评（关账后 · 非本 Loop 阻塞）

| 项 | 值 |
| --- | --- |
| **实验轨** | [`docs/harness/experiments/skill_cross_platform_v1/`](../../harness/experiments/skill_cross_platform_v1/README.md) |
| **建议 case** | `wiki-loop-unit-a_claude-code_<YYYYMMDD>` |
| **量表** | [`rubric_v1.md`](../../harness/experiments/skill_cross_platform_v1/rubric_v1.md) · ST1–ST6 |
| **SKILL 载荷** | 显式 `@` `SKILL-harness-loop-batch.md` · `SKILL-docs-governance.md` |

---

## 验收标准

- [ ] `HG-LOOP-BATCH` = **approved** 后启动  
- [ ] `HG-INGEST-BATCH-3-SCOPE` = **approved** 后启动 **R3**  
- [ ] R1→R2→R3 各走 22→关账 · invoke C2 全绿  
- [ ] syntheses **≥25** · T4 铺量完成（见 R2 task）  
- [ ] **PR-A** 合 `main` · META `REPORT_completion_wiki_loop_unit_a_v1.md` 落盘  
- [x] `skill_cross_platform_v1` case 落盘 · [`wiki-loop-unit-a_claude-code_20260528`](../../harness/experiments/skill_cross_platform_v1/cases/wiki-loop-unit-a_claude-code_20260528/)  

---

## 给 Cursor / Claude Code

`wiki-loop-unit-a`、`WIKI-LOOP-UNIT-A`、`task/wiki-unit-ab-plan-v1`、PR-A、cc
