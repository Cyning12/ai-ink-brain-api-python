# Task：docs-noise 治理 · P1 标 archived / superseded

> **状态**：`draft`（T0 产出 · 待人签 HG-TASK-DRAFT）  
> **Epic**：docs-noise 治理线 · **P1**（Claude Code 串行 Task 链）  
> **关联 SPEC 导图**：`[docs/spec/governance/docs-noise-inventory/README.md](../spec/governance/docs-noise-inventory/README.md)`  
> **关联 SPEC 正文**：`[docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md](../spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md)` §8.2  
> **freeze_id**：`GOV-DOCS-NOISE-INVENTORY@2026-06-06`

---

## Harness 元信息


| 字段                          | 值                                                                    |
| --------------------------- | -------------------------------------------------------------------- |
| **task_slug**               | `gov_docs_noise_p1_archived_v1`                                      |
| **orchestration**           | **Claude Code** · Lead 主会话 + **串行 spawn** `.claude/agents/harness-*` |
| **semi_auto**               | `true`                                                               |
| **test_strategy**           | `not_applicable`                                                     |
| **test_strategy_note**      | 纯 docs 指针修正；无 `api/` / 契约 / CI workflow 变更                           |
| **audit_profile**           | `post_close`                                                         |
| **git_branch**              | `task/gov-docs-noise-p1-v1`                                          |
| **Open Folder**             | `ai-ink-brain-api-python`                                            |
| **blocked_by**              | P0（`done` · PR #121 @ `5184c10`）                                     |
| **blocks**                  | P2 子批（未建）                                                            |
| **kpi_rubric**              | `KPI_RUBRIC_v1_2`                                                    |
| **kpi_aggregator**          | `CLOSE`                                                              |
| **merge_policy**            | `docs_only_ci_green_merge`                                           |
| **close_action**            | `merge` — CI Required 全绿后 **00/CLOSE 可执行** `gh pr merge --squash`    |
| **experience_capture**      | `recommended`                                                        |
| **experience_capture_note** | 执行简报落盘 diary；关账后可蒸馏 Claude Task 链 PROMPT 惯例                          |


### 人工闸 `human_gate`


| human_gate_id  | status   | blocks_hats                | 说明                         |
| -------------- | -------- | -------------------------- | -------------------------- |
| HG-TASK-DRAFT  | approved | 22-R1, 30                  | task 草案人扫；纯 docs 可预批后直进 30 |
| HG-GOV-P1-EXEC | approved | explore, 22, 30, 40, CLOSE | P1 执行链开干前人签                |


---

## 背景与目标

docs-noise SPEC §5 将 `docs/delivery/v0.2.0-code-rag/` 与 `docs/flows/` 列为 **历史遗留 / 低维护噪音**。P0 已修 C1–C3 真冲突；P1 在 **不删正文** 的前提下，为两处历史快照加 **archived / superseded** 横幅与 POINTER，避免 Agent/新人误将其当作 L0 真值。

**完成态**：

- `docs/delivery/v0.2.0-code-rag/README.md` 文首含 archived 横幅，链至 `docs/harness/README` + `docs/spec/`
- `docs/flows/README.md` 新建，写明 freeze 日期、Legacy chat 性质、superseded by `_tech_graph`

---

## 范围（P1）


| ID       | 交付                                                       | 文件                                        |
| -------- | -------------------------------------------------------- | ----------------------------------------- |
| **P1-1** | `docs/delivery/v0.2.0-code-rag/README.md` 文首 archived 横幅 | `docs/delivery/v0.2.0-code-rag/README.md` |
| **P1-2** | 新建 `docs/flows/README.md`                                | `docs/flows/README.md`（新建）                |


### P1-1 内容要求（SPEC §8.2）

- 文首加 `> **ARCHIVED`** 横幅（或同级醒目标记）
- 说明：本交付包已被 `docs/spec/` + `docs/harness/` supersede
- 链至 `docs/harness/README`（Harness 过程库入口）与 `docs/spec/`（当前 SDD 真值）
- **不** 删改正文其余段落（保留历史全文）

### P1-2 内容要求（SPEC §8.2）

- 写明 **freeze 日期**：`2026-04-16`（`docs/flows/rag-chat/v1_2026-04-16_*.md` 快照日期）
- 说明：本目录为 **Legacy chat** 流程快照，落后于 Unified/ChatBI
- 说明：端到端真值已迁移至 `docs/_tech_graph/`
- 链至 `docs/_tech_graph/00_main.md` 或 `docs/_tech_graph/README.md`
- 若目录内已存在其他 `.md`，本 README 仅作 **索引 / POINTER**，不替代子文件

---

## 非范围

- **不** 删除 `docs/delivery/v0.2.0-code-rag/` 内任何文件
- **不** 删除 `docs/flows/` 内现有快照文件
- **不** 删 invoke/review 审计链
- **不** 改 `api/`、`tests/`、`.github/workflows/`
- **不** 执行 P2/P3 治理（读序对齐 / SPEC 收敛）
- **不** 修改 SPEC 正文或导图 README 的冲突寄存器状态（P1 非真冲突，属标注类）

---

## 行为变更（Delta）

**无对外行为变更** — 纯 docs 指针标注。相对现网增量：

### ADDED

- **Requirement**：`docs/delivery/v0.2.0-code-rag/README.md` 须含 archived 横幅
  - **Scenario**：`sc-p1-delivery-archived` — GIVEN Agent 打开 delivery README WHEN 读取文首 THEN 看到 ARCHIVED 标记及 supersede 指针
- **Requirement**：`docs/flows/README.md` 须新建并含 freeze 日期与 superseded 说明
  - **Scenario**：`sc-p1-flows-readme` — GIVEN Agent 打开 flows 目录 WHEN 读取 README THEN 知悉本目录为 Legacy 快照且真值在 `_tech_graph`

---

## 依赖与引用


| 依赖项           | 路径/说明                                                                                          |
| ------------- | ---------------------------------------------------------------------------------------------- |
| SPEC 导图       | `docs/spec/governance/docs-noise-inventory/README.md` §5 · §8.2                                |
| SPEC 正文       | `docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md` §8.2 |
| P0 precedent  | `docs/tasks/done/task_gov_docs_noise_p0_readme_v1.md`                                          |
| MANIFEST      | `docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md`                             |
| T2b PROMPT    | `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md`               |
| delivery 目标文件 | `docs/delivery/v0.2.0-code-rag/README.md`（已存在）                                                 |
| flows 目标文件    | `docs/flows/README.md`（**须新建**）                                                                |


---

## 失败路径


| #   | Scenario ID                    | 触发                                                     | 系统行为                                                      | 可重试    | 用户可见         | 测试                 |
| --- | ------------------------------ | ------------------------------------------------------ | --------------------------------------------------------- | ------ | ------------ | ------------------ |
| F1  | `fp-gov-p1-delete-audit`       | 误删 `docs/delivery/` 或 `docs/flows/` 内历史正文              | **禁止**；仅改 README / 新建 POINTER                             | —      | —            | —                  |
| F2  | `fp-gov-p1-delivery-no-banner` | archived 横幅缺失或位置不在文首                                   | 30 执行帽拒交付；回退补横幅                                           | 是（人工补） | PR review 阻塞 | —                  |
| F3  | `fp-gov-p1-flows-mislink`      | `docs/flows/README.md` 链至错误目标（如仍指 `docs/flows/` 自身为真值） | 22 审核帽拒过；回退修正指针                                           | 是      | PR review 阻塞 | —                  |
| F4  | `fp-gov-p1-scope-creep`        | T2b 执行时越界改 `api/`、`tests/`、CI workflow                 | 40 自检帽拒 CLOSE；diff 回滚                                     | 是      | —            | `git diff --stat`  |
| F5  | `fp-gov-p1-ci-red`             | docs-only PR 触发 CI 异常（参考 P0 教训：test_validate 首轮红）      | 按 `merge_policy: docs_only_ci_green_merge` 阻塞 merge；排查后重跑 | 是      | PR status 红  | CI Required checks |


> **P0 CI 教训**：P0 执行中 `harness_task_validate` 首轮红（`05be476` 修复）。P1 须预检：若 docs-only 变更意外触发 api/tests 相关 CI，先排查 workflow 路径过滤，不强行 merge。

---

## 验收标准

- P1-1：`docs/delivery/v0.2.0-code-rag/README.md` 文首含 **ARCHIVED** 横幅，链至 `docs/harness/README` + `docs/spec/`
- P1-1：delivery README 正文其余段落 **未被删除**
- P1-2：`docs/flows/README.md` **已新建**，含 freeze 日期 `2026-04-16`、Legacy chat 说明、superseded by `_tech_graph` 指针
- P1-2：flows README 链至 `docs/_tech_graph/` 具体入口文件
- 未删 `docs/delivery/`、`docs/flows/` 内任何历史文件
- 未改 `api/`、`tests/`、`.github/workflows/`
- 单 PR · docs-only · CI Required 全绿

**测试 / TDD**：


| test_strategy    | 自检须含                                                       |
| ---------------- | ---------------------------------------------------------- |
| `not_applicable` | `test_strategy_note` 已说明；自检以 `git diff --stat` + `rg` 验证为主 |


**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见 `AGENTS.md`）。

---

## 规划 artifact

### 规划摘要

- **Intent**：为历史交付包与 Legacy 流程快照加 archived / superseded 标注，防止误读为当前真值
- **Scope / 非范围**：见上文；核心约束「不删历史正文、不改 api/tests/workflows」
- **Approach**：两文件最小扰动 — 一文首加横幅、一新建 POINTER README

### 实施清单（T2b 执行用）

- 1.1 确认 `docs/delivery/v0.2.0-code-rag/README.md` 当前内容（仅读文首 20 行）
- 1.2 在文首插入 archived 横幅 + supersede 指针（保留原正文）
- 2.1 确认 `docs/flows/` 目录现状（ls，不读子文件全文）
- 2.2 新建 `docs/flows/README.md` 含 freeze 日期、Legacy 说明、`_tech_graph` 链
- 3.1 `git diff --stat` 确认仅 docs 目录两文件变更
- 3.2 `rg` 验证 archived 横幅存在、links 有效
- 4.1 40 帽自检 → 建议 CLOSE + PR
- 4.2 CLOSE → `gh pr create` → CI 绿 → `gh pr merge --squash`
- 4.3 `git mv` task → `done/` + 更新 `_views/done.md`

---

## 实现备忘（T2b 回填）


| 项        | 内容                                                                      |
| -------- | ----------------------------------------------------------------------- |
| 涉及文件     | `docs/delivery/v0.2.0-code-rag/README.md`（改）、`docs/flows/README.md`（新建） |
| 关键 env   | 无                                                                       |
| SQL 执行顺序 | 无                                                                       |
| 接口变更     | 无                                                                       |
| 图谱变更点    | 无                                                                       |


---

### 自检结论（执行者）

**执行的文件变更清单**

| 文件 | 操作 | 说明 |
|------|------|------|
| `docs/delivery/v0.2.0-code-rag/README.md` | 修改（文首插入 ARCHIVED 横幅） | 已含 `> **ARCHIVED**` 横幅，链至 `docs/spec/` + `docs/harness/README`；保留原正文全部段落 |
| `docs/flows/README.md` | 新建 | 含标题、freeze 日期 `2026-04-16`、Legacy chat 说明、`_tech_graph` 指针、目录索引 |

**`git diff --stat` 输出（commit `a3225c9`）**

```
 docs/delivery/v0.2.0-code-rag/README.md | 110 ++++++++++++++++++++++++++++++++
 docs/flows/README.md                    |  21 ++++++
 2 files changed, 131 insertions(+)
```

**范围验证**

- `git diff --stat HEAD~1 -- api/ tests/ .github/workflows/`：无输出（确认未改 api/tests/workflows）
- 未删除 `docs/delivery/`、`docs/flows/` 内任何历史文件
- 未删 invoke/review 审计链

**结论**：P1-1 / P1-2 均已完成，范围合规，建议进入 40 自检帽。

---

## 自检结论（40 帽回填 · T2b 后）

> **40 自检帽** 运行 task 所列命令后，将 **原始输出要点** 与 pass/fail 结论写入本节。


| 项   | 结果                                                                                                              |
| --- | --------------------------------------------------------------------------------------------------------------- |
| 命令  | `git diff --stat` / `rg -n 'ARCHIVED' docs/delivery/v0.2.0-code-rag/README.md` / `test -f docs/flows/README.md` |
| 结论  | （待 T2b 回填）                                                                                                      |
| 要点  | （待 T2b 回填）                                                                                                      |


---

## KPI（00 / CLOSE 回填）

**rubric**: KPI_RUBRIC_v1_2 · **汇总**: （待 CLOSE 回填） · **状态**: （待 CLOSE 回填）  
**评诊日期**: （待 CLOSE 回填） · **简报**: （待 CLOSE 回填）


| hat_code | round | agent_mode    | D1  | D2  | D3  | D4  | D5  | judgment_notes |
| -------- | ----- | ------------- | --- | --- | --- | --- | --- | -------------- |
| explore  | R1    | task_subagent | （待） | （待） | （待） | （待） | —   | —              |
| 22       | R1    | task_subagent | （待） | （待） | （待） | （待） | —   | —              |
| 30       | R1    | task_subagent | （待） | （待） | （待） | （待） | —   | —              |
| 40       | R1    | task_subagent | （待） | （待） | （待） | （待） | —   | —              |
| CLOSE    | close | main_chat     | （待） | （待） | （待） | （待） | （待） | —              |


**完成度（人读摘要 · 待 CLOSE 回填）**


| 维度                | 得分  | 说明  |
| ----------------- | --- | --- |
| 业务交付（P1-1 / P1-2） | （待） | —   |
| Task 链执行          | （待） | —   |
| 预期对照              | （待） | —   |


---

## Claude Code 执行编排

### Round 表


| Round   | 帽链                                        | PROMPT 实例                                                                                                                                      | 说明                                     |
| ------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **T0**  | Lead / harness-10                         | `[PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md](../../harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md)`   | 写 **本 task** + gate `pending` → **人签** |
| **T2b** | explore → 22 → 30 → 40 → CLOSE（**跳过 50**） | `[PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md](../../harness/prompts/PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md)` | P1 执行 · SPEC §8.2                      |


### Subagent roster（`.claude/agents/`）


| 文件                           | 帽       | T0  | T2b                               |
| ---------------------------- | ------- | --- | --------------------------------- |
| `harness-10-requirements.md` | 10      | ✅   | —                                 |
| `harness-explore-l0.md`      | explore | —   | ✅                                 |
| `harness-22-audit.md`        | 22      | —   | ✅                                 |
| `harness-30-docs.md`         | 30      | —   | ✅                                 |
| `harness-40-check.md`        | 40      | —   | ✅                                 |
| `harness-50-reinspect.md`    | 50      | —   | **跳过**（纯 docs · `not_applicable`） |


### Invoke 落盘

T2b 执行后落盘至：`docs/harness/invokes/by-task/gov-docs-noise-p1/`

---

## 修订记录


| 日期         | 摘要                                          |
| ---------- | ------------------------------------------- |
| 2026-06-06 | T0：Claude 写 P1 task 草案 · 待 HG-TASK-DRAFT 人签 |


