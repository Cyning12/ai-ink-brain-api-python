# Task：巩固 Harness P1 文档（P1-3 → P1-2）

> **状态**：draft  
> **关联图谱**：`docs/_tech_graph/99_spec.md`（工程规约）  
> **关联 Issue/PR**：待补（本任务目标为一个 task + 一个 PR）  
> **前端依赖**：无

> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/*.md` 索引。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) **§5**；半自动 / 人工闸：[`docs/harness/prompts/HANDOFF_SEMI_AUTO.md`](../../harness/prompts/HANDOFF_SEMI_AUTO.md)。

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
| HG-TASK-DRAFT | pending | 22-R1,30 | task 初稿由人扫后改 `approved`；在此之前仅允许停留在 10 帽。 |
| HG-REINSPECT | pending | done | （可选）50 复检后由人签收再归档 done / 合并。 |

---

## 背景与目标

对齐 `RECENT_TASK_SCHEDULE` §0.4 的 Harness P1 巩固计划，在本后端仓以 **一个任务单 + 一个 PR** 完成两项文档治理：先补 `human_gate` 场景速查（P1-3），再落 `docs/tasks/skills/README.md` 的 6 类 SKILL 说明（P1-2），并形成可审可执行的闭环输入给 22/30 帽。

---

## 范围

- [ ] **P1-3（先做）**：更新 `docs/tasks/README.md`，新增 `human_gate` 场景速查表，字段至少包含：`gate_id`、`status`、`blocks_hats`、`典型场景`、`谁可改 approved`。  
- [ ] **P1-2（后做）**：新增目录 `docs/tasks/skills/` 与 `docs/tasks/skills/README.md`，定义 6 类 SKILL（含关账蒸馏与人审口径）。  
- [ ] 在 `docs/tasks/README.md` 补充到 `docs/tasks/skills/README.md` 的可发现入口（索引链路）。  
- [ ] 所有新增或改动文档采用 UTF-8、相对路径引用，不写绝对本机路径。  

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
| 半自动与状态栏 | [`docs/harness/prompts/HANDOFF_SEMI_AUTO.md`](../../harness/prompts/HANDOFF_SEMI_AUTO.md) |
| 10 帽规则 | [`docs/harness/prompts/10-requirements.md`](../../harness/prompts/10-requirements.md) |
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

- [ ] `docs/tasks/README.md` 新增 `human_gate` 场景速查，含 5 列：`gate_id`、`status`、`blocks_hats`、`典型场景`、`谁改 approved`。  
- [ ] 新增 `docs/tasks/skills/README.md`，明确 6 类 SKILL、适用阶段、输入输出与关账蒸馏/人审口径。  
- [ ] `docs/tasks/README.md` 出现到 `docs/tasks/skills/README.md` 的入口链接。  
- [ ] task 内保留「矛盾单列」要求：若 §九 与 HARNESS_V2 §5 不一致，必须单独小节列出而非混写。  
- [ ] 非范围项未被触及（无 `api/`、CI workflow、前端仓改动）。  

**测试 / TDD（与 `test_strategy` 对齐）**：

| test_strategy | 自检须含 |
|---------------|----------|
| `not_applicable` | 在 `### 自检结论（执行者）` 明确「纯 docs 变更」理由，并给出目录与文件检查结果。 |

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（项目通用要求；本任务可标记为“未触发代码路径”并说明）。

---

## 矛盾单列（执行期必填）

> 若在编写 `docs/tasks/skills/README.md` 时发现 `docs/diary/...§九` 与 `HARNESS_V2_PLAN.md §5` 对 6 类 SKILL 定义冲突，必须新增本小节并按以下格式逐条记录：

| 矛盾项 | 来源 A | 来源 B | 当前处理 |
|--------|--------|--------|----------|
| （待填） | diary §九 | HARNESS_V2 §5 | 保留冲突并提交 22 帽裁决 |

---

## 给执行帽的必读列表

1. `docs/tasks/active/task_harness_p1_docs_consolidation_v1.md`（本文件全文）  
2. `docs/tasks/RECENT_TASK_SCHEDULE.md`（§0.4）  
3. `docs/tasks/README.md`（将被修改）  
4. `docs/harness/HARNESS_V2_PLAN.md`（§5 字段口径）  
5. `docs/harness/prompts/HANDOFF_SEMI_AUTO.md`（人工闸与状态栏）  
6. `docs/diary/2026-05-22-harness-evaluation-improvement-response.md`（§九，类型清单来源）  

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/tasks/README.md`、`docs/tasks/skills/README.md` |
| 关键 env | 无 |
| SQL 执行顺序 | 无 |
| 接口变更 | 无 |
| 图谱变更点 | 无 |

---

## 自检结论（执行者 · 40 帽回填）

> **40 自检帽** 运行 task 所列命令后，将 **原始输出要点** 与 pass/fail 结论写入本节。

| 项 | 结果 |
|----|------|
| 命令 | 待回填 |
| 结论 | 待回填 |
| 要点 | 待回填 |

---

## 给 Cursor

`task_harness_p1_docs_consolidation_v1`、`Harness P1`、`P1-3`、`P1-2`、`human_gate`、`skills`、`test_strategy`、`audit_profile`、`semi_auto`
