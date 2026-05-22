# Task：<动词 + 范围>

> **状态**：draft / pending / in_progress / done  
> **关联图谱**：`docs/_tech_graph/xx_flow_xxx.md`  
> **关联 Issue/PR**：#xxx  
> **前端依赖**：`<前端任务文件名>`（如 API 变更需前端配合，否则填 "无"）

> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/*.md` 索引。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**；半自动 / 人工闸：[`docs/harness/prompts/HANDOFF_SEMI_AUTO.md`](../harness/prompts/HANDOFF_SEMI_AUTO.md)。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` / `recommended` / `not_applicable` |
| **test_strategy_note** | （仅 `not_applicable` 时 **必填** 一行理由；禁止滥用） |
| **freeze_id** | （可选）实现基准契约 ID，如 `SPEC-xxx@2026-05-22` 或 commit 短哈希 |
| **gates_before_code** | （可选）显式门闸列表；默认隐式：`failure_paths` + 验收命令 + 必读路径已齐 |
| **semi_auto** | `true` / `false` — 无 `pending` 人工闸时允许同会话链式戴帽（见 HANDOFF_SEMI_AUTO） |
| **audit_profile** | `full` / `post_close` / `human_only` — 审核节奏（见 HARNESS_V2 §5.5） |
| **git_branch** | `task/<slug>` — 半自动与实现 **禁止** 在 `main` 上连续提交 |

### 人工闸 `human_gate`

> **仅人** 可将 `pending` 改为 `approved`；Agent 遇阻塞帽 **拒执行** 所列 `blocks_hats`。

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1,30 | 初稿 task / SPEC 人扫 |
| HG-AUDIT-R1 | pending | 30 | 22 R1 落盘 `docs/harness/reviews/` 后人签 |
| HG-REINSPECT | pending | done | （可选）50 复检后人签、合并 PR 前 |

**`audit_profile` 速查**：

| 取值 | 适用 | 人工闸建议 |
|------|------|------------|
| `full` | 架构 / 跨仓 / 高风险 | 多轮 22（R1/R2…） |
| `post_close` | 工程流水线 task（**推荐**） | 闸 1：HG-TASK-DRAFT、HG-AUDIT-R1；闸 2：关账签收 |
| `human_only` | 纯文档 / 产品决策 | 关键步均 `pending`，不自动戴帽 |

---

## 背景与目标

<短段落，描述完成态行为。>

---

## 范围

- [ ] <具体事项 1>
- [ ] <具体事项 2>

## 非范围

- <明确排除的事项，减少越界>

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_xxx.md` |
| API 契约 | `POST /api/py/xxx` |
| 数据库表 | `public.xxx` |
| 图谱文件 | `docs/_tech_graph/xx_xxx.md` |

---

## 失败路径

> 每条建议：**触发条件** → **系统行为**（含错误码或 HTTP 状态）→ **是否可重试** → **用户可见类型**。  
> 缺失或不可操作化时，**30 执行帽拒开工**（仅输出缺口清单）。

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | <例：Supabase 不可用> | `500 DATABASE_DISCONNECT` | 是 | 服务暂不可用提示 |
| F2 | <例：参数非法> | `422` + 结构化 `detail` | 否 | 字段级错误说明 |

---

## 验收标准

- [ ] <验收项 1>
- [ ] <验收项 2>
- [ ] <验收项 3>

**测试 / TDD（与 `test_strategy` 对齐）**：

| test_strategy | 自检须含 |
|---------------|----------|
| `required` | 先失败可复现测试再实现；命令 + 通过证明 |
| `recommended` | 鼓励补测；以命令 + 人工为主 |
| `not_applicable` | `test_strategy_note` 一行理由 |

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见 `AGENTS.md`）。

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `<文件列表>` |
| 关键 env | `<新增/变更的环境变量>` |
| SQL 执行顺序 | `<init.sql → migration.sql>` |
| 接口变更 | `<新增/修改的端点>` |
| 图谱变更点 | `<_tech_graph/ 中更新的文件>` |

---

## 自检结论（执行者 · 40 帽回填）

> **40 自检帽** 运行 task 所列命令后，将 **原始输出要点** 与 pass/fail 结论写入本节。

| 项 | 结果 |
|----|------|
| 命令 | `<例：pytest …>` |
| 结论 | pass / fail |
| 要点 | `<日志摘要或失败原因>` |

---

## 给 Cursor

`<task_slug>`、`test_strategy`、`failure_paths`、`semi_auto`、`human_gate`、`audit_profile`、`git_branch`、`Harness`、`RECENT_TASK_SCHEDULE`
