# Task：Wiki-CTX-AB v1（Harness 上下文消费对照 · P1→P2）

> **状态**：`active`（P1 **done** · P2 **40 done** · 待 **50** 复检）  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)  
> **实验目录**：[`docs/harness/experiments/wiki_ctx_ab_v1/`](../harness/experiments/wiki_ctx_ab_v1/README.md)  
> **T1b（done）**：[`../done/task_coding_wiki_pilot_v1.md`](../done/task_coding_wiki_pilot_v1.md) · 同 slug `harness-p1-docs-consolidation`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 实验填表 + 结论文；无代码/CI 变更。 |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **gates_before_code** | `["human_gate"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-ctx-ab-p2-v1` |
| **task_slug** | `wiki-ctx-ab` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-AB-SLUG | approved | — | gold slug = `harness-p1-docs-consolidation` |
| HG-AB-P1-DONE | approved | P2 执行 | P1 已验收 — [`conclusion_p1_zh.md`](../harness/experiments/wiki_ctx_ab_v1/conclusion_p1_zh.md) |

---

## 帽子顺序（P2 · 计划：**22 → 30 → 40 → 50 → 关账**）

| 序 | 帽 | 启动 Prompt（子仓） |
|----|-----|----------------------|
| 1 | **22 R1** | [`docs/harness/invokes/by-task/wiki-ctx-ab/PROMPT_22_startup_wiki-ctx-ab-p2-v1.md`](../harness/invokes/by-task/wiki-ctx-ab/PROMPT_22_startup_wiki-ctx-ab-p2-v1.md) |
| 2 | **30** | [`…/PROMPT_30_startup_wiki-ctx-ab-p2-v1.md`](../harness/invokes/by-task/wiki-ctx-ab/PROMPT_30_startup_wiki-ctx-ab-p2-v1.md) |
| 3 | **40** | [`…/PROMPT_40_startup_wiki-ctx-ab-p2-v1.md`](../harness/invokes/by-task/wiki-ctx-ab/PROMPT_40_startup_wiki-ctx-ab-p2-v1.md) |
| 4 | **50** | [`…/PROMPT_50_startup_wiki-ctx-ab-p2-v1.md`](../harness/invokes/by-task/wiki-ctx-ab/PROMPT_50_startup_wiki-ctx-ab-p2-v1.md) |
| 5 | **关账** | [`…/PROMPT_CLOSE_wiki-ctx-ab-p2-v1.md`](../harness/invokes/by-task/wiki-ctx-ab/PROMPT_CLOSE_wiki-ctx-ab-p2-v1.md) |

| 帽 | 说明 |
|----|------|
| **10** | **跳过**（task 已存在） |
| **22** | P2 **开工就绪审**（T1b Wiki 同 slug · W 载荷） |
| **30** | 跑 H-lean vs W · 填 scorecard §P2 · `conclusion_p2_zh.md` |
| **40** | VERIFY 实验产物 |
| **50** | 独立复检 → `reinspect_results/` |
| **关账** | 整 task `done/` + CLOSE_TRACE |

**纪律**：每帽 **新对话** + Open **`ai-ink-brain-api-python/`**；见 [`docs/harness/ACCEPTANCE_LANDING.md`](../harness/ACCEPTANCE_LANDING.md)。

**三方跑题**（30 内引用）：[`PROMPT_third_party_agent_wiki_ctx_ab_p2.md`](../harness/experiments/wiki_ctx_ab_v1/PROMPT_third_party_agent_wiki_ctx_ab_p2.md)

---

## 背景与目标

用可复现 **H-full / H-lean / W** 对照，为 **Harness 全仓推广** 与 **Coding Wiki 默认读序** 提供证据（见 SPEC §3）。

**P1 完成态**：物化 H-full/H-lean + `scorecard` §P1 + `conclusion_p1_zh.md`（**accepted**）。  
**P2 完成态**（T1b **done**）：`TEMPLATE-W` + `W_*` 物化 + `scorecard` §P2 + `conclusion_p2_zh.md`。

---

## 范围

- [x] 按 [`questions.md`](../harness/experiments/wiki_ctx_ab_v1/questions.md) 跑 P1（4 题 × 2 臂）。
- [x] `payloads/H-full_harness-p1-docs-consolidation.md`、`H-lean_*.md` 已物化。
- [x] [`scorecard.md`](../harness/experiments/wiki_ctx_ab_v1/scorecard.md) §P1 · [`conclusion_p1_zh.md`](../harness/experiments/wiki_ctx_ab_v1/conclusion_p1_zh.md)。
- [x] （P2）H-lean vs W（同题集）· `conclusion_p2_zh.md` · 是否默认 `coding_wiki/` 读序。

## 非范围

- 不改 `docs/harness/prompts/`、CI、api/。
- 不重跑 P1 或修改 P1 已冻结 payload 行（除 22 指出的阻塞修复）。

---

## 验收标准

- [x] P1 `scorecard` 含每题 × 两臂的 `payload_char_count`、正确性 pass/fail。
- [x] `conclusion_p1_zh.md` 明确：推荐 T3 Harness 推广（已 accepted）。
- [x] （P2）`conclusion_p2_zh.md` 明确：是否默认先读 `coding_wiki/`（**推荐是**）。

---

## 实现备忘（由执行 Agent 回填）

| 类别 | 路径 / 值 |
|------|------|
| **30 执行** | 2026-05-26 · model `composer-2.5` · temp `0` |
| **payload_char_count** | H-lean **9896** · W **2096**（降幅 78.8%） |
| **P2 结论** | [`conclusion_p2_zh.md`](../harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md)（accepted · 推荐默认 `coding_wiki/`) |
| **invoke** | `docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_{22,30,40,50}_wiki-ctx-ab-p2-v1.md` |
| **22 R1** | `docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md` |
| **W 物化** | `python tools/wiki_ctx_ab_materialize_w.py` → `payloads/W_harness-p1-docs-consolidation.md` |
| **50** | `docs/tasks/reinspect_results/reinspect_wiki_ctx_ab_p2_*_v1.md` |
| **40 自检** | 2026-05-26 · VERIFY (1)–(7) 全 pass |
| **下一棒** | **50**（`PROMPT_50_startup_wiki-ctx-ab-p2-v1.md`） |

---

### 自检结论（执行者）

| 项 | 结果 |
|----|------|
| **帽** | **40**（P2 自检 · 2026-05-26） |
| **cwd** | `ai-ink-brain-api-python/` · 分支 `task/wiki-ctx-ab-p2-v1` |
| **test_strategy** | `not_applicable`（纯文档实验；未跑 pytest） |

#### 30 产出核对（通读）

| 检查项 | 结果 |
|--------|------|
| `scorecard.md` §P2 八行（Q1–Q4 × H-lean/W） | pass · 均为 **pass** |
| `payload_char_count` H-lean/W | 9896 / 2096 · 降幅 78.8% |
| `conclusion_p2_zh.md` SPEC §3.1（T7+T8） | pass |
| **默认读序**（task 验收 P2） | **是** — §3 写明推荐先读 `docs/coding_wiki/index.md` + `syntheses/<slug>.md` |
| 30 invoke | `invoke_20260526_30_wiki-ctx-ab-p2-v1.md` |

#### VERIFY 验收表（40 · 子仓根）

| # | 命令 / 检查 | exit | pass/fail | 要点 |
|---|-------------|------|-----------|------|
| 1 | `test -f …/payloads/TEMPLATE-W.md` | 0 | **pass** | 模板存在 |
| 2 | `test -f …/W_harness-p1-docs-consolidation.md` | 0 | **pass** | W 物化实例存在 |
| 3 | `test -f docs/coding_wiki/syntheses/harness-p1-docs-consolidation.md` | 0 | **pass** | T1b ingest 页存在 |
| 4 | `rg '^## P2' scorecard.md` + §P2 表 8 行 | 0 | **pass** | L115 主表；Q1–Q4×2 臂均 **pass** |
| 5 | `test -f …/conclusion_p2_zh.md` | 0 | **pass** | P2 结论文存在 |
| 6 | `git diff --name-only -- docs/harness/prompts/ \| wc -l` | 0 | **pass** | 计数 **0**（未改 prompts） |
| 7 | `python tools/wiki_ctx_ab_materialize_w.py --slug …`（可选） | 0 | **pass** | 可再生 · `payload_char_count=2096` |

**40 总评**：**pass** — P2 实验产物与 task 验收对齐；**未改** scorecard 答题原文。下一棒：**50** 独立复检。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | 初稿 `draft` |
| 2026-05-26 | P2 帽链启动稿 22→50→CLOSE；T1b done；`TEMPLATE-W` + W 物化预备 |
