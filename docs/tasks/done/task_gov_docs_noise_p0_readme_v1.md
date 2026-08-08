# Task：docs-noise 治理 · P0 修真冲突指针（C1–C3）

> **状态**：`done（2026-06-06 · PR #121 @ 5184c10）`  
> **Epic**：docs-noise 治理线 · **P0 试点**（Cursor Task 串链子 Agent 验证）  
> **关联 SPEC 导图**：[`docs/spec/governance/docs-noise-inventory/README.md`](../spec/governance/docs-noise-inventory/README.md)  
> **关联 SPEC 正文**：[`docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md`](../spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md) §8.1  
> **freeze_id**：`GOV-DOCS-NOISE-INVENTORY@2026-06-06`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `gov_docs_noise_p0_readme_v1` |
| **semi_auto** | `true` |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs 指针修正；无 `api/` / 契约 / CI workflow 变更 |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-docs-noise-p0-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **blocked_by** | 无 |
| **blocks** | P1/P2 子批（未建） |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **merge_policy** | `docs_only_ci_green_merge` |
| **close_action** | `merge` — CI Required 全绿后 **00/CLOSE 可执行** `gh pr merge --squash`（本 task 授权 · [#121](https://github.com/Cyning12/ai-ink-brain-api-python/pull/121)） |
| **experience_capture** | `recommended` |
| **experience_capture_note** | 执行简报已落盘 diary；关账后可蒸馏 Task 链 PROMPT 惯例 |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | approved | 22-R1, 30 | task 草案人扫；纯 docs 试点可预批后直进 30 |
| HG-GOV-P0-EXEC | approved | explore, 22, 30, 40, CLOSE | P0 执行链开干前人签 |

---

## 背景与目标

docs-noise SPEC 冻结 C1–C3 为 **高/中高/中** 真冲突。本 task **仅** 做 P0 最小扰动：更正三处 README 指针，**不** 删 invoke/review 审计链。

**完成态**：冲突寄存器 C1/C2/C3 在 SPEC 导图 README §3 标 `done`；三文件内容与 §8.1 验收一致。

---

## 范围（P0）

| ID | 交付 | 文件 |
| --- | --- | --- |
| **C1 / P0-1** | 更正 reviews 分工表述 | `docs/harness/invokes/README.md` |
| **C2 / P0-2** | flows 降为历史快照；L0 `_tech_graph` 优先 | `docs/README.md` §1 |
| **C3 / P0-3** | 遗留目录 POINTER | 新建 `docs/tech_graph/README.md` |

## 非范围

- P1 archived / P2 读序对齐 / P3 收敛
- 修改 `api/`、`tests/`、`.github/workflows/`
- 删除 `docs/harness/invokes/`、`reviews/` 历史全文

---

## 验收标准

- [x] C1：`invokes/README` 无「reviews 已移除」类表述；22→`reviews/`、20→`review_results/`、50→`reinspect_results/` 分工与 `reviews/README.md` 一致
- [x] C2：`docs/README.md` §1 端到端 **优先** `docs/_tech_graph/`；`docs/flows/` 标为历史快照
- [x] C3：`docs/tech_graph/README.md` 链至 `_tech_graph`；说明 2 份 gate 留痕
- [x] SPEC 导图 [`README.md`](../spec/governance/docs-noise-inventory/README.md) §3 中 C1–C3 状态改为 `done`
- [x] 单 PR · docs-only · CI Required 全绿（[#121](https://github.com/Cyning12/ai-ink-brain-api-python/pull/121) · squash merge `5184c10` · 2026-06-06）

---

### 自检结论（执行者）

> **40 帽回填** · 2026-06-06 · **建议 CLOSE + PR**

| 验收项 | 结果 |
| --- | --- |
| C1 invokes/README 无「已移除」；22/20/50 分工 | ✅ 已修；与 reviews/README §「与 20 / 50 分工」一致 |
| C2 docs/README §1 `_tech_graph` 优先；flows Legacy | ✅ L12–L14 已更新 |
| C3 docs/tech_graph/README.md POINTER + gate 留痕 | ✅ 新建；链至 `_tech_graph` |
| SPEC 导图 §3 C1–C3 = done | ✅ 已更新 |
| 未删 invoke/review 审计链 | ✅ 仅改 README |
| 未改 api/tests/workflows | ✅ diff 仅 docs |

**验证命令输出**：

```text
$ rg -n '已移除|reviews.*移除' docs/harness/invokes/README.md
(无命中 · exit 1)

$ test -f docs/tech_graph/README.md && echo OK
OK
```

**40 结论**：无阻塞；建议 CLOSE + `gh pr create` → CI 绿后按 **close_action: merge** 合入。

---

### KPI（00）

**rubric**: KPI_RUBRIC_v1_2 · **汇总**: **100%** · **状态**: **pass** · **帽**: explore · 22 · 30 · 40 · CLOSE  
**评诊日期**: 2026-06-06 · **简报**: [`docs/diary/2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md`](../diary/2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md)

| hat_code | round | agent_mode | D1 | D2 | D3 | D4 | D5 | judgment_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| explore | R1 | task_subagent | pass | pass | pass | pass | — | C1–C3 差分清晰；invoke 落盘 |
| 22 | R1 | task_subagent | pass | pass | pass | pass | — | 零阻塞；未预跑 `harness_task_validate`（CI 后补，记 warn 不入 D2 fail） |
| 30 | R1 | task_subagent | pass | pass | pass | pass | — | 三文件 + SPEC §3；scope 未越界 |
| 40 | R1 | task_subagent | pass | pass | pass | pass | — | rg/test 证据齐全 |
| CLOSE | close | main_chat | pass | pass | pass | pass | pass | PR #121 merged `5184c10`；task_validate 首轮红已 `05be476` 修复 |

**Task 级聚合**：D1 avg=100 · D2 min=100 · D3 avg=100 · D4 min=100 · D5 min=100  
**Task_KPI%** = 20+30+15+15+20 = **100%**（业务/工程双目标均达成）

**完成度（人读摘要）**

| 维度 | 得分 | 说明 |
| --- | ---: | --- |
| 业务交付（C1–C3） | **100%** | 验收 5/5 已勾选 |
| Task 链试点 | **100%** | 五帽 invoke/review 齐全；PR 已 merge；task 已归档 `done/` |
| 预期对照 | **满足** | docs 指针 + Cursor Task 链闭环均达设计目标 |

**关账**：PR #121 已 squash merge（`main@5184c10`）；本 task 已 `git mv` → `done/`。

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | fp-gov-p0-delete-audit | 误删 invoke/review 审计链 | **禁止**；仅改 README / POINTER |
| F2 | fp-gov-p0-readorder-drift | AGENTS 与 docs/README 仍不一致 | 本 task **不** 改 AGENTS（留 P2）；但不得引入新冲突 |

---

## Cursor 试点说明（Round T1）

Harness 00（父 Agent）串行 Task 链：`explore` → `22` → `30` → `40` → `CLOSE` → PR → **merge**（`close_action: merge` · PR #121 @ `5184c10` · 2026-06-06）。

Invoke 落盘：`docs/harness/invokes/by-task/gov-docs-noise-p0/`

**Prompt 真值**：

- 通用模板：[`docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md`](../harness/prompts/PROMPT_cursor_task_chain_serial_v1.md)
- T1 实例（各帽 §3 已填）：[`docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md`](../harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md)
