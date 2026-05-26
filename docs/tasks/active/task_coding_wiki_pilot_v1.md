# Task：Coding Wiki 试点（LLM Wiki 模式 · 后端 · v1）

> **状态**：`active`（`HG-TASK-DRAFT` / `HG-WIKI-INGEST-SCOPE` 已 **approved** · 可开 22 或 30）  
> **关联图谱**：`docs/_tech_graph/99_spec.md`（工程规约；本 task 不修改流程图正文）  
> **关联 Issue/PR**：无  
> **前端依赖**：无  
> **指导意见（对话归档）**：[`docs/harness/guides/README.md`](../../harness/guides/README.md)（指针 → 工作区 `GUIDANCE_coding_wiki_llm_wiki_insert_v1_zh.md`）

> 落盘规则：验收通过后 `git mv` 至 `docs/tasks/done/` 并更新 `_views/*.md`。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯文档与目录骨架；无运行时代码与 CI 行为变更。 |
| **freeze_id** | `CODING-WIKI-PILOT@2026-05-25` |
| **gates_before_code** | `["human_gate", "failure_paths", "必读列表"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/coding-wiki-pilot-v1` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1, 30 | 人扫 task 与 `GUIDANCE_*` 后改 `approved` |
| HG-WIKI-INGEST-SCOPE | approved | 30 | 人确认首期 ingest 的 2～3 个 `done` task 名单 |

### 前置条件（开工前自检）

| # | 条件 | 2026-05-25 状态 |
|---|------|-----------------|
| P1 | 后端 Harness **P1-1～P1-3** 已收口 | **已满足**（见 `RECENT_TASK_SCHEDULE.md` §0.4） |
| P2 | `docs/tasks/` 规整（INK-P6）已关 | **已满足**（`task_docs_tasks_reorg_move_v1` done · 2026-05-22） |
| P3 | 工作区 Harness `active/` 无常驻改版 task | **已满足** |
| P4 | 本 task `HG-TASK-DRAFT` = `approved` | **已满足** |

> **说明**：**P1-4 前端 Harness parity** 为远期项，**不**作为本 task 硬前置。若你仍希望等「全栈 parity」，可将本 task 保持 `draft` 直至 P1-4 立项——与指导意见 §5 二选一，须在 `HG-TASK-DRAFT` 备注中写明。

---

## 帽子顺序（计划：**22 → 30 → 40 → 50 → 关账**）

| 序 | 帽 | 启动 Prompt（子仓） |
|----|-----|----------------------|
| 1 | **22 R1** | `docs/harness/invokes/by-task/coding-wiki-pilot/PROMPT_22_startup_coding-wiki-pilot-v1.md` |
| 2 | **30** | `…/PROMPT_30_startup_coding-wiki-pilot-v1.md` |
| 3 | **40** | `…/PROMPT_40_startup_coding-wiki-pilot-v1.md` |
| 4 | **50** | `…/PROMPT_50_startup_coding-wiki-pilot-v1.md` |
| 5 | **关账** | `…/PROMPT_CLOSE_coding-wiki-pilot-v1.md` |

| 帽 | 说明 |
|----|------|
| **10** | **跳过**（task 已完整；非新建 SPEC） |
| **22** | **必须先做**；审查 md 落 `reviews/by-task/coding-wiki-pilot/` |
| **30** | 交付 `docs/coding_wiki/` + ingest 三件套 |
| **40** | 独立跑 VERIFY + 回填 §自检结论 |
| **50** | 复检 + `docs/tasks/reinspect_results/`；纯文档仍 **建议做** |

**纪律**：每帽 **新对话** + Open **`ai-ink-brain-api-python/`**；见 [`docs/harness/ACCEPTANCE_LANDING.md`](../harness/ACCEPTANCE_LANDING.md)。

### 首期 ingest 名单（`HG-WIKI-INGEST-SCOPE` 已锁定）

| # | done task（相对子仓根） |
|---|-------------------------|
| 1 | `docs/tasks/done/task_harness_p1_docs_consolidation_v1.md` |
| 2 | `docs/tasks/done/task_engineering_tech_graph_gate_d_v2_tasks_v1.md` |
| 3 | `docs/tasks/done/task_docs_tasks_reorg_move_v1.md` |

---

## 背景与目标

在后端 AI coding 场景引入 **LLM Wiki / Coding Wiki** 编译层：将 **已关账** 的 SDD + Harness + TDD 过程产物蒸馏为互链 Markdown，供后续 Agent **省 token、提准确率、易回溯**。

**Harness 落盘 taxonomy（先于 Wiki ingest 定稿）**：[`docs/harness/README.md`](../harness/README.md) **§2.1** — `prompts/{hats,templates,handoff}`、`invokes/by-task/`、`reviews/by-task/`；**不**建 `prompts/domains/`（域知识归 Wiki，invoke/review 按 task 绑定）。

**完成态（试点）**：

1. 存在 `docs/coding_wiki/` 目录与 `CODING_WIKI.md` schema（ingest / query / lint 约定）。  
2. `index.md`、`log.md` 可导航；至少 **2 张** `syntheses/` 或 `concepts/` 页来自真实 `done` task。  
3. 与 Harness、`_tech_graph` 边界写清；**零** 修改 `docs/harness/prompts/` 与 CI workflow。

---

## 范围

- [x] 新建 `docs/coding_wiki/` 骨架（见指导意见 §7）。
- [x] 编写 `CODING_WIKI.md`：L0/L1/L2 分工、ingest/query/lint、frontmatter 最小集、`[[wikilink]]` 与 pointer 规则。
- [x] 初始化 `index.md`、`log.md`（含 2026-05-26 试点启动与 ingest 条目）。
- [x] **Ingest** 上表 **3** 个 done task（`HG-WIKI-INGEST-SCOPE` 已锁定）
- [x] 每张 ingest 页含：`freeze_id` 或关账日期、链至 task / review（**摘要**，非全文复制）。
- [x] 在 `docs/tasks/README.md` 与 `docs/README.md` 增加 **一行** 入口链至 `coding_wiki/`（避免孤儿目录）。
- [x] 22 帽 R1（`audit_profile: post_close`）：审查 Wiki 与 Harness/图谱无双真值风险。

## 非范围

- 不修改 `docs/harness/prompts/`、不新增/改 Harness 帽子、不把 Wiki ingest 写入 `gates_before_code`。
- 不迁移 `docs/harness/reviews/` 全文至 Wiki（仅 pointer + 摘要）。
- 不替代 `docs/_tech_graph/`、`graph.json`、`_contract_manifest`。
- 不实施 Neo4j（方案 3 / INK-P7）；不强制向量库。
- 不 ingest **active** 进行中 task 入 `syntheses/`（仅可 `log` 一行「进行中」）。
- 不改 `api/`、测试、CI workflow。

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 指导意见 | `docs/harness/guides/README.md`（指针 → 工作区 `GUIDANCE_coding_wiki_llm_wiki_insert_v1_zh.md`） |
| Harness 排期 | `docs/tasks/RECENT_TASK_SCHEDULE.md` §0 |
| Harness V2 字段 | `docs/harness/HARNESS_V2_PLAN.md` §5 |
| 图谱消费 | `docs/_tech_graph/graph_v2_schema.md`、方案 2 查询（按需） |
| 方案 3 留坑 | `docs/tech_graph/` · `改进方向.md` R2/R3 |
| Karpathy 原文 | [llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
| skills 目录 | `docs/tasks/skills/README.md`（Wiki 只链 stub） |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | Wiki 摘要与 task/`freeze_id` 矛盾 | lint 列出冲突；**禁止** 标 syntheses 为「当前真值」 | 修正 ingest 或回链 L0 | Agent 拒答或标注「待人工」 |
| F2 | 复制整份 SPEC/review 进 Wiki | 22 R1 打回：违反非范围 | 改为摘要 + 链接 | 审查 md |
| F3 | 在 Harness 未收口时大批量 ingest | 路径/状态漂移 | 等 P1/P6 后再 ingest | task 保持 draft |
| F4 | `HG-*` 仍为 `pending` | 30 帽拒开工 | 人签后重试 | 缺口清单 |

---

## 验收标准

- [x] `docs/coding_wiki/CODING_WIKI.md` 存在且含 ingest/query/lint 三步与 L0/L1/L2 表。
- [x] `index.md` 列出所有试点页；`log.md` 含至少 1 条 ingest 记录（带日期前缀，可 `grep`）。
- [x] ≥2 张 Wiki 页链回真实 `done` task 路径（相对路径，无绝对本机路径）。
- [x] `docs/harness/prompts/` **未改**（本 task 未改 Harness 执行链；见 40 自检 `git diff`）。
- [x] 22 R1 落盘 `docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md`。
- [ ] （可选）同一问题对比：仅读 Wiki index+2 页 vs 扫 3 个 done task 的 context 行数（留 50 或关账会话）。

---

## 实现备忘（由执行 Agent 回填）

| 类别 | 路径 |
|------|------|
| **task_slug** | `coding-wiki-pilot` |
| **Open Folder** | **`ai-ink-brain-api-python/`**（交付物在本子仓；**不要**只开 Projects 写 `docs/coding_wiki/`） |
| **invoke** | `docs/harness/invokes/by-task/coding-wiki-pilot/invoke_20260526_{22,30,40}_coding-wiki-pilot.md` |
| **22 R1** | `docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md` |
| Wiki 根 | `docs/coding_wiki/`（3× `syntheses/` + 1× `concepts/`） |
| 入口 | `docs/README.md`、`docs/tasks/README.md` 各一行 |
| 治理 SPEC | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` **T1b** |
| **下一棒** | **50** + 关账 → `PROMPT_50_*`、`PROMPT_CLOSE_*`（新 Agent） |

---

### 自检结论（执行者）

| 项 | 结果 |
|----|------|
| **帽** | 40（2026-05-26） |
| **cwd** | `ai-ink-brain-api-python/` |
| **test_strategy** | `not_applicable` — 纯文档；未跑 pytest（无代码路径） |

**命令与退出码**

```text
test -f docs/coding_wiki/CODING_WIKI.md     → 0
test -f docs/coding_wiki/index.md           → 0
test -f docs/coding_wiki/log.md             → 0
grep '2026-05-26' docs/coding_wiki/log.md   → 匹配
grep ingest docs/coding_wiki/log.md         → 匹配
syntheses/*.md 计数                         → 3（≥2）
git diff --quiet docs/harness/prompts/      → 0（未改 prompts）
```

**验收摘要**：骨架、schema、三份 ingest、双入口、22 R1 零阻塞均已落盘。**待**：50 复检、关账 CLOSE_TRACE、task 归档 `done/`。

---

## 测试策略（Harness）

见头部 **test_strategy: not_applicable**；验收以目录存在性、链接解析、22 审查为主。

---

## 给 Cursor

`Coding Wiki`、`LLM Wiki`、`ingest`、`index.md`、`not_applicable`、`HG-WIKI-INGEST-SCOPE`、`docs/coding_wiki`、Harness 不同环节、done task only

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | 初稿：对话归档后生成；状态 `draft`；前置 P1/P6 已满足 |
| 2026-05-26 | `active`：帽子顺序表；ingest 三件套锁定；22/30 启动 Prompt 路径 |
| 2026-05-26 | 帽链 22→30→40→50→关账；PROMPT_22 v1.2 + 40/50/CLOSE 启动稿 |
| 2026-05-26 | 22/30/40 已执行；Wiki 试点交付；50+关账留待新 Agent |
