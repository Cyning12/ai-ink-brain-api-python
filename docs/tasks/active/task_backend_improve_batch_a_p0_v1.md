# Task：FAQ 改进 · Batch A（P0）工程补齐

> **状态**：`draft`（**草稿 · 非最终**；执行 Agent 可按实际裁剪范围、改写验收与 IMP 勾选）  
> **关联规划**：治理仓 [`09_PLAN_Ink后端改进方案_可推广_v1_zh.md`](../../../../ai_coding_governance/09_PLAN_Ink后端改进方案_可推广_v1_zh.md) · [`SUMMARY_三卷读者FAQ_完整结论`](../../../../ai_coding_governance/narrative/reviews/SUMMARY_三卷读者FAQ_完整结论_20260530_v1_zh.md)  
> **Agent Prompt**：[`docs/harness/prompts/PROMPT_FAQ改进_09PLAN_理解_v1_zh.md`](../harness/prompts/PROMPT_FAQ改进_09PLAN_理解_v1_zh.md)  
> **关联 Issue/PR**：（待开 PR 后填）  
> **前端依赖**：无

> **落盘规则**：验收后 `git mv` → `docs/tasks/done/` 并更新 `_views/`。  
> **方法论**：**不** redesign Harness/图谱；仅 FAQ 驱动的 DX + CI 可读性 + 模板。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 本 task 以 docs / CI workflow / 工具 stderr 为主；**无** `api/` 行为变更。若 IMP-B-01/02 需补 pytest，在 **实现备忘** 回填后 Agent 可改为 `recommended` 并补测。 |
| **freeze_id** | `FAQ-IMPROVE-BATCH-A@2026-05-30` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/backend-improve-batch-a-p0` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1,30 | 草稿 task 人扫后可改 `approved` |
| HG-AUDIT-R1 | pending | 30 | 22 R1 落盘 `docs/harness/reviews/` 后人签 |
| HG-AUDIT-CLOSE | pending | done | PR 合并 + 关账 22 |

---

## 背景与目标

三卷公众稿发表后，读者 FAQ 与 Ink 后端真值对照结论：**方法论方向正确**，缺口在 **合并入口、CI 红字可读、Blocking 模板、冷温热术语**。  
本 task 交付 **Batch A（P0）** 工程项，使后端成为 FAQ 改进的 **样板仓**（Batch B/C 另 task）。

**完成态（草案）**

- 新开 PR 自带 **Ink 轨** 自检模板；22 帽可对照 **Blocking** 表。  
- 开发者遇 **manifest/contract CI 红** 时，Runbook + stderr **能指导下一步**。  
- 改 task 文件时 CI **可选/默认** 跑 `harness_task_validate`。  
- 对内 **冷/温/热** 术语卡可被 22/10 引用。

---

## 范围（IMP-B · Batch A）

> **首包已落盘（2026-05-30）** — Agent 验收时勾选，不必重做除非需修订。

| ID | 项 | 状态（草稿） | 交付物 |
| --- | --- | --- | --- |
| IMP-B-10 | Ink 轨 PR 模板 | ✅ 初稿 | `.github/pull_request_template.md` |
| IMP-B-11 | 22 Blocking 表 | ✅ 初稿 | `docs/harness/prompts/hats/22-task-audit.md` §Blocking |
| IMP-B-20 | 冷/温/热术语卡 | ✅ 初稿 | `docs/harness/guides/GUIDE_冷温热层_对内术语_v1_zh.md` |
| — | Agent Prompt | ✅ 初稿 | `docs/harness/prompts/PROMPT_FAQ改进_09PLAN_理解_v1_zh.md` |
| IMP-B-01 | CI 红字 + Runbook | ✅ | `tools/tech_graph_*_check.py` stderr · `docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md` |
| IMP-B-02 | task 路径 `task_validate` | ✅ | `.github/workflows/tech-graph.yml` job `task_validate` |

**Agent 可调**：若 IMP-B-01/02 过大，可拆子 PR 或降 scope（须在 review 说明）；**不可** 引入 FAQ 已拒项（`graph.auto.json`、PR `/approve` 唯一闸等，见 PROMPT）。

---

## 非范围

- OpenSpec **O7** Delta→spec 关账（Batch C · IMP-B-14）  
- L2 manifest SPEC 全量关账（Batch B · IMP-B-03）  
- failure-cases 目录（Batch B · IMP-B-30）  
- 改 `api/` 业务逻辑、ChatBI 功能  
- 治理仓 `narrative/` 公众稿正文（本 task 仅后端工程）  
- 工作区 `Projects/docs/harness/` 任何写入  

---

## 行为变更（Delta）

**无**（对外 HTTP/SSE/DB 行为不变）。

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| 09 PLAN | `ai_coding_governance/09_PLAN_Ink后端改进方案_可推广_v1_zh.md` |
| FAQ SUMMARY | `ai_coding_governance/narrative/reviews/SUMMARY_…` |
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| pr-post-ci | `docs/spec/governance/SPEC-Governance-PR-Post-CI-v1.md` |
| task_validate | `tools/harness_task_validate.py` |
| 图谱入口 | `docs/_tech_graph/00_main.ai.md`（一般 **不必改**） |

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-task-validate-fail` | PR 改 task 缺 Delta/Scenario | CI `task_validate` exit 非 0 | 是 | PR checks 红 + stderr |
| F2 | `fp-manifest-check-fail` | manifest 与代码不一致 | `manifest_check` exit 非 0 | 是 | 见 IMP-B-01 三段式 stderr（待做） |

---

## 验收标准

- [ ] **IMP-B-01**：故意制造 manifest/contract 不一致 PR，stderr 含 **位置 / 期望 vs 实际 / 下一步**；Runbook 链自 `docs/harness/README.md`
- [ ] **IMP-B-02**：仅改 `docs/tasks/active/*.md` 且缺字段的 PR，CI **失败**；补齐后 **通过**
- [ ] **IMP-B-10/11/20** 与 PROMPT：README 可发现；22 审查可对照 Blocking（首包已存在则 **抽检** 即可）
- [ ] `docs/harness/README.md` 已链 PROMPT + guides（首包已做则勾选）
- [ ] PR 上 `pytest` workflow 全绿（本地等价：`pytest tests -m "not intent_eval and not intent_benchmark"`）
- [ ] 22 R1 审查落盘：`docs/harness/reviews/by-task/backend-improve-batch-a-p0/`（路径 Agent 可微调）
- [ ] 关账：`git mv` 本 task → `done/`；可选 50（本 task `not_applicable` 时可省略，由 22 CLOSE 说明）

---

## 实施清单（Agent 可增删）

- [ ] 1.1 读 PROMPT + 本 task；确认 **首包** 四文件是否需润色  
- [x] 1.2 **IMP-B-01**：改 check 脚本 stderr + 写 Runbook；本地/PR 故意红一次  
- [x] 1.3 **IMP-B-02**：workflow `paths: docs/tasks/**` + `harness_task_validate.py`  
- [x] 1.4 更新 `docs/harness/README.md`（Runbook 链）  
- [ ] 1.5 22 R1 → 30 实现 → 40 自检 → 22 CLOSE  
- [ ] 1.6 更新治理仓 `09_PLAN` §2 IMP 状态列（可选 · 跨仓只读后人工或另 commit）

---

## 实现备忘（由 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `tools/tech_graph_ci_stderr.py` · `tools/tech_graph_manifest_check.py` · `tools/tech_graph_contract_check.py` · `docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md` · `docs/harness/README.md` · `.github/workflows/tech-graph.yml` |
| workflow 变更 | `tech-graph.yml` 增 job `task_validate`（`docs/tasks/active/*.md` 变更时跑 `harness_task_validate.py`） |
| 故意红 PR / commit | 本地：`python tools/tech_graph_manifest_check.py` 改 `_manifest.json` 后应见三段式 stderr；task：删 test_strategy 后 `harness_task_validate.py` 应 FAIL |
| 图谱变更点 | 无（预期） |

---

## 自检结论（40 帽 · 待填）

| 项 | 结果 |
|----|------|
| 命令 | |
| 结论 | |
| 要点 | |

---

## 给 Cursor

`task_backend_improve_batch_a_p0`、`FAQ-IMPROVE-BATCH-A`、`IMP-B-01`、`IMP-B-02`、`09_PLAN`、`PROMPT_FAQ改进_09PLAN`、`Harness`、`not_applicable`、`post_close`

---

## 修订记录（task 本体）

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| draft-v0 | 2026-05-30 | 草稿；首包 IMP-B-10/11/20 + PROMPT 已落盘 |
