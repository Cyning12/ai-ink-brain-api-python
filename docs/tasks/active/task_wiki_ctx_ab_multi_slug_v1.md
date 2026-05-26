# Task：Wiki-CTX-AB 多 slug 对照（P2 扩域 · v1）

> **状态**：`active` — 待 **22 R1** 与人工闸 `approved` 后执行  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) **§5.1 P1 多 slug AB**  
> **对比表**：[`docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md)（#46 单 Epic 外推局限）  
> **前置（done）**：[`task_wiki_ctx_ab_v1.md`](../done/task_wiki_ctx_ab_v1.md) P2 accepted · [`task_coding_wiki_t1c_test_archive_v1.md`](../done/task_coding_wiki_t1c_test_archive_v1.md)  
> **10 帽起草**：2026-05-26 · invoke `docs/harness/invokes/by-task/wiki-ctx-ab-multi/invoke_20260526_10_wiki-ctx-ab-multi-v1.md`

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/` 并更新 `_views/done.md`、`RECENT_TASK_SCHEDULE.md` §6.6。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 对照实验填表 + 结论文；不新增 pytest、不改 `api/` / CI。 |
| **freeze_id** | `WIKI-CTX-AB-MULTI@2026-05-26` |
| **gates_before_code** | `["human_gate", "failure_paths", "必读列表"]` |
| **semi_auto** | `true`（无 `pending` 闸时可连跑；**建议** 22 单独会话后 30→关账） |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-ctx-ab-multi-slug-v1` |
| **task_slug** | `wiki-ctx-ab-multi` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | **pending** | 22-R1, 30 | 人扫 task、题集、slug 名单 |
| HG-AB-MULTI-SLUGS | **pending** | 30 | 人确认本期 **恰好 2** 个 slug（见下表，勿擅自增删） |
| HG-AB-P2-BASELINE | **pending** | 30 | 人确认 P2 单 slug 已 accepted（`conclusion_p2_zh.md`） |

### 本期锁定 slug（`HG-AB-MULTI-SLUGS` · 2 个）

| # | slug | synthesis（须 `test -f`） | done task |
|---|------|---------------------------|-----------|
| 1 | `tech-graph-gate-d-v2-tasks` | `docs/coding_wiki/syntheses/tech-graph-gate-d-v2-tasks.md` | `docs/tasks/done/task_engineering_tech_graph_gate_d_v2_tasks_v1.md` |
| 2 | `query-rewrite-observability` | `docs/coding_wiki/syntheses/query-rewrite-observability.md` | `docs/tasks/done/task_05_query_rewrite_observability.md` |

> **域差异**：#1 图谱/闸口 D · #2 RAG 可观测 + T1c §测试变更。用于削弱「仅 harness-p1-docs 单 slug」外推。

---

## 帽子顺序（计划：**10 跳过** · **22 → 30 → 40 → 50 → 关账**）

| 序 | 帽 | 启动 Prompt |
|----|-----|-------------|
| 1 | **22 R1** | [`docs/harness/invokes/by-task/wiki-ctx-ab-multi/PROMPT_22_startup_wiki-ctx-ab-multi-v1.md`](../harness/invokes/by-task/wiki-ctx-ab-multi/PROMPT_22_startup_wiki-ctx-ab-multi-v1.md) |
| 2 | **30** | [`…/PROMPT_30_startup_wiki-ctx-ab-multi-v1.md`](../harness/invokes/by-task/wiki-ctx-ab-multi/PROMPT_30_startup_wiki-ctx-ab-multi-v1.md) |
| 3 | **40** | [`…/PROMPT_40_startup_wiki-ctx-ab-multi-v1.md`](../harness/invokes/by-task/wiki-ctx-ab-multi/PROMPT_40_startup_wiki-ctx-ab-multi-v1.md) |
| 4 | **50** | [`…/PROMPT_50_startup_wiki-ctx-ab-multi-v1.md`](../harness/invokes/by-task/wiki-ctx-ab-multi/PROMPT_50_startup_wiki-ctx-ab-multi-v1.md) |
| 5 | **关账** | [`…/PROMPT_CLOSE_wiki-ctx-ab-multi-v1.md`](../harness/invokes/by-task/wiki-ctx-ab-multi/PROMPT_CLOSE_wiki-ctx-ab-multi-v1.md) |

| 帽 | 说明 |
|----|------|
| **10** | **跳过**（本单已由 10 帽起草 task + 题集草案 + Prompt 链） |
| **22** | 审 slug/题集/载荷模板；准许 30 |
| **30** | 物化 H-lean/W × 2 slug · 跑题 · `scorecard` §Multi · `conclusion_multi_slug_zh.md` |
| **40** | VERIFY 实验产物 |
| **50** | `reinspect_results/` |
| **关账** | `done/` + 排期 + 对比表 #46 |

**纪律**：每帽 **新对话** + Open **`ai-ink-brain-api-python/`**；**禁止在 `main` 上连续提交**。

---

## 背景与目标

P2 已在单 slug `harness-p1-docs-consolidation` 上证明 **H-lean vs W**（降幅 78.8%、4/4）。SPEC §5.1 要求对 **至少 2 个异域 slug** 复跑 **对照实验二**（精简 Harness 包 vs 仅 Wiki），评估结论是否可外推。

**完成态**：

1. 每个锁定 slug 各有 **H-lean**、**W** 物化 payload（字符数可填 scorecard）。  
2. 按 [`questions.md`](../harness/experiments/wiki_ctx_ab_multi_slug_v1/questions.md) 每 slug **4 题 × 2 臂** 落盘 scorecard。  
3. [`conclusion_multi_slug_zh.md`](../harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md) 写明：两 slug 是否均满足「W 相对 H-lean 降幅 ≥30% 且正确性不降」；若否，列局限与是否仍推荐默认 Wiki 读序。  
4. **不**修改 `wiki_ctx_ab_v1/` 已冻结 P1/P2 行与 `conclusion_p2_zh.md`。

---

## 范围

- [ ] 实验目录 `docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/`（payloads、scorecard、结论文）。  
- [ ] 每 slug 物化 `H-lean_<slug>.md`、`W_<slug>.md`（W 可 `python tools/wiki_ctx_ab_materialize_w.py --slug <slug>`，输出 **复制** 至本实验 `payloads/`，**禁止覆盖** `wiki_ctx_ab_v1/payloads/` 既有文件）。  
- [ ] H-lean 按本实验 [`payloads/TEMPLATE-H-lean.md`](../harness/experiments/wiki_ctx_ab_multi_slug_v1/payloads/TEMPLATE-H-lean.md) 摘录（done task + harness README 节选；**禁止** invoke/review 全文）。  
- [ ] 跑题并填 `scorecard.md` §Multi（见题集）。  
- [ ] `conclusion_multi_slug_zh.md` + 可选更新 SPEC §5.1 / 对比表 #46 一行结论（关账帽或人审后）。

## 非范围

- 不重跑 P1 H-full vs H-lean；不重跑 P2 单 slug（只读 `conclusion_p2_zh.md`）。  
- 不改 `docs/harness/prompts/`、`api/`、CI、`.github/workflows/`。  
- 不新增/修改 `docs/coding_wiki/syntheses/` 正文（除非 22 发现 blocking 事实错误 — 须单列清单请人确认）。  
- 不做 T1c 式 ingest 或 `decisions/` 扩域（另 task）。  
- 第三 slug、entities 织网、L2 工具链 manifest（SPEC P2 另项）。

---

## 依赖与必读

| 路径 | 用途 |
|------|------|
| `docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md` | P2 基线与方法论 |
| `docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/questions.md` | Gold 题（10 帽草案 · 22 可修订） |
| `docs/coding_wiki/index.md` | W 臂 index 片段 |
| `docs/coding_wiki/CODING_WIKI.md` | 消费纪律 |
| `tools/wiki_ctx_ab_materialize_w.py` | W 物化（`--slug`） |

---

## 验收标准

- [ ] `HG-TASK-DRAFT`、`HG-AB-MULTI-SLUGS`、`HG-AB-P2-BASELINE` = **approved**。  
- [ ] 22 R1 落盘 · 准许 30。  
- [ ] 每 slug：`payloads/H-lean_*.md`、`payloads/W_*.md` 含 `payload_char_count`。  
- [ ] `scorecard.md` §Multi：每题 × 每 slug × 两臂有 pass/fail + 字符数。  
- [ ] `conclusion_multi_slug_zh.md` 含 SPEC 两问（每 slug + 汇总）。  
- [ ] 40 VERIFY 全 pass；50 建议关账。  
- [ ] `git diff` 无 `api/`、`docs/harness/prompts/`、`tests/`。  
- [ ] 关账：`done/` + `_views/done.md` + `RECENT_TASK_SCHEDULE` §6.6。

---

## 失败路径

| ID | 触发 | 系统行为 | 可重试 |
|----|------|----------|--------|
| F1 | synthesis 缺失或 slug 与 `HG-AB-MULTI-SLUGS` 不一致 | 22/30 **拒开工** | 人改闸或补 Wiki |
| F2 | W 臂答题引用 `docs/harness/` / `docs/tasks/done/` 全文 | scorecard 记 **幻觉**；结论倾向 **不通过** | 重跑该题 |
| F3 | 误覆盖 `wiki_ctx_ab_v1/payloads/*` P2 冻结文件 | 40 **fail**；回滚该路径 | 从 git 恢复 |
| F4 | 单 slug 正确性 4/4 但另一 slug &lt;4/4 | 结论文写 **部分外推**；不自动否定 P2 | 可选增 slug 另开 task |

---

## 实现备忘（由执行 Agent 回填）

| 类别 | 路径 |
|------|------|
| 实验目录 | `docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/` |
| invoke | `docs/harness/invokes/by-task/wiki-ctx-ab-multi/invoke_*` |
| 22 R1 | `docs/harness/reviews/by-task/wiki-ctx-ab-multi/` |
| 50 | `docs/tasks/reinspect_results/reinspect_wiki_ctx_ab_multi_*_v1.md` |

### 自检结论（执行者）

（40 帽填写 VERIFY 表）

---

## 给 Cursor

`task_wiki_ctx_ab_multi_slug_v1`、`WIKI-CTX-AB-MULTI`、`多 slug`、`H-lean`、`W`、`tech-graph-gate-d-v2-tasks`、`query-rewrite-observability`、`wiki-ctx-ab-multi`
