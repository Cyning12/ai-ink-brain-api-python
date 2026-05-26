# Task：Coding Wiki T1c — 测试迭代过程档案（v1）

> **状态**：`in_progress`  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)（**T1c** · §5.1 P1）  
> **关联对比表**：[`docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md)  
> **前置（done）**：[`task_coding_wiki_pilot_v1.md`](../done/task_coding_wiki_pilot_v1.md) · [`task_wiki_ctx_ab_v1.md`](../done/task_wiki_ctx_ab_v1.md)

> 落盘规则：验收通过后 `git mv` 至 `docs/tasks/done/` 并更新 `_views/done.md`、`RECENT_TASK_SCHEDULE.md` §6.6。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯文档：Wiki 测试**过程**存档；不新增 pytest、不改 CI。 |
| **freeze_id** | `CODING-WIKI-T1C@2026-05-26` |
| **gates_before_code** | `["human_gate", "failure_paths", "必读列表"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/coding-wiki-t1c-v1` |
| **task_slug** | `coding-wiki-t1c` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1, 30 | 人扫 task 与 ingest 名单 |
| HG-T1C-INGEST-SCOPE | approved | 30 | 人确认本期 **2** 个测试相关 done task（见下表） |

### 前置条件（开工前自检）

| # | 条件 | 状态 |
|---|------|------|
| P1 | T1b pilot、`docs/coding_wiki/` 骨架存在 | **已满足** |
| P2 | Wiki-CTX-AB P2 签收、默认读序已写 SPEC | **已满足** |
| P3 | `HG-TASK-DRAFT`、`HG-T1C-INGEST-SCOPE` = `approved` | **已满足**（2026-05-26 人签） |

---

## 帽子顺序（计划：**22 → 30 → 40 → 50 → 关账**）

| 序 | 帽 | 启动 Prompt |
|----|-----|-------------|
| 1 | **22 R1** | `docs/harness/invokes/by-task/coding-wiki-t1c/PROMPT_22_startup_coding-wiki-t1c-v1.md` |
| 2 | **30** | `…/PROMPT_30_startup_coding-wiki-t1c-v1.md` |
| 3 | **40** | `…/PROMPT_40_startup_coding-wiki-t1c-v1.md` |
| 4 | **50** | `…/PROMPT_50_startup_coding-wiki-t1c-v1.md` |
| 5 | **关账** | `…/PROMPT_CLOSE_coding-wiki-t1c-v1.md` |

| 帽 | 说明 |
|----|------|
| **10** | **跳过**（task 已起草） |
| **22** | 审查 md → `reviews/by-task/coding-wiki-t1c/` |
| **30** | 交付 T1c 扩域（decisions、concept、ingest §测试变更） |
| **40** | VERIFY + 回填 §自检结论 |
| **50** | `reinspect_results/` |

**纪律**：每帽 **新对话** + Open **`ai-ink-brain-api-python/`**；分支 **`task/coding-wiki-t1c-v1`**（禁止在 `main` 连续提交）。

### 本期 ingest 名单（`HG-T1C-INGEST-SCOPE` 锁定 · 2 个）

| # | done task（相对子仓根） | 预期 Wiki 动作 |
|---|-------------------------|----------------|
| 1 | `docs/tasks/done/task_05_query_rewrite_observability.md` | 新建 `syntheses/query-rewrite-observability.md`（含 **§测试变更**） |
| 2 | `docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md` | 新建 `syntheses/chatbi-v3-text2sql-tool-latency-obs.md`（含 **§测试变更**） |

> 已有 synthesis 的 done task **本期的不要求重做**；仅上表 2 个为硬交付。

---

## 背景与目标

T1b/P2 已证明 **Coding Wiki** 可显著减少 Harness 历史回溯上下文。T1c 在 **不替代 pytest / coverage / `_test_manifest`** 前提下，把 **测试增删改查的过程**（意图、范围、退役原因）写入 L2，便于后续 Agent 理解「为何这样测」。

**完成态**：

1. `docs/coding_wiki/decisions/` 存在且 **≥1** 条 append-only 决策（可来自上表 ingest 中的退役/暂不测结论）。  
2. `docs/coding_wiki/concepts/test-strategy-ink-backend.md`（或人批准的同义 slug）描述跨 Epic 测试策略指针（链 L0 `ERR_*`、L1 `failure_paths`）。  
3. 上表 **2** 个 done task 各 **1** 张 synthesis，且含 **`## 测试变更`**（新增/删除/修改的测试路径 + pointer）。  
4. 更新 `index.md`、`log.md`；`CODING_WIKI.md` §8 与交付一致（若需微调仅文档）。  
5. 22/40/50 落盘；关账后 `RECENT_TASK_SCHEDULE` §6.6 标 T1c **done**。

---

## 范围

- [ ] 新建 `decisions/` 与首条决策记录（append-only）。  
- [ ] 新建 `concepts/test-strategy-ink-backend.md`（frontmatter 合规）。  
- [ ] 上表 2 个 done task → `syntheses/` + `index` + `log`。  
- [ ] 每张新 synthesis 含：`source_task`、`## 测试变更`、pointer → `tests/` 与相关 `failure_paths` / 图谱节点（文字即可）。  
- [ ] 22 R1 审查：无双真值、未复制 review 全文、未改 `docs/harness/prompts/`。

## 非范围

- 新建或修改 `tests/`、CI workflow、`_test_manifest.json`。  
- 跑 Wiki-CTX-AB **多 slug** 对照实验（另立 task，见 SPEC §5.1 P1 第二行）。  
- 复制 Karpathy 式 Raw 库或 `entities/` 全网。  
- 改 `api/`、`_tech_graph/` 流程图正文（仅允许 pointer）。

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| Schema | `docs/coding_wiki/CODING_WIKI.md` §8–§9 |
| 治理路线图 | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` |
| 图谱测评（工具链分工） | 治理仓 `11_REVIEW_L3_L2理论层缺口分析_v1_zh.md` L2-2 |
| 实践文 | `docs/diary/2026-05-26-llm-wiki-harness-pilot-practice.md` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | Wiki 与 L1 `freeze_id` 矛盾 | 标 synthesis「待人工」；不以 Wiki 为准 | 是 | Agent 回 L1 |
| F2 | 将 pytest 清单当 Wiki 真值维护 | 22 阻塞；删清单式正文 | 是 | 审查意见 |
| F3 | `HG-T1C-INGEST-SCOPE` pending | 30 拒开工 | 是 | 等人签 gate |

---

## 验收标准

- [ ] `decisions/` ≥1 文件；`concepts/test-strategy-ink-backend.md` 存在且在 `index.md` 登记。  
- [ ] 2 张新 synthesis 含 `## 测试变更` 与有效 `source_task`。  
- [ ] 40 VERIFY 全 pass；50 建议关账无阻塞。  
- [ ] `git diff` 无 `api/`、无 `docs/harness/prompts/`。  
- [ ] task 关账：`done/` + `_views/done.md` + §6.6 T1c **done**。

---

## 实现备忘（30 帽回填）

| 类型 | 路径 |
|------|------|
| Wiki | `docs/coding_wiki/decisions/`、`concepts/`、`syntheses/` |
| Harness | `docs/harness/invokes/by-task/coding-wiki-t1c/`、`reviews/by-task/coding-wiki-t1c/` |

### 自检结论（执行者）

（40 帽填写）

---

## 给 Cursor

`task_coding_wiki_t1c_test_archive_v1`、`CODING-WIKI-T1C`、`T1c`、`测试迭代档案`、`decisions`、`test-strategy`、`semi_auto`、`coding-wiki-t1c`
