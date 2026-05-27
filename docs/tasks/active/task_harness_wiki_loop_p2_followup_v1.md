# Task：Wiki Loop P2 后续 — 单 PR 编排母单（第五轮 · 推广线）

> **状态**：draft  
> **META 关账日期**：（三轮子 task 均 `done/` 后）  
> **关联 SKILL**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../skills/SKILL-harness-loop-batch.md)（第五轮 · **T4 active + L2 Phase C 设计 + Ingest-2**）  
> **治理 SPEC**：[`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](../spec/governance/SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md)  
> **10 帽 Batch**：[`docs/harness/invokes/by-task/wiki-loop-p2-followup/PROMPT_BATCH_10_p2_followup_v1.md`](../harness/invokes/by-task/wiki-loop-p2-followup/PROMPT_BATCH_10_p2_followup_v1.md)

> 落盘规则：三轮子 task 均 `done/` 后本单 META 关账；`git mv` → `docs/tasks/done/` 并更新 `_views/done.md`。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；子 task 交付 docs/治理；母 task 不直接改业务正文。 |
| **freeze_id** | `WIKI-LOOP-P2-FOLLOWUP@2026-05-27` |
| **gates_before_code** | `["human_gate", "failure_paths", "子 task 顺序", "R3 ingest 名单人批"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-p2-followup-v1` |
| **task_slug** | `wiki-loop-p2-followup` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **approved** | 22-R1, 30, 40, 50 | **人** 批后启动 R1；子 task 继承后可启动全链 |
| HG-INGEST-BATCH-2-SCOPE | **approved** | 22-R3, 30 | **R3 启动前** 锁定 5 slug · 真值 [`task_governance_wiki_ingest_batch_2_v1.md`](task_governance_wiki_ingest_batch_2_v1.md) §3 · P2 SPEC §3 |

> **子 task 继承**：R1/R2 仅继承 `HG-LOOP-BATCH`；R3 另受 `HG-INGEST-BATCH-2-SCOPE` 约束。**改 status 以母单为准**，子单勿单独漂移。

---

## 子 task 顺序（硬 · R1→R2→R3→META）

| 序 | round | task 路径 | task_slug | freeze_id |
|----|-------|-----------|-----------|-----------|
| 1 | **R1** | [`task_governance_t4_spec_active_v1.md`](task_governance_t4_spec_active_v1.md) | `gov-t4-spec-active` | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
| 2 | **R2** | [`task_governance_l2_phase_c_design_v1.md`](task_governance_l2_phase_c_design_v1.md) | `gov-l2-phase-c-design` | `GOV-L2-PHASE-C-DESIGN@2026-05-27` |
| 3 | **R3** | [`task_governance_wiki_ingest_batch_2_v1.md`](task_governance_wiki_ingest_batch_2_v1.md) | `gov-wiki-ingest-batch-2` | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` |
| 4 | **META** | 本文件 | `wiki-loop-p2-followup` | `WIKI-LOOP-P2-FOLLOWUP@2026-05-27` |

**Manifest 真值**：[`docs/harness/invokes/by-task/wiki-loop-p2-followup/LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-p2-followup/LOOP_MANIFEST.md)

**排期职责**：**R1** 负责 RECENT §6.6 P2 Loop 行 **in_progress**；**META 关账** 负责 **done** + `_views/done.md` + `REPORT_completion_*`。

---

## 帽子顺序（母单 · **跳过 10** · Loop 关账）

| 序 | 帽 | 说明 |
|----|-----|------|
| — | **10** | **本 Loop 已 Batch 起草**；子 task **禁止** 再开 10 |
| 1–3 | **R1–R3 各轮** | 每轮 **22 → 30 → 40 → 50 → 关账** |
| 4 | **母关账** | 三轮子 task 均在 `done/` 后 META |

**执行纪律**：

- **单 PR**：合入 **`task/wiki-loop-p2-followup-v1`**，最终 **一个 PR** 合 `main`。  
- **顺序**：**R1 → R2 → R3 → META**  
- **禁止**：改 `api/`、`tests/`、`docs/harness/prompts/` 帽子正文、CI workflow。  
- **与 P1-4 关系**：**并行**；不阻塞工作区前端 task。

---

## 验收标准

- [ ] `HG-LOOP-BATCH` = **approved** 后启动  
- [ ] `HG-INGEST-BATCH-2-SCOPE` = **approved** 后启动 **R3**  
- [ ] R1→R2→R3 各走完整 22→关账链  
- [ ] 各 round invoke **C2 全绿**  
- [ ] 三轮子 task 均 `git mv` 至 `docs/tasks/done/`  
- [ ] META 后 `REPORT_completion_wiki_loop_p2_followup_v1.md` 落盘  

---

## 给 Cursor

`wiki-loop-p2-followup`、`WIKI-LOOP-P2-FOLLOWUP`、`harness-loop-batch` 第五轮
