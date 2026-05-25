# Payload · H-lean（P1 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `H-lean` |
| **task_slug** | `harness-p1-docs-consolidation` |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **generated** | 2026-05-25 · `python3` 拼接 |

## Agent 约束

只能依据下文作答；**禁止** invoke/review 全文。

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

## 2. 目录结构

```text
docs/harness/
  README.md
  ACCEPTANCE_LANDING.md
  HARNESS_V2_PLAN.md
  SDD_HAT_FLOW.md
  prompts/
    hats/                   # 10～50 帽正文
    templates/              # TEMPLATE-*-invoke
    handoff/                # HANDOFF_*
    README.md
  invokes/by-task/<slug>/   # §2.1
  reviews/by-task/<slug>/   # §2.1
```

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

## 3. 关账最低要求（摘要）

--- FILE: docs/harness/invokes/README.md ---
# docs/harness/invokes（新快照落盘）

> **用途**：本仓 `docs/tasks/` 任务在 **每顶帽子新开局** 时，将已替换占位符的 `TEMPLATE-*` **§3 全文** 存一份于此。  
> **历史快照**（2026-05 图谱/闸口等 ~50 份）已迁至 [`../../diary/harness-archive/invokes/`](../../diary/harness-archive/invokes/)，**非必读**。

---

## 命名

`invoke_YYYYMMDD_<帽号>_<slug>.md`（例：`invoke_20260525_30_chatbi-v3-p2-1a-health.md`）

## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状（2026-05-25）** | 已迁至 `invokes/by-task/<task_slug>/` |
| **新文件** | 仅落 `invokes/by-task/<task_slug>/invoke_*.md`（例 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。

## 规则（摘要）

1. **同一帽**多轮追问 **不** 重复落盘；换帽才新建文件。  
2. 与 task 同 **`git_branch`** 提交；并行任务用独立 worktree（见 [`../README.md`](../README.md) §3）。  
3. 审查结论：用 **`docs/tasks/review_results/`**（20 帽）或 task 正文，**不**使用已移除的 `harness/reviews/`。

--- FILE: docs/tasks/done/task_harness_p1_docs_consolidation_v1.md ---
# Task：巩固 Harness P1 文档（P1-3 → P1-2）

> **状态**：done（2026-05-23 验收通过 · HG-REINSPECT 人签）  
> **关联图谱**：`docs/_tech_graph/99_spec.md`（工程规约）  
> **关联 Issue/PR**：待补（本任务目标为一个 task + 一个 PR）  
> **前端依赖**：无

> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/*.md` 索引。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) **§5**；半自动 / 人工闸：[`docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md`](../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯文档治理改动（`docs/tasks/` 下 README 与 skills 目录），不涉及运行时代码、API、SQL、CI 行为变更。 |
| **freeze_id** | `HARNESS-P1-DOCS@2026-05-23` |
| **gates_before_code** | `["human_gate", "failure_paths", "必读列表"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/harness-p1-docs-consolidation` |

### 人工闸 `human_gate`

> **仅人** 可将 `pending` 改为 `approved`；Agent 遇阻塞帽 **拒执行** 所列 `blocks_hats`。

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | task 初稿由人扫后改 `approved`；在此之前仅允许停留在 10 帽。 |
| HG-REINSPECT | approved | done | （可选）50 复检后由人签收再归档 done / 合并。 |

---

## 背景与目标

对齐 `RECENT_TASK_SCHEDULE` §0.4 的 Harness P1 巩固计划，在本后端仓以 **一个任务单 + 一个 PR** 完成两项文档治理：先补 `human_gate` 场景速查（P1-3），再落 `docs/tasks/skills/README.md` 的 6 类 SKILL 说明（P1-2），并形成可审可执行的闭环输入给 22/30 帽。

---

## 范围

- [x] **P1-3（先做）**：更新 `docs/tasks/README.md`，新增 `human_gate` 场景速查表，字段至少包含：`gate_id`、`status`、`blocks_hats`、`典型场景`、`谁可改 approved`。  
- [x] **P1-2（后做）**：新增目录 `docs/tasks/skills/` 与 `docs/tasks/skills/README.md`，定义 6 类 SKILL（含关账蒸馏与人审口径）。  
- [x] 在 `docs/tasks/README.md` 补充到 `docs/tasks/skills/README.md` 的可发现入口（索引链路）。  
- [x] 所有新增或改动文档采用 UTF-8、相对路径引用，不写绝对本机路径。  

## 非范围

- `Projects/docs/harness/reviews/` pointer 调整（P1-1，工作区仓）。  
- 任何 `api/` 代码、数据库脚本、测试实现与 CI workflow 变更。  
- 前端仓 Harness parity（P1-4）。  

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 排期真值 | [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §0.4 |
| 任务模板 | [`docs/tasks/templates/TASK_TEMPLATE.md`](../templates/TASK_TEMPLATE.md) |
| 本仓任务规则 | [`docs/tasks/README.md`](../README.md) |
| Harness 字段真值 | [`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) §5 |
| 半自动与状态栏 | [`docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md`](../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md) |
| 10 帽规则 | [`docs/harness/prompts/hats/10-requirements.md`](../../harness/prompts/10-requirements.md) |
| 关账与人审口径参考 | `docs/diary/2026-05-22-harness-evaluation-improvement-response.md` §九（执行时按需核对） |

---

## 给执行帽的执行顺序（硬）

1. **P1-3**：先完成 `docs/tasks/README.md` 的 `human_gate` 场景速查。  
2. **P1-2**：再新增 `docs/tasks/skills/README.md`，写 6 类 SKILL。  
3. 回填自检与复检材料时，按 `audit_profile: post_close` 执行闸口。  

---

## 失败路径

> 本任务为文档治理，失败路径定义为「流程与口径失败」，用于阻止错误推进。

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | 未先完成 P1-3 就直接做 P1-2 | 判定为顺序不合规，30 帽应停止并回到步骤 1 | 是 | 审查结论标记为流程阻塞 |
| F2 | `human_gate` 表缺必填列或写成不可执行口径 | 22 帽给出阻塞项，禁止进入 done | 是 | review 中给出回填清单 |
| F3 | 6 类 SKILL 与 §九 / HARNESS_V2 §5 语义冲突且未单列 | 22 帽标记为口径冲突，要求补「矛盾小节」后再审 | 是 | review 中给出冲突条目 |
| F4 | 改动越界到 API/CI/SQL | 视为超范围改动，要求拆分并回滚越界部分 | 是 | PR 评论或 review 阻塞 |

---

## 验收标准

- [x] `docs/tasks/README.md` 新增 `human_gate` 场景速查，含 5 列：`gate_id`、`status`、`blocks_hats`、`典型场景`、`谁改 approved`。  
- [x] 新增 `docs/tasks/skills/README.md`，明确 6 类 SKILL、适用阶段、输入输出与关账蒸馏/人审口径。  
- [x] `docs/tasks/README.md` 出现到 `docs/tasks/skills/README.md` 的入口链接。  
- [x] task 内保留「矛盾单列」要求：若 §九 与 HARNESS_V2 §5 不一致，必须单独小节列出而非混写。  
- [x] 非范围项未被触及（无 `api/`、CI workflow、前端仓改动）。  

**测试 / TDD（与 `test_strategy` 对齐）**：

| test_strategy | 自检须含 |
|---------------|----------|
| `not_applicable` | 在 `### 自检结论（执行者）` 明确「纯 docs 变更」理由，并给出目录与文件检查结果。 |

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（项目通用要求；本任务可标记为“未触发代码路径”并说明）。

> **H-lean 截断**：下文 40 自检 / 50 复检 / 实现备忘 **未纳入** 本载荷（纪律消费）。

--- FILE: docs/tasks/RECENT_TASK_SCHEDULE.md ---
### 0.4 阶段 P1 — 巩固（**已收口**）


| #    | 任务                                                   | 状态       | 说明                                                                                                        |
| ---- | ---------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------- |
| P1-1 | 工作区 `Projects/docs/harness/reviews/` pointer 改索引/删悬空 | **done** | Projects `main` `c8f3d8c` · `docs/harness/tasks/done/task_harness_p1_reviews_pointers_v1.md` · 2026-05-23 |
| P1-2 | `docs/tasks/skills/` + README（6 类 SKILL，关账蒸馏+人审）     | **done** | `task_harness_p1_docs_consolidation_v1` · PR #49 · 2026-05-23                                             |
| P1-3 | `docs/tasks/README.md` `human_gate` 场景速查表            | **done** | 同上                                                                                                        |
| P1-4 | 前端 `ai-ink-brain` **Harness parity**（模板/rsync/规则同步）  | **远期**   | ≠ V3 **P1-4 §4.3 烟测**（已 done，见 §5）                                                                        |
| P1-5 | 历史 review 样例                                         | **已做**   | 10 份 + `task_05` 新 R1，`reviews/README`                                                                    |


**P1 巩固**：P1-1～P1-3 **全部 done**（2026-05-23）；工作区 pointer 与后端文档批分仓交付完成。

---

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 9896 |
| `file_count` | 4 |
| `notes` | done task 截断至验收/必绿说明；无 invoke；无 40/50 回填 |
