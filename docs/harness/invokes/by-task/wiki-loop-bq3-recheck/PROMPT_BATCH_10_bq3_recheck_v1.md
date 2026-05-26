# 启动 Prompt · 一次性 Batch-10 · Wiki Loop B-Q3 Recheck（v1）

> **只运行一次**。生成母 task + 三个子 task 初稿后，后续每轮 **仅** 使用 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md)（见 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md)）。  
> **分支**：`task/wiki-loop-bq3-recheck-v1` · Open **`ai-ink-brain-api-python/`**

---

```text
你正在扮演 Harness「需求与任务分析帽（10）· Batch 模式」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（输出形状；本批 **禁止** 写业务代码）
- docs/tasks/templates/TASK_TEMPLATE.md
- docs/tasks/skills/SKILL-docs-governance.md（预填片段）
- docs/tasks/skills/SKILL-harness-loop-batch.md（Loop 字段）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、07-git-workflow.mdc

【背景】
Loop A1–A4 **done**：synthesis `query-rewrite-observability` 已补 `test_strategy: recommended`。
Multi slug 原 scorecard 仍记录 slug B W 臂 B-Q3 **fail**（载荷生成于 A1 前）。
SPEC §5.1 / 对比表 #46 仍为「部分外推」；conclusion §4 建议「补跑 B-Q3 修复后复检」。
本 Loop = **第二次 harness-loop-batch 试点**（验证 SKILL draft）；**单 PR**、docs-only。
扫描合并：R1 实验载荷+跑分 · R2 结论文+对比表 · R3 SPEC+RECENT 治理收口。

【开帽 · Invoke 快照】将 **本 user 消息全文** 落盘至：
docs/harness/invokes/by-task/wiki-loop-bq3-recheck/invoke_20260526_10_batch_bq3_recheck_v1.md

【SDD】不涉及新 SPEC · 状态 = 不涉及新 SPEC（§3 省略）

【你必须落盘以下 4 个 task 文件（相对子仓根）】

---

## 0. 母 task · task_harness_wiki_loop_bq3_recheck_v1.md

路径：docs/tasks/active/task_harness_wiki_loop_bq3_recheck_v1.md

| 字段 | 值 |
|------|-----|
| test_strategy | not_applicable |
| test_strategy_note | Loop 编排；子 task 交付 docs/实验工件；母 task 不直接改 api |
| freeze_id | WIKI-LOOP-BQ3-RECHECK@2026-05-26 |
| semi_auto | true |
| audit_profile | post_close |
| git_branch | task/wiki-loop-bq3-recheck-v1 |
| task_slug | wiki-loop-bq3-recheck |

人工闸（仅母 task）：
| HG-LOOP-BATCH | pending | 22-R1,30,40,50 | 人批后子 task 写「继承母闸」 |

正文须含：
- 子 task 顺序 R1→R2→R3→META
- 链 LOOP_MANIFEST / PROMPT_LOOP
- 单 PR、不改 api/tests/prompts/CI
- **R3 负责** RECENT §6.6 + SPEC §5.1（合并治理；**#46 / conclusion** 属 R2）
- META 关账时注明：SKILL `harness-loop-batch` 第二 Loop 完成 → **人** 可审 draft→accepted
- §验收：三轮均 done/ 后母关账

---

## 1. 子 task R1 · task_wiki_ctx_ab_multi_bq3_recheck_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | WIKI-BQ3-R1-PAYLOAD@2026-05-26 |
| task_slug | wiki-bq3-r1-payload-scorecard |
| human_gate | 继承 HG-LOOP-BATCH |

**目标**：
1. 按当前 `docs/coding_wiki/` **重新物化** W 臂载荷 `docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/payloads/W_query-rewrite-observability.md`（须含 synthesis frontmatter `test_strategy`；更新 `generated` 元信息）。
2. 在 **独立只读** 语境下答 Multi **B-Q3**（及建议 slug B W 臂 **四题** 快检），依据新 W 载荷。
3. 在 `scorecard.md` 末尾增 **§Recheck（Wiki Loop B-Q3 · 2026-05-26）** addendum（**不**改 §Multi 主表冻结行）。

**范围**：
- 改 W payload 文件；scorecard addendum；可选 `payloads/W_query-rewrite-observability.md` 旁 README 一行
- VERIFY：`rg test_strategy docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/payloads/W_query-rewrite-observability.md`
- 关账回填 R2 `PLACEHOLDER:R1_OUTCOME`（含 B-Q3 pass/fail、W 4/4 与否、commit 短哈希）

**非范围**：不改 H-lean 载荷；不推翻 `conclusion_multi_slug_zh.md` 冻结正文（属 R2）；不改 api/tests

**帽子顺序**：22→30→40→50→关账 · PROMPT_LOOP round=R1

---

## 2. 子 task R2 · task_wiki_ctx_ab_multi_conclusion_bq3_sync_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | WIKI-BQ3-R2-CONCLUSION@2026-05-26 |
| task_slug | wiki-bq3-r2-conclusion |
| human_gate | 继承 HG-LOOP-BATCH |

**目标**（依赖 R1 addendum）：
- 若 R1 B-Q3 **pass**：在 `conclusion_multi_slug_zh.md` 增 **§5 Recheck**（或修订 §1 slug B 脚注），说明 slug B W 臂可 4/4；**保留**原 §Multi 历史结论。
- 更新 `docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` **#46** 与 **§7** 行（部分→全满足或附条件全满足，与 R1 证据一致）。
- 可选：`questions.md` B-Q3 gold 要点与 synthesis 对齐说明（一行 footnote，非改题面）。

**占位**：`<!-- PLACEHOLDER:R1_OUTCOME -->` · 22 前须已回填

**非范围**：RECENT/SPEC 正文（属 R3）；改 scorecard 主表

---

## 3. 子 task R3 · task_governance_wiki_bq3_spec_schedule_sync_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | GOV-WIKI-BQ3-SYNC@2026-05-26 |
| task_slug | wiki-bq3-r3-gov-sync |
| human_gate | 继承 HG-LOOP-BATCH |

**目标**（合并治理 · 原 Loop A3+A4 合并为一 round）：
- `SPEC-Governance-Wiki-Harness-Roadmap-v1.md` §5.1 增行或脚注：**B-Q3 Recheck done** · 链本 Loop 母 task
- `RECENT_TASK_SCHEDULE.md` §6.6 增 **Wiki Loop B-Q3 Recheck** 行（in_progress→done 由关账更新）
- 可选：`docs/tasks/skills/SKILL-harness-loop-batch.md` 修订记录一行「第二 Loop 试点关账」——**不**代改 status draft→accepted

**非范围**：不改 Harness prompts；不改 api/tests

---

【commit】
- 4 task + invoke batch + 本目录 README/MANIFEST/BATCH/START/LOOP（若 Batch 一并创建）
- message：`docs(task): Wiki Loop B-Q3 Recheck Batch-10 · WIKI-LOOP-BQ3-RECHECK@2026-05-26`

【停】
- **勿** 执行 22
- 下一棒：人批 `HG-LOOP-BATCH` → [`PROMPT_START_loop_bq3_full_chain_v1.md`](./PROMPT_START_loop_bq3_full_chain_v1.md) §3
```
