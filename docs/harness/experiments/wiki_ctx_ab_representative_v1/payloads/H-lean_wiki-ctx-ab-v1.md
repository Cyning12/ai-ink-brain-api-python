# Payload · H-lean（Representative 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `H-lean` |
| **task_slug** | `wiki-ctx-ab-v1` |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **generated** | 2026-05-27 · `python tools/wiki_ctx_ab_materialize_h_lean.py` |

## Agent 约束

只能依据下文作答。禁止 invoke/review 全文。禁止 `docs/coding_wiki/*`。

---

## 载荷正文

--- FILE: docs/harness/README.md ---
## 1. 日常读什么

| 场景 | 路径 |
|------|------|
| 写 task / **下一棒双 Prompt** | `TEMPLATE-requirements`（**A:22** + **B:30**，人择一） |
| 任务审核 22 | [`reviews/README.md`](reviews/README.md) → `TEMPLATE-task-audit` |
| 执行 + 自检 | `TEMPLATE-execute` → `TEMPLATE-self-check` |
| **三方复检** | `TEMPLATE-independent-reinspect` → [`../tasks/reinspect_results/`](../tasks/reinspect_results/README.md) |
| 半自动 / 人工闸 | `HANDOFF_SEMI_AUTO` |
| commit / 关账 | `HANDOFF_AUTO_COMMIT`、`HANDOFF_CLOSE_TRACE` |
| task 字段 | `HARNESS_V2_PLAN.md` §5 |
| 流程 | `SDD_HAT_FLOW.md` |
| 新 invoke | `invokes/` |
| **Harness 裁决共识（已接受）** | [`../diary/2026-05-22-harness-evaluation-improvement-response.md`](../diary/2026-05-22-harness-evaluation-improvement-response.md) **§九** |

**Cursor**：`.cursor/rules/05-harness-semi-auto.mdc`、`.cursor/rules/06-harness-in-repo.mdc`。

**Agent 禁止（日常）**：

- **禁止** 默认读取工作区 `Projects/docs/harness/`（跨子仓 Harness 任务除外，见 `docs/tasks/README.md`）。
- **禁止** 将子仓 `prompts/` 软链到工作区；真值以 **本仓** `docs/harness/prompts/` 为准。
- **禁止** 在任务执行中运行下文 **§4 `rsync`**（仅维护者偶发同步）。

---

### 2.1 落盘 taxonomy（**已迁移** · 2026-05-25）

**原则**：**按 task 绑定**落盘（`invokes` / `reviews` / `reinspect_results` 已按 task 语义）；**不按业务域分顶层目录**。域知识进 **LLM Wiki**（`task_coding_wiki_pilot_v1`），不进 `prompts/domains/`。

| 树 | 目标路径 | 内容 |
|----|----------|------|
| **prompts** | `prompts/hats/` | `10-requirements` … `50-independent-reinspect` |
| | `prompts/templates/` | `TEMPLATE-*-invoke.md` |
| | `prompts/handoff/` | `HANDOFF_*.md` |
| **invokes** | `invokes/by-task/<task_slug>/` | `invoke_YYYYMMDD_<帽号>_<slug>.md`（见 [`invokes/README.md`](invokes/README.md)） |
| **reviews** | `reviews/by-task/<task_slug>/` | `task_<slug>_audit_R<轮次>_YYYYMMDD.md`（见 [`reviews/README.md`](reviews/README.md)） |
| **50（不变）** | `docs/tasks/reinspect_results/` | 关账复检；文件名可含 task slug |

**为何不建 `prompts/domains/chatbi` 或 `domains/tech-graph`？**

- Harness 文件描述的是**帽序与 HANDOFF 协议**，与「ChatBI / 图谱」等业务域 **正交**；同一 task 常跨多域。
- 按域拆目录会导致：同一 `invoke` 难归类、Agent 误把域片段当关账真值。
- **若将来**需要跨 task 复用的 Prompt **片段**，再用 `prompts/snippets/<domain>/`（可选），与 Wiki 词条分工，**仍不**替代 `by-task/` 落盘。

**新落盘**：invoke / review **必须**进 `by-task/<task_slug>/`；prompts 从 `hats/`、`templates/`、`handoff/` 读取（勿在 `prompts/` 根新增帽文件）。

**落地 task**：[`docs/tasks/active/task_coding_wiki_pilot_v1.md`](../tasks/active/task_coding_wiki_pilot_v1.md) · [`task_wiki_ctx_ab_v1.md`](../tasks/active/task_wiki_ctx_ab_v1.md)（Wiki-CTX-AB）。

**实验（P1 题集 / payload 模板）**：[`experiments/wiki_ctx_ab_v1/`](experiments/wiki_ctx_ab_v1/README.md) · SPEC [`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)。

---

--- FILE: docs/harness/invokes/README.md ---
## 命名

`invoke_YYYYMMDD_<帽号>_<slug>.md`（例：`invoke_20260525_30_chatbi-v3-p2-1a-health.md`）

## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状（2026-05-25）** | 已迁至 `invokes/by-task/<task_slug>/` |
| **新文件** | 仅落 `invokes/by-task/<task_slug>/invoke_*.md`（例 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。
## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状（2026-05-25）** | 已迁至 `invokes/by-task/<task_slug>/` |
| **新文件** | 仅落 `invokes/by-task/<task_slug>/invoke_*.md`（例 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。

## 规则（摘要）

1. **同一帽**多轮追问 **不** 重复落盘；换帽才新建文件。

--- FILE: docs/tasks/done/task_wiki_ctx_ab_v1.md ---
# Task：Wiki-CTX-AB v1（Harness 上下文消费对照 · P1→P2）

> **状态**：`done（2026-05-26 验收通过 · WIKI-CTX-AB@2026-05-25）`  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)  
> **实验目录**：[`docs/harness/experiments/wiki_ctx_ab_v1/`](../harness/experiments/wiki_ctx_ab_v1/README.md)  
> **T1b（done）**：[`task_coding_wiki_pilot_v1.md`](task_coding_wiki_pilot_v1.md) · 同 slug `harness-p1-docs-consolidation`

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
| **50** | [`reinspect_wiki_ctx_ab_p2_20260526_v1.md`](../reinspect_results/reinspect_wiki_ctx_ab_p2_20260526_v1.md)（建议关账 · 无阻塞） |
| **40 自检** | 2026-05-26 · VERIFY (1)–(7) 全 pass |
| **下一棒** | **无**（50 建议关账 · 2026-05-26；本单已 `done/`） |

---

### 自检结论（执行者）

| 项 | 结果 |
|----|------|
| **帽** | **40** + **50**（P2 自检 + 独立复检 · 2026-05-26） |
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

**40 总评**：**pass** — P2 实验产物与 task 验收对齐；**未改** scorecard 答题原文。

**50 复检摘要**：`reinspect_wiki_ctx_ab_p2_20260526_v1.md` — 独立抽检 Q2/Q4、W 载荷边界、T7/T8 一致；**建议关账、无阻塞**。**关账**：`HANDOFF_CLOSE_TRACE` · 归档 `docs/tasks/done/`（2026-05-26）。

---

## 关闭回溯（HANDOFF_CLOSE_TRACE）

**结论**：`freeze_id` `WIKI-CTX-AB@2026-05-25` · Wiki-CTX-AB **P1 + P2** 帽链 **22 → 30 → 40 → 50** 已完成；50 书面复检 **建议关账、无阻塞**；P2 裁决 **推荐默认先读** `docs/coding_wiki/index.md` + `syntheses/<slug>.md`（W 相对 H-lean 降幅 **78.8%**、4/4 pass）；本 task 归档 **`docs/tasks/done/`**（2026-05-26）。

### 执行路线表

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件（相对 `ai-ink-brain-api-python/`） | commit |
|------|-------------|----------|---------------------------------------------|--------|
| 0 | P1（历史） | H-full vs H-lean · scorecard §P1 · `conclusion_p1_zh` accepted | `docs/harness/experiments/wiki_ctx_ab_v1/**` · 初版 task | `api-python@f73eb8c` |
| 1 | 预备 | P2 帽链启动 · TEMPLATE-W · W 物化脚本 | `docs/harness/invokes/by-task/wiki-ctx-ab/PROMPT_{22,30,40,50,CLOSE}_*` · `payloads/TEMPLATE-W.md` | `api-python@bb8496d` |
| 2 | **22** R1 | P2 开工就绪审 · 零阻塞 | `docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md` · `…/invoke_20260526_22_wiki-ctx-ab-p2-v1.md` | `api-python@8126ed3` |
| 3 | **30** | H-lean vs W · scorecard §P2 · `conclusion_p2_zh.md` | `docs/harness/experiments/wiki_ctx_ab_v1/scorecard.md` · `conclusion_p2_zh.md` · `…/invoke_20260526_30_wiki-ctx-ab-p2-v1.md` | `api-python@91045eb` |
| 4 | **40** | VERIFY (1)–(7) · §自检结论 | `…/invoke_20260526_40_wiki-ctx-ab-p2-v1.md` · 本 task `### 自检结论` | `api-python@669debc` |
| 5 | **50** | 独立复检 + 全局验收（T2 / 读序） | `docs/tasks/reinspect_results/reinspect_wiki_ctx_ab_p2_20260526_v1.md` · `…/invoke_20260526_50_wiki-ctx-ab-p2-v1.md` | `api-python@c0e8cfb` |
| 6 | **关账** | `git mv` task · 排期/_views · SPEC §3.1 · 本回溯节 | `docs/tasks/done/task_wiki_ctx_ab_v1.md` | `api-python@0dcd394` |

### 分仓 Commit 索引（api-python · 从新到旧）

```text
### api-python（ai-ink-brain-api-python · branch task/wiki-ctx-ab-p2-v1）
- 0dcd394 docs(task): Wiki-CTX-AB v1 关账 · WIKI-CTX-AB@2026-05-25
- c0e8cfb docs(harness): 完成 Wiki-CTX-AB P2 的 50 复检落盘
- 669debc docs(harness): WIKI-CTX-AB P2 40 自检 VERIFY 全 pass
- 91045eb feat(wiki-ctx-ab): P2 H-lean vs W 对照落盘与结论文
- 8126ed3 docs(harness): 22 audit for wiki-ctx-ab P2 R1
- bb8496d docs(harness): Wiki-CTX-AB P2 帽链启动稿与 W 臂物化预备 (#58)
- f73eb8c docs: Coding Wiki pilot 关账 (T1b) + …（含 P1 scorecard / conclusion_p1）
```

**关联工件**：`freeze_id` `WIKI-CTX-AB@2026-05-25` · `task_slug` `wiki-ctx-ab` · gold slug `harness-p1-docs-consolidation` · 治理 SPEC [`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) **T2**。

**下一 Epic（非本 task）**：全仓 **P1-4** Harness parity（`ai-ink-brain`）· 远期。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | 初稿 `draft` |
| 2026-05-26 | P2 帽链启动稿 22→50→CLOSE；T1b done；`TEMPLATE-W` + W 物化预备 |
| 2026-05-26 | **done**：P2 22→30→40→50 完成；`git mv` → `done/`；`HANDOFF_CLOSE_TRACE` 关账 |

--- FILE: docs/tasks/RECENT_TASK_SCHEDULE.md ---
> **近期当前（治理/工程）**：**P1-4 前端 Harness parity**（全仓 · 远期）；工作区 **T3** taxonomy **done**（2026-05-26 · Projects）；本仓 taxonomy **done**（§6.4）；**Wiki-CTX-AB T2 done**（2026-05-26 · 推荐默认 `coding_wiki/` 读序）。  
| **近期当前** | **P1-4 前端 Harness parity**（全仓 · 远期）← **T2 done**（[`done/task_wiki_ctx_ab_v1.md`](done/task_wiki_ctx_ab_v1.md) · 2026-05-26 · 推荐默认 `coding_wiki/` 读序） |
| ~~**当前**~~ | ~~Coding Wiki pilot（T1b）~~ | ~~治理~~ | **done**（2026-05-26 · [`done/task_coding_wiki_pilot_v1.md`](done/task_coding_wiki_pilot_v1.md)） |
| ~~**当前**~~ | ~~Wiki-CTX-AB P2（T2）~~ | ~~治理~~ | **done**（2026-05-26 · [`done/task_wiki_ctx_ab_v1.md`](done/task_wiki_ctx_ab_v1.md) · 推荐默认 `coding_wiki/` 读序） |
| **P0**    | Text2SQL 可观测     | `done`                                                                                                                                     |
### 6.6 Wiki-CTX-AB · Coding Wiki · 全仓 Harness 推广（2026-05-25）
| **T1b** | **`task_coding_wiki_pilot_v1`** | **done** | 2026-05-26 关账 · [`done/task_coding_wiki_pilot_v1.md`](done/task_coding_wiki_pilot_v1.md) |
| T2 | **`task_wiki_ctx_ab_v1`** · P2（精简包 vs 仅 Wiki） | **done** | 2026-05-26 关账 · [`done/task_wiki_ctx_ab_v1.md`](done/task_wiki_ctx_ab_v1.md) · **推荐默认** `coding_wiki/index` + syntheses（降幅 78.8%、4/4 pass） |
| **T1c** | **`task_coding_wiki_t1c_test_archive_v1`** | **done** | 2026-05-26 关账 · [`done/task_coding_wiki_t1c_test_archive_v1.md`](done/task_coding_wiki_t1c_test_archive_v1.md) · `reinspect_coding_wiki_t1c_20260526_v1.md` |
| T4 | 图谱桥接 / `graph_nodes` | **draft**（Pilot done → 3 slug 扩面） | 链 `SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` · Pilot `query-rewrite-observability` + `chatbi-v3-text2sql-tool-latency-obs` + `tech-graph-gate-d-v2-tasks` · `gov-wiki-t4-expand` |
| **AB 代表性扩面** | **`task_governance_wiki_ctx_ab_representative_v1`** | **draft** | 6 slug P2 · 前端 P1-4 证据 · `task/wiki-ctx-ab-representative-v1` · `WIKI-CTX-AB-REP@2026-05-27` |
| Wiki-CTX-AB 实验   | `docs/harness/experiments/wiki_ctx_ab_v1/`                                                                                         |
| 2026-05-26 | **T2 done**：Wiki-CTX-AB v1 关账 · `WIKI-CTX-AB@2026-05-25` · 推荐默认 `coding_wiki/` 读序；当前棒 **P1-4** 前端 parity |
| 2026-05-26 | **T1c done**：`task_coding_wiki_t1c_test_archive_v1` 关账 · `CODING-WIKI-T1C@2026-05-26` · §6.6 更新 |

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 14798 |
| `file_count` | 4 |
| `notes` | H-lean：README §1+§2.1 + invokes README 摘录 + done task 全文 + RECENT 关键词行 |
