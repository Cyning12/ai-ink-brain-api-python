# Task · Ops Session S5.1 Extract ADR（monorepo 子包 vs 独立 repo/PyPI）

> **状态**：`draft` · 00 统筹起草 · 2026-07-03  
> **epic**：Session Orchestrator · S5 `ops-session-s5-extract`  
> **schedule_ref**：SPEC §11.3 · §12.1 S5 · BLOCKERS B5 · PLAN §5  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) §11 harness_runtime 包边界 · §12.3 验收标准  
> **前置**：`[task_ops_session_s5_import_boundary_api_v1.md](./task_ops_session_s5_import_boundary_api_v1.md)` · HG-AUDIT-R1 approved  
> **配对前端**：无（架构决策）  
> **依赖**：S5.0 import 边界 pytest 绿  
> **人拍板**：D1 = **S5.2 graph_delta promote UI 要做** · D4 = **S5.1 + MVP+ 完整 checklist 通过后再确认 Epic 收官**（PLAN §9）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-session-s5-extract-adr` |
| **module_id** | `OPS-SESSION-ORCH` |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **test_strategy** | `required` |
| **worktree_root** | `ai-ink-brain-api-python/`（ADR 同时落盘工作区 `docs/harness/guides/`） |
| **git_branch** | `task/ops-session-s5-extract-adr` |
| **blocks** | S5.2 `ops-session-s5-graph-promote`（可选）· Epic v1 freeze |
| **blocked_by** | S5.0 `ops-session-s5-import-boundary-api` |

### 行为变更 Delta

| 变更 | 类型 | 触达 api/ | 说明 |
| --- | --- | --- | --- |
| 新增 ADR 文档 | ADDED | `docs/harness/guides/ADR_ops_session_s5_extract_v1_zh.md` | 00 骨架 · 30 回填 |
| 新增 Host 适配评估 | ADDED | `api/ops` 注入点清单 | 明确 Runtime 与 Host 边界 |
| 可能的 pyproject 占位 | ADDED | `api/harness_runtime/pyproject.toml`（可选） | 若 ADR 结论走独立子包 |
| 无 Runtime 逻辑改动 | — | — | 本 task 为决策与适配文档 |

---

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 人签 · 2026-07-03 · 派工执行 |
| HG-AUDIT-R1 | `approved` | 30 | 人签 · 2026-07-03 · 20-task-audit 关注点由 30/50 复核 |

---

## 背景与目标

BLOCKERS B5 已拍板：S0–S4 在 `ai-ink-brain-api-python/api/harness_runtime/` 内实现；**S5 评估独立 repo / PyPI**；本 task 产出抽包/留守的架构决策记录（ADR），并明确 Host 侧（`api/ops`）需保留的适配层，使后续无论留守 monorepo 还是抽包，边界都可持续验证。

**完成态一句话**：ADR 落盘并得出明确结论（留守 monorepo 子包 / 独立仓库 / PyPI），同时给出 `api/ops` Host 适配点清单，保证 Runtime 与业务仓解耦。

### 拍板（00 统筹 · BLOCKERS B5）

| # | 决策 |
| --- | --- |
| D1 | ADR 必须覆盖：留守 `api/harness_runtime/` · 独立 Git repo · PyPI 发布 · 三种形态的成本/收益/风险 |
| D2 | Host 适配层留在 `api/ops/`，**不**随 Runtime 抽走；注入方式：Protocol/DTO + 环境变量 |
| D3 | 抽包结论 **不推翻** S5.0 import 边界；若抽包则边界测试须在新仓库复用 |
| D4 | ADR 须经 20-task-audit R1 后人签 HG-AUDIT-R1 |

---

## 范围

- [ ] 00 起草 ADR 骨架：`docs/harness/guides/ADR_ops_session_s5_extract_v1_zh.md`
- [ ] 30 回填评估维度：构建/发布/CI/版本/依赖/安全/团队维护成本
- [ ] 列出 `api/ops` 对 `harness_runtime` 的注入点（LLM Provider · checkpointer config · probe runner env · ops events）
- [ ] 若结论为独立 repo/PyPI，给出迁移步骤与回滚方案
- [ ] 若结论为留守 monorepo，给出子包化建议（`pyproject.toml` / namespace）
- [ ] 补充 S5.0 边界测试在新形态下的复用策略
- [ ] ADR 须经 ruff（若含代码清单）与 20-task-audit R1

---

## 非范围

- 不实际执行抽包迁移（除非 ADR 结论要求且另开 task）
- 不改 `harness_runtime` 内部实现逻辑
- 不改 Ink 前端
- 不处理 graph_delta promote（S5.2 可选）
- 不替代 BLOCKERS B5 原决策；本 ADR 为 B5 的 S5 评估细化

---

## 失败路径

| # | Scenario ID | 触发 | 行为 | 可重试 |
| --- | --- | --- | --- | --- |
| F1 | fp-adr-ambiguous | ADR 结论模糊，无明确留守/抽包结论 | 20-task-audit 驳回，要求补充决策树 | 是（修改 ADR） |
| F2 | fp-host-boundary-missing | 未列出 `api/ops` 适配点 | ADR 不完整，30 须补全 | 是（修改 ADR） |
| F3 | fp-test-reuse-gap | 未说明 S5.0 边界测试在抽包后如何复用 | R1 驳回 | 是（修改 ADR） |
| F4 | fp-contradict-b5 | ADR 与 BLOCKERS B5 已拍板结论冲突 | 拒绝，须回退到 B5 真值 | 否（须重新对齐） |

---

## 20-task-audit 关注点

- [ ] S5.0 与 S5.1 是否应合并为单一 task？（人要求 20-task-audit 再次确认拆分合理性）
- [ ] ADR 结论是否明确：留守 / 独立 repo / PyPI / 分阶段
- [ ] Host 适配层清单是否完整
- [ ] S5.0 边界测试在新形态下的复用策略是否可行

---

## 验收标准

- [ ] ADR 文件落盘 `docs/harness/guides/ADR_ops_session_s5_extract_v1_zh.md`
- [ ] ADR 结论明确：继续 monorepo 子包 / 独立 repo / PyPI 三选一（或分阶段路线图）
- [ ] 含 Host 适配点清单（`api/ops` 注入点）
- [ ] 含迁移/留守的 cost/benefit/risk 表
- [ ] 含 S5.0 边界测试复用策略
- [ ] 20-task-audit R1 通过 · HG-AUDIT-R1 approved

**合并前必绿**：ADR 审阅通过 · 无新增失败路径未闭合

---

### 自检结论（执行者，30/20 回填）

| 项 | 结果 |
| --- | --- |
| **日期** | 2026-07-03 |
| **分支** | `task/ops-session-s5-extract-adr` |

```text
ADR 结论：A（留守 monorepo 子包，显式子包化）+ D→B→C 分阶段路线图
Host 适配点：7 项（H1 LLM Provider · H2 Checkpointer · H3 Probe Runner · H4 Ops Events · H5 Session Store Root · H6 Run Store · H7 Demo Cache/Queries 透传）
20 R1 状态：HG-AUDIT-R1 approved · 本 task 仅文档/决策，未改 Runtime 逻辑
新增文件：api/harness_runtime/pyproject.toml（最小占位）
ruff check api/harness_runtime → All checks passed!
```

---

## 给 Cursor

`ops-session-s5-extract-adr` · **HG-AUDIT-R1 pending** · 30 不可开工直至人签；本 task 以文档与决策为主，不改动 Runtime 逻辑。
