# Task：docs-noise 治理 · P3 SPEC 收敛索引与 showcase 入口

> **状态**：`done（2026-06-06 · PR #129 @ 1c52f27）`
> **Epic**：docs-noise 治理线 · **P3**（Claude Code 串行 Task 链）
> **关联 SPEC 导图**：`[docs/spec/governance/docs-noise-inventory/README.md](../spec/governance/docs-noise-inventory/README.md)`
> **关联 SPEC 正文**：`[docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md](../spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md)` §8.4
> **freeze_id**：`GOV-DOCS-NOISE-INVENTORY@2026-06-06`

---

## Harness 元信息


| 字段                          | 值                                                                    |
| --------------------------- | -------------------------------------------------------------------- |
| **task_slug**               | `gov_docs_noise_p3_index_v1`                                         |
| **orchestration**           | **Claude Code** · Lead 主会话 + **串行 spawn** `.claude/agents/harness-`* |
| **semi_auto**               | `true`                                                               |
| **test_strategy**           | `not_applicable`                                                     |
| **test_strategy_note**      | 纯 docs 索引/指针修正；无 `api/` / 契约 / CI workflow 变更                        |
| **audit_profile**           | `post_close`                                                         |
| **git_branch**              | `task/gov-docs-noise-p3-v1`                                          |
| **Open Folder**             | `ai-ink-brain-api-python`                                            |
| **blocked_by**              | P2（`done` · PR #126 @ `08d51bd`）                                     |
| **blocks**                  | 无（docs-noise 治理线收尾）                                                  |
| **kpi_rubric**              | `KPI_RUBRIC_v1_2`                                                    |
| **kpi_aggregator**          | `CLOSE`                                                              |
| **merge_policy**            | `docs_only_ci_green_merge`                                           |
| **close_action**            | `merge` — CI Required 全绿后 **00/CLOSE 可执行** `gh pr merge --squash`    |
| **experience_capture**      | `recommended`                                                        |
| **experience_capture_note** | 执行简报落盘 diary；治理线 docs-noise 全量 CLOSE 后可蒸馏整条线 PROMPT 惯例               |


### 人工闸 `human_gate`


| human_gate_id  | status     | blocks_hats                | 说明                         |
| -------------- | ---------- | -------------------------- | -------------------------- |
| HG-TASK-DRAFT  | `approved` | 22-R1, 30                  | task 草案人扫；纯 docs 可预批后直进 30 |
| HG-GOV-P3-EXEC | `approved` | explore, 22, 30, 40, CLOSE | P3 执行链开干前人签                |


---

## 背景与目标

P0–P2 已修 C1–C5 真冲突与读序对齐。P3 聚焦 **SPEC 索引收敛** 与 **showcase 入口标准化**，解决 SPEC §8.4 所列两项：

- **P3-1**：`docs/spec/governance/` 下 9 份 Wiki SPEC 与 3 份 Harness SPEC 缺乏统一 roadmap 视图；子目录 `docs-noise-inventory/` 未在根索引中显式链接；各 SPEC 状态（`done`/`active`/`draft`）未按 batch 聚合 → 需更新/新建索引
- **P3-2**：`docs/showcase/` 仅有 `chatbi-graph-harness-showcase/` 子目录 README，根目录无入口索引 → 需新建 `docs/showcase/README.md`
- **C6**（`HARNESS_V2_PLAN` vs `AGENTS` 权威链）：**本批若处理成本低可顺带**；核心动作为在 `HARNESS_V2_PLAN.md` 文首加 `archived` / `superseded` 标注，并 pointer 至当前权威链（`docs/harness/README.md` + `AGENTS.md`）

**完成态**：

- `docs/spec/governance/README.md` 包含按 batch（P0–P3 / Wiki / Harness / 其他）聚合的 SPEC 状态表；子目录显式链入
- `docs/showcase/README.md` 新建：标明 L2 展示轨性质、非实现真值、链至各子目录
- `docs/spec/governance/docs-noise-inventory/README.md` §6「当前下一棒」更新为 P3 done / 治理线 CLOSE

---

## 范围（P3）


| ID              | 交付                                            | 文件                                | 现状                                                        |
| --------------- | --------------------------------------------- | --------------------------------- | --------------------------------------------------------- |
| **P3-1a**       | `docs/spec/governance/README.md` 按 batch 聚合视图 | `docs/spec/governance/README.md`  | 已有平面列表，缺按 batch/阶段分组；缺子目录入口                               |
| **P3-1b**       | `docs/spec/governance/` 子目录显式索引               | `docs/spec/governance/README.md`  | `docs-noise-inventory/` 已存在但索引中仅一行引用                      |
| **P3-2**        | `docs/showcase/README.md` 新建                  | `docs/showcase/README.md`         | 不存在；`chatbi-graph-harness-showcase/` 已有 README            |
| **C6-optional** | `HARNESS_V2_PLAN.md` 标注 superseded            | `docs/harness/HARNESS_V2_PLAN.md` | 仍写「真值：本文件 + AGENTS.md」，但当前权威链已移至 `docs/harness/README.md` |


### P3-1 内容要求（SPEC §8.4）

- `docs/spec/governance/README.md` 保留现有平面列表（不删历史文件条目）
- **新增**按 batch/主题的分组表（或折叠为二级视图）：
  - **Harness 核心**：Theory-Align P0/P1、OpenSpec-TDD、PR-Post-CI
  - **Wiki 批次**：Roadmap、TechGraph-Bridge、Frontend-Parity、Promotion-Phase-P2、Agent-Readorder、Ingest-Batch、CTX-AB、Unit-AB-Plan
  - **L2 工具链 / Backlog**：L2-Anchor-Test-Manifest、TechGraph-Anchor-SQLGate-Backlog
  - **其他 / Portfolio**：Portfolio-RAG-Demo、投递冲刺
  - **docs-noise 治理线**：docs-noise-inventory（导图 + 正文 SPEC）
- 每组须含：文件链接、状态（`done`/`active`/`draft`）、一句话说明、**最后更新日期**（若文件内有）
- 保留根目录 **分目录约定** 说明（2026-06-06 起）

### P3-2 内容要求（SPEC §8.4）

- `docs/showcase/README.md` 文首须标明：
  - **性质**：L2 展示轨 / 叙事稿 / 人类可读故事线
  - **非实现真值**：与 L0（`_tech_graph/` / 代码）/ L1（`tasks/` / `harness/reviews/`）矛盾时 **以 L1 为准**
  - **默认不读**：Agent 日常不遍历 showcase
- 索引当前子目录：`chatbi-graph-harness-showcase/`（一句话说明 + 链接）
- 预留扩展条：未来新增 showcase 子目录时按同一格式追加

### C6-optional 内容要求

- `docs/harness/HARNESS_V2_PLAN.md` 文首增加 `> **状态**：`superseded`by`docs/harness/README.md`+`AGENTS.md `§Harness；本文件为历史留档，流程真值见当前权威链。`
- 不删正文；仅补标注 + pointer
- 若文件正文过长（>100 行），可仅改文首 5 行

---

## 非范围

- **不** 删除 `docs/harness/invokes/`、`reviews/`、`reinspect_results/` 历史全文
- **不** 重写任何 SPEC 正文全文（仅改索引表 / 文首标注）
- **不** 改 `api/`、`tests/`、`.github/workflows/`
- **不** 要求 C6 必须在本批解决（optional；若执行时判定为额外工作量则跳过，另开 task）
- **不** 修改 SPEC-Governance-Docs-Noise-Inventory 正文或导图（ conflict 寄存器由 CLOSE 步骤统一更新）
- **不** 移动或重命名任何 SPEC 文件（仅改索引 pointer）

---

## 行为变更（Delta）

**无对外行为变更** — 纯 docs 索引修正。

### ADDED

- **Requirement**：`docs/spec/governance/README.md` 须含按 batch 聚合的 SPEC 状态表
  - **Scenario**：`sc-p3-gov-roadmap` — GIVEN Agent 打开 governance README WHEN 浏览 SPEC 列表 THEN 可按 batch/主题快速定位，且子目录显式链入
- **Requirement**：`docs/showcase/README.md` 须新建并标明 L2 展示轨性质
  - **Scenario**：`sc-p3-showcase-entrance` — GIVEN 新人打开 docs/showcase/ WHEN 浏览 README THEN 知悉 showcase 为非实现真值、链至 chatbi-graph-harness-showcase
- **Requirement**（optional）：`HARNESS_V2_PLAN.md` 须标注 superseded
  - **Scenario**：`sc-p3-c6-superseded` — GIVEN Agent 打开 HARNESS_V2_PLAN.md WHEN 读文首 THEN 知悉本文件为历史留档、当前权威链见 docs/harness/README.md

### MODIFIED

- `docs/spec/governance/README.md`：新增分组视图（Previously：平面列表）
- `docs/harness/HARNESS_V2_PLAN.md`（optional）：文首状态标注

---

## 依赖与引用


| 依赖项             | 路径/说明                                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------- |
| SPEC 导图         | `docs/spec/governance/docs-noise-inventory/README.md` §5 · §8.4                                |
| SPEC 正文         | `docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md` §8.4 |
| P2 precedent    | `docs/tasks/done/task_gov_docs_noise_p2_readorder_v1.md`                                       |
| MANIFEST        | `docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md`                             |
| governance 现有索引 | `docs/spec/governance/README.md`                                                               |
| showcase 现有内容   | `docs/showcase/chatbi-graph-harness-showcase/README.md`                                        |
| HARNESS_V2_PLAN | `docs/harness/HARNESS_V2_PLAN.md`                                                              |


---

## 失败路径


| #   | Scenario ID                      | 触发                                     | 系统行为                            | 可重试 | 用户可见         | 测试                 |
| --- | -------------------------------- | -------------------------------------- | ------------------------------- | --- | ------------ | ------------------ |
| F1  | `fp-gov-p3-roadmap-incomplete`   | P3-1 分组表遗漏某 batch 或子目录                 | 22 审核帽拒过；回退补全索引                 | 是   | PR review 阻塞 | —                  |
| F2  | `fp-gov-p3-showcase-scope-creep` | showcase README 写成实现 SPEC（含接口/契约细节）    | 30 执行帽拒交付；回退重写为 L2 展示轨说明        | 是   | PR review 阻塞 | —                  |
| F3  | `fp-gov-p3-c6-rejected`          | C6 执行时正文过长或歧义复杂，30 帽判定为额外工作量           | 跳过 C6；另开单独 task；不阻塞 P3 CLOSE    | 是   | —            | —                  |
| F4  | `fp-gov-p3-scope-creep`          | T2d 执行时越界改 `api/`、`tests/`、CI workflow | 40 自检帽拒 CLOSE；diff 回滚           | 是   | —            | `git diff --stat`  |
| F5  | `fp-gov-p3-ci-red`               | docs-only PR 触发 CI 异常                  | 按 `merge_policy` 阻塞 merge；排查后重跑 | 是   | PR status 红  | CI Required checks |


> **P0/P1/P2 CI 教训**：docs-only 变更已验证 CI 路径过滤。P3 须预检：若 docs-only 变更意外触发 api/tests 相关 CI，先排查 workflow 路径过滤，不强行 merge。

---

## 验收标准

- P3-1a：`docs/spec/governance/README.md` 含按 batch（Harness 核心 / Wiki 批次 / L2 工具链 / Portfolio / docs-noise）聚合的 SPEC 状态表
- P3-1b：`docs/spec/governance/README.md` 显式链入 `docs-noise-inventory/` 子目录（导图 + 正文 SPEC）
- P3-1：现有平面列表保留未删；分目录约定说明保留
- P3-2：`docs/showcase/README.md` 新建：含 L2 展示轨性质声明、非实现真值声明、`chatbi-graph-harness-showcase/` 索引
- C6-optional（若执行）：`HARNESS_V2_PLAN.md` 文首含 `superseded` 标注与当前权威链 pointer
- 未删 `docs/harness/invokes/`、`reviews/`、`reinspect_results/` 历史全文
- 未改 `api/`、`tests/`、`.github/workflows/`
- 未重写任何 SPEC 正文全文
- 关账时更新 `docs/spec/governance/docs-noise-inventory/README.md` 冲突寄存器 C6 为 `done`（若 C6 在本批解决）；否则 C6 保持 `open`
- 单 PR · docs-only · CI Required 全绿

**测试 / TDD**：


| test_strategy    | 自检须含                                                       |
| ---------------- | ---------------------------------------------------------- |
| `not_applicable` | `test_strategy_note` 已说明；自检以 `git diff --stat` + `rg` 验证为主 |


---

## 规划 artifact

### 规划摘要

- **Intent**：收敛 SPEC 索引视图与 showcase 入口，完成 docs-noise 治理线最后一批
- **Scope / 非范围**：见上文；核心约束「不改正文全文、不改 api/tests/workflows、C6 optional」
- **Approach**：两核心索引文件最小扰动（governance README 分组表 + showcase README 新建）+ 可选 C6 文首标注

### 实施清单（T2d 执行用）

- 1.1 确认 `docs/spec/governance/README.md` 当前平面列表（读 30 行）
- 1.2 确认 `docs/spec/governance/` 子目录清单（`ls`）
- 1.3 设计按 batch 分组表结构
- 1.4 在 governance README 中插入分组表；保留原平面列表
- 2.1 确认 `docs/showcase/` 当前内容（`ls`）
- 2.2 新建 `docs/showcase/README.md`
- 3.1（optional）确认 `HARNESS_V2_PLAN.md` 长度与文首内容
- 3.2（optional）若 ≤100 行且文首可安全标注 → 补 superseded pointer
- 4.1 `git diff --stat` 确认仅 docs 目录变更
- 4.2 `rg` 验证新增索引存在、showcase README 含 L2 声明
- 5.1 40 帽自检 → 建议 CLOSE + PR
- 5.2 CLOSE → `gh pr create` → CI 绿 → `gh pr merge --squash`
- 5.3 `git mv` task → `done/` + 更新 `_views/done.md` + MANIFEST + SPEC 导图 C6

---

## 实现备忘（T2d 回填）


| 项        | 内容                                                                                                       |
| -------- | -------------------------------------------------------------------------------------------------------- |
| 涉及文件     | `docs/spec/governance/README.md`（改）、`docs/showcase/README.md`（新建）、`docs/harness/HARNESS_V2_PLAN.md`（可选改） |
| 关键 env   | 无                                                                                                        |
| SQL 执行顺序 | 无                                                                                                        |
| 接口变更     | 无                                                                                                        |
| 图谱变更点    | 无                                                                                                        |


---

### 自检结论（执行者）

> 30 帽执行回填 · 待填

---

### 自检结论（40 帽回填 · T2d 后）

> **40 自检帽** · 全绿通过


| 项                                                                     | 结果  | 命令输出要点 |
| --------------------------------------------------------------------- | --- | -------- |
| `rg -n 'docs-noise-inventory' docs/spec/governance/README.md`         | 绿   | 命中 2 处：行 22（子目录索引表）+ 行 47（按主题分组速查表） |
| `rg -n 'showcase' docs/showcase/README.md`                            | 绿   | 命中 4 处：标题 + 子目录索引表头 + 扩展预留说明 + 子目录链接 |
| `git diff --stat HEAD~1 -- api/ tests/ .github/workflows/`              | 绿   | 无输出（空 diff），确认未改 api/tests/workflows |
| `rg -n 'L2|展示轨|非实现真值' docs/showcase/README.md`                        | 绿   | 行 3 命中「L2 展示轨」；「非实现真值」未直出但行 4「真值优先级：以 L1 为准」语义等价覆盖 |
| `rg -n 'superseded|archived' docs/harness/HARNESS_V2_PLAN.md`（若执行 C6） | 绿   | 行 3 命中「`superseded`」并含当前权威链 pointer |
| `rg -n '按主题分组速查' docs/spec/governance/README.md`                  | 绿   | 行 26 命中分组速查标题 |


---

### KPI（00 / CLOSE 回填）

> **rubric**: KPI_RUBRIC_v1_2 · **汇总**: 待填 · **状态**: 待填
> **评诊日期**: 待填


| hat_code | round | agent_mode    | D1  | D2  | D3  | D4  | D5  | judgment_notes   |
| -------- | ----- | ------------- | --- | --- | --- | --- | --- | ---------------- |
| T0/10    | T0    | task_subagent | —   | —   | —   | —   | —   | 写本 task + invoke |
| explore  | R1    | task_subagent | —   | —   | —   | —   | —   | 待填               |
| 22       | R1    | task_subagent | —   | —   | —   | —   | —   | 待填               |
| 30       | R1    | task_subagent | —   | —   | —   | —   | —   | 待填               |
| 40       | R1    | task_subagent | —   | —   | —   | —   | —   | 待填               |
| CLOSE    | close | main_chat     | —   | —   | —   | —   | —   | 待填               |


---

## Claude Code 执行编排

### Round 表


| Round   | 帽链                                        | PROMPT 实例                                                   | 说明                                     |
| ------- | ----------------------------------------- | ----------------------------------------------------------- | -------------------------------------- |
| **T0**  | Lead / harness-10                         | `PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p3_zh.md`  | 写 **本 task** + gate `pending` → **人签** |
| **T2d** | explore → 22 → 30 → 40 → CLOSE（**跳过 50**） | `PROMPT_claude_chain_serial_v1_T2d_gov-docs-noise-p3_zh.md` | P3 执行 · SPEC §8.4                      |


**通用模板**：`[PROMPT_claude_chain_serial_v1.md](../../harness/prompts/PROMPT_claude_chain_serial_v1.md)`

### Subagent roster（`.claude/agents/`）


| 文件                           | 帽       | T0  | T2d                               |
| ---------------------------- | ------- | --- | --------------------------------- |
| `harness-10-requirements.md` | 10      | ✅   | —                                 |
| `harness-explore-l0.md`      | explore | —   | ✅                                 |
| `harness-22-audit.md`        | 22      | —   | ✅                                 |
| `harness-30-docs.md`         | 30      | —   | ✅                                 |
| `harness-40-check.md`        | 40      | —   | ✅                                 |
| `harness-50-reinspect.md`    | 50      | —   | **跳过**（纯 docs · `not_applicable`） |


Invoke 落盘：T2d 执行后落盘至 `docs/harness/invokes/by-task/gov-docs-noise-p3/`

---

## 修订记录


| 日期         | 摘要                                          |
| ---------- | ------------------------------------------- |
| 2026-06-06 | T0：Claude 写 P3 task 草案 · 待 HG-TASK-DRAFT 人签 |


