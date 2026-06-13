# Task：后端 docs/tasks done 索引卫生治理（域 Hub + Wiki 链路同步）

> **状态**：draft  
> **关联 Issue/PR**：待开 PR（文档-only）  
> **前端依赖**：无  

> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/*.md` 索引。  
> **Harness 字段真值**：`[docs/harness/HARNESS_V2_PLAN.md](../harness/HARNESS_V2_PLAN.md)` **§5**；链式常模：`[docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md](../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md)` + `[docs/harness/prompts/PROMPT_*_chain_serial_*](../harness/prompts/README.md)`。`**semi_auto` 已 deprecated**（历史见 `[HANDOFF_SEMI_AUTO.md](../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)`）。  
> **行为变更 Delta / Scenario**：见 **§3 失败路径**；TDD 与分层测试决策见 `[docs/tasks/README.md](../README.md)` **§test_strategy**。

---

## Harness 元信息（执行 Agent 必读）


| 字段                     | 值                                                                                                                                  |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **module_id**          | `none`                                                                                                                             |
| **graph_delta**        | `none`                                                                                                                             |
| **graph_delta_note**   | 纯文档索引 + Wiki 指针治理；无 `api/` 拓扑变更                                                                                                    |
| **test_strategy**      | `not_applicable`                                                                                                                   |
| **test_strategy_note** | 无 `api/` 行为变更；验证靠链接自检 + 50 书面复检                                                                                                    |
| **freeze_id**          | （本 task 关账后生成，如 `GOV-TASKS-DONE-HYGIENE@2026-06-13`）                                                                               |
| **gates_before_code**  | `HG-TASK-DRAFT` → `HG-AUDIT-R1` → `HG-REINSPECT`                                                                                   |
| **semi_auto**          | `deprecated` — 新 task 使用链式 orchestration                                                                                           |
| **orchestration**      | `Cursor Task 链` / `Claude Code` 串行（文档-only，无 api 编码）                                                                               |
| **chain_prompt**       | `[docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md](../harness/prompts/PROMPT_cursor_task_chain_serial_v1.md)`（或 CC 等价链） |
| **audit_profile**      | `full`                                                                                                                             |
| **git_branch**         | `task/governance-tasks-done-hygiene-v1`                                                                                            |
| **experience_capture** | `recommended`                                                                                                                      |
| **kpi_rubric**         | `KPI_RUBRIC_v1_2`                                                                                                                  |
| **kpi_aggregator**     | `CLOSE`                                                                                                                            |
| **schedule_ref**       | `RECENT §6.1 / §6.6 · 治理索引卫生 · done 域化 Hub`                                                                                        |
| **epic**               | `治理 · docs/tasks 索引卫生`                                                                                                             |
| **blocked_by**         | RECENT 治理/backlog 锚点；编码规范 Epic CLOSE（W1～W8 done）                                                                                   |
| **blocks**             | 后续 `docs/tasks/done/<domain>/` 物理迁移子 task（P1）                                                                                      |


### 人工闸 `human_gate`

> **仅人** 可将 `pending` 改为 `approved`；Agent 遇阻塞帽 **拒执行** 所列 `blocks_hats`。


| human_gate_id | status   | blocks_hats | 说明                                                |
| ------------- | -------- | ----------- | ------------------------------------------------- |
| HG-TASK-DRAFT | approved | 22-R1, 30   | 初稿 task 人扫：字段完整性、验收可执行性、§3 failure_paths、§4 交接物清单 |
| HG-AUDIT-R1   | approved | 30          | 22 R1 落盘 `docs/harness/reviews/` 后人签，确认零阻塞或阻塞已回填  |
| HG-REINSPECT  | approved | done, 50    | 50 复检落盘 `docs/tasks/reinspect_results/` 后人签关账     |


---

## §1 背景与完成态

当前 `docs/tasks/done/` 已积累约 **138** 篇已关账 task，全部扁平存放；`_views/done.md` 随之膨胀为长列表，导致：

- 日常浏览难以按域定位历史任务；
- Agent 开工前读 `_views/done.md` 消耗大量上下文；
- `docs/tasks/README.md` 归档流程未明确域子目录 + Hub 索引纪律；
- Coding Wiki `concepts/task-schedule-ink-backend` 与 `index.md` 未显式链到 done 索引 Hub，L1/L2 边界易漂移。

**完成态**：

- `docs/tasks/done/README.md` 成为按域分组的 Hub，覆盖 `harness / governance / chatbi / engineering / standards / epics` 等主域；
- `_views/done.md` 退化为 ≤15 行薄指针，只链 Hub 与 `done_by_domain.md`；
- `_views/done_by_domain.md` 与 Hub 一致，按域维护；
- `docs/tasks/README.md` 归档流程更新：关账时「Hub 追加一行 + `_views/done.md` 不追加长列表」；
- Coding Wiki `task-schedule-ink-backend.md` + `index.md` + `CODING_WIKI.md` 同步链到 Hub，并写明 L1 task 文件仍是真值、L2 Wiki 只作导航；
- 50 书面复检落盘；文档-only PR 合 `main`。

---

## §2 范围（30 必须交付）

### A) `docs/tasks` 索引层

- [x] **A1** 新建 `docs/tasks/done/README.md`（Hub · 按域分组表）
  - 域：`harness` · `governance` · `chatbi` · `engineering` · `standards` · `epics`
  - 每域表：关账日 · 链接 · freeze_id / 一行摘要
  - Epic / MANIFEST / Loop 母单独立一节
  - 底部链 `[FRAGMENT_task_domain_infer_v1_zh.md](../../../cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md)`
- [x] **A2** 新建 `docs/tasks/_views/done_by_domain.md`
  - 与 Hub 语义一致，路径相对 `../done/<domain>/task_*.md`
  - Epic 母单单独一节
- [x] **A3** 重写 `docs/tasks/_views/done.md` 为薄指针
  - ≤15 行
  - 快速入口：Hub、`done_by_domain.md`、`in_progress.md`
  - 维护纪律：关账更新 Hub / `done_by_domain`；**勿**在本文件追加长列表
- [x] **A4** `docs/tasks/done/<domain>/` 目录结构声明（P0 不 mass `git mv`）
  - 在 Hub 中说明目标子目录 slug
  - 保留现有扁平文件不动，P1 子 task 再分批迁移
- [x] **A5** 索引表链到 **现有** `done/task_*.md`
  - 路径仍用扁平相对路径（如 `../done/task_governance_xxx_v1.md`），确保 P0 不破坏链接
- [x] **A6** `docs/tasks/README.md` 归档流程更新
  - 在「任务归档流程」中增：「更新 `done/README.md` Hub 对应域表一行」
  - 强化「禁止只把头部改成 done 而文件仍留在 active/」的硬规则
  - 新增「域子目录 + Hub 纪律」段落

### B) Coding Wiki 同步（与 task 同 PR）

- [x] **B1** `docs/coding_wiki/concepts/task-schedule-ink-backend.md`
  - 「Epic 分区」与「链接」节增 `docs/tasks/done/README.md` Hub 指针
  - 写明：L1 真值仍在 `RECENT` 与 `done/task_*.md`，L2 Wiki 只链不替代
- [x] **B2** `docs/coding_wiki/index.md`
  - 在「综合」或「维护」节说明：syntheses `source_task` 指向 L1 `done/` 扁平路径；Hub 只改善浏览，不改 frontmatter 真值
- [x] **B3** `docs/coding_wiki/CODING_WIKI.md`
  - §4.1 ingest / §4.2 query 中增「关账更新 Hub 一行」指针
  - 链 `[FRAGMENT_task_domain_infer_v1_zh.md](../../../cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md)`
- [x] **B4** 已有 syntheses 的 `source_task` 路径 **保持有效**
  - P0 仍扁平路径则不改 frontmatter 路径
  - 若 Hub 路径与旧路径冲突，以旧路径为准，Hub 中注明「待 P1 物理迁移后更新」

### C) 40：链接自检结论回填 task

- [ ] **C1** 运行相对链接自检（可用手工 `rg` / `markdown-link-check` / Python 脚本）
- [ ] **C2** 在 task §8「自检结论」填：命令、pass/fail、BROKEN 链接清单

### D) 50：独立复检落盘

- [x] **D1** `docs/tasks/reinspect_results/reinspect_governance_tasks_done_index_hygiene_20260613_v1.md`
- [x] **D2** 结论：pass / 无阻塞；列出抽检的链接与域表一致性

### E) PR

- [ ] **E1** 开 PR 合 `main`，body 含验收勾选 + 50 路径
- [ ] **E2** CI 绿；文档-only 无 pytest 回归，写明 skip 理由
- [ ] **E3** `Fixes` 无（或链治理 Epic 若有）

---

## §2.1 非范围

- 不批量 `git mv` 138 篇 done task（P1 子 task，本单不阻塞关账）。
- 不写 `api/`**、不改业务 SPEC 行为。
- 不为每篇 done task 新建或重写 synthesis。
- 不迁移 `docs/spec/` 规格文件。
- 不改 `docs/harness/prompts/` 帽子本体，只链现有 PROMPT。

---

## §3 失败路径

> 本 task 为纯文档索引治理，失败路径聚焦「索引断链 / 流程漂移 / 关账过早」。


| #   | Scenario ID                | 触发条件                                                      | 系统行为          | 可重试 | 用户/Agent 可见   | 测试 / 检查                          |
| --- | -------------------------- | --------------------------------------------------------- | ------------- | --- | ------------- | -------------------------------- |
| F1  | `fp-done-hub-broken-link`  | Hub / `_views/done_by_domain.md` 中链到不存在的 `done/task_*.md` | 文档浏览 404      | 否   | 链接失效          | 40 链接自检必须 zero BROKEN            |
| F2  | `fp-wiki-drift-from-l1`    | Coding Wiki 写成「done 域化已完成」，但 `done/` 仍扁平                  | Agent 误判真值    | 否   | 双轨信息          | 50 抽检 Wiki 与 task 正文一致性          |
| F3  | `fp-reinspect-missing`     | 50 未落盘即关账或合并 PR                                           | 关账证据缺失        | 否   | Harness 硬规则违反 | 验收标准强制 D1/D2                     |
| F4  | `fp-views-done-rebloated`  | `_views/done.md` 被改回长列表                                   | 薄指针失效         | 否   | 索引回退          | 40 检查 `_views/done.md` 行数 ≤15    |
| F5  | `fp-agent-reads-old-views` | Agent 只读旧 `_views/done.md` 长列表而忽略 Hub                     | 上下文浪费 / 遗漏域分组 | 是   | 无直接错误         | 在 `README.md` 与 Wiki 读序中显式指向 Hub |


> **思考未闭合**：§5 仍有 `（待填）` 且无合法 **思考轮控制** → 22 **退回 10** · 30 **拒开工**。

---

## §4 给 10-task / 执行链的交接物

1. **invoke 目录**：`docs/harness/invokes/by-task/governance-tasks-done-hygiene/`
  - `README.md`：索引 · 链最终目的与帽序 22→30→40→50→PR
  - `PROMPT_kimi_agent_rethink_R1_R5.md`：10-task 用，含 R0–R5 思考轮框架
  - `PROMPT_30_execute_docs_v1_zh.md`：30 专用，列 A+B 文件清单，禁止写 `api/`**
2. **必读**：
  - `docs/tasks/README.md`
  - `docs/tasks/_views/done.md`
  - `docs/coding_wiki/CODING_WIKI.md`
  - `docs/coding_wiki/concepts/task-schedule-ink-backend.md`
  - `[FRAGMENT_task_domain_infer_v1_zh.md](../../../cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md)`
3. **gate-check**：执行 30 前须确认 `HG-TASK-DRAFT` 与 `HG-AUDIT-R1` 均为 `approved`；若未签，拒执行并输出阻塞闸 ID。

---

## §5 思考轮次（高复杂度 / orchestration 含 rethink 时 · 10 帽预置）

> **何时启用**：`audit_profile: full`、跨索引治理、Agent rethink 链。  
> **真值**：`[docs/harness/prompts/hats/10-requirements.md](../harness/prompts/hats/10-requirements.md)` §思考轮 · `[22-task-audit.md](../harness/prompts/hats/22-task-audit.md)`。

### 思考轮控制（Agent 填 · 22 审）


| 字段                    | 值                         |
| --------------------- | ------------------------- |
| **actual_last_round** | `R5` / `R3` / …           |
| **early_stop**        | `no` / `yes`              |
| **early_stop_reason** | （`early_stop=yes` **必填**） |
| **residual_risks**    | `none` 或逐条（**必填**）        |


### R0 · 读 task / SPEC / 非范围

**回填区：** `（待填）`

### R1 · 代码事实

**回填区：** `（待填）`

### R2 · 方案对比

**回填区：** `（待填）`

### R3 · 边界 / 测试 / failure_paths

**回填区：** `（待填）`

### R4 · 链接自检 / PR 策略

**回填区：** `（待填）`

### R5 · 图谱/契约增量 + 关账判断

**回填区：** `（待填）`

---

## §6 依赖与引用


| 依赖项                 | 路径/说明                                                                    |
| ------------------- | ------------------------------------------------------------------------ |
| **编码规范 L2**         | `docs/standards/CODING_BACKEND_L2_v1_zh.md`                              |
| **PROJECT_CONFIG**  | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`                    |
| **Task 落盘规则**       | `docs/tasks/README.md`                                                   |
| **排期真值**            | `docs/tasks/RECENT_TASK_SCHEDULE.md` §6.1 / §6.6                         |
| **Wiki Schema**     | `docs/coding_wiki/CODING_WIKI.md`                                        |
| **Wiki 排期 hub**     | `docs/coding_wiki/concepts/task-schedule-ink-backend.md`                 |
| **域推断 FRAGMENT**    | `cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md`   |
| **工作区 done Hub 样例** | `Projects/docs/harness/tasks/done/README.md`                             |
| **链式常模**            | `docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md` |
| **关闭回溯**            | `docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md`                    |


---

## §7 给执行帽的必读列表

- `AGENTS.md`
- `docs/tasks/README.md`
- `docs/tasks/_views/done.md`
- `docs/coding_wiki/CODING_WIKI.md`
- `docs/coding_wiki/concepts/task-schedule-ink-backend.md`
- `docs/coding_wiki/index.md`
- `docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md`
- `cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md`

---

## §8 自检结论（执行者 · 40 帽回填）


| 项   | 结果                                                                                                                                  |
| --- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 命令  | `python3 /tmp/check_links2.py`（扫描 7 个文件：`docs/tasks/done/README.md`、`_views/done_by_domain.md`、`_views/done.md`、`docs/tasks/README.md`、`docs/coding_wiki/concepts/task-schedule-ink-backend.md`、`docs/coding_wiki/index.md`、`docs/coding_wiki/CODING_WIKI.md`） |
| 结论  | `pass`                                                                                                                              |
| 要点  | 356 个仓内相对链接 zero BROKEN；3 个跨仓链接指向 `cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md`（工作区中存在，本仓独立检查时不计入 broken）；`_views/done.md` 行数 10 ≤15。 |


---

## §9 实现备忘（由子 Agent 回填）


| 项        | 内容                                                                                                                                                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 涉及文件     | `docs/tasks/done/README.md` · `docs/tasks/_views/done_by_domain.md` · `docs/tasks/_views/done.md` · `docs/tasks/README.md` · `docs/coding_wiki/concepts/task-schedule-ink-backend.md` · `docs/coding_wiki/index.md` · `docs/coding_wiki/CODING_WIKI.md` |
| 关键 env   | 无                                                                                                                                                                                                                                                       |
| SQL 执行顺序 | 无                                                                                                                                                                                                                                                       |
| 接口变更     | 无                                                                                                                                                                                                                                                       |
| 图谱变更点    | 无                                                                                                                                                                                                                                                       |


---

## §10 验收标准

- [x] `done/README.md` 可按域浏览，覆盖 `harness / governance / chatbi / engineering / standards / epics` 主域
- [x] `_views/done.md` ≤15 行，且指向 Hub
- [x] `_views/done_by_domain.md` 与 Hub 一致
- [x] 索引相对链接自检 zero BROKEN
- [x] `docs/tasks/README.md` 归档流程已更新（域子目录 + Hub 纪律）
- [x] Coding Wiki：`task-schedule-ink-backend` + `index.md` + `CODING_WIKI.md` 已链 Hub，读序写明 L1 vs L2
- [x] 50 reinspect 落盘，结论 pass/无阻塞
- [ ] PR 已开，CI 绿（文档-only，pytest 无回归，body 写明 skip 理由）

**测试 / TDD（与 `test_strategy` 对齐）**：


| test_strategy    | 自检须含                               |
| ---------------- | ---------------------------------- |
| `not_applicable` | `test_strategy_note` 一行理由 + 链接自检命令 |


**合并前必绿（本仓）**：文档-only PR 无 `api/` 变更，pytest 不强制重跑；但仍须 `ruff check` / `markdown` 质量检查通过（若 CI 配置）。

---

## §11 执行路线与 Commit 回溯（关闭轮回填）

> 见 `[HANDOFF_CLOSE_TRACE.md](../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md)` §2。  
> 本 task 关账时由 22/40/50 回填：阶段表、分仓 commit、关联工件路径。

---

## 给 Cursor

`governance-tasks-done-hygiene`、`done/README.md`、`_views/done.md`、`done_by_domain.md`、`FRAGMENT_task_domain_infer_v1_zh.md`、`test_strategy: not_applicable`、`failure_paths`、`human_gate`、`audit_profile: full`、`git_branch`、`RECENT §6.1`、`Hub`、`薄指针`、`域子目录`