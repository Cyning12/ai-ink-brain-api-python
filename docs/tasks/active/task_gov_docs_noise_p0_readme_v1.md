# Task：docs-noise 治理 · P0 修真冲突指针（C1–C3）

> **状态**：`pending`  
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

- [ ] C1：`invokes/README` 无「reviews 已移除」类表述；22→`reviews/`、20→`review_results/`、50→`reinspect_results/` 分工与 `reviews/README.md` 一致
- [ ] C2：`docs/README.md` §1 端到端 **优先** `docs/_tech_graph/`；`docs/flows/` 标为历史快照
- [ ] C3：`docs/tech_graph/README.md` 链至 `_tech_graph`；说明 2 份 gate 留痕
- [ ] SPEC 导图 [`README.md`](../spec/governance/docs-noise-inventory/README.md) §3 中 C1–C3 状态改为 `done`
- [ ] 单 PR · docs-only · CI Required 全绿

---

## 失败路径

| 触发 | 行为 |
| --- | --- |
| 误删 invoke/review 审计链 | **禁止**；仅改 README / POINTER |
| AGENTS 与 docs/README 仍不一致 | 本 task **不** 改 AGENTS（留 P2）；但不得引入新冲突 |

---

## Cursor 试点说明（Round T1）

Harness 00（父 Agent）串行 Task 链：`explore` → `22` → `30` → `40` → `CLOSE` → PR。

Invoke 落盘：`docs/harness/invokes/by-task/gov-docs-noise-p0/`

**Prompt 真值**：

- 通用模板：[`docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md`](../harness/prompts/PROMPT_cursor_task_chain_serial_v1.md)
- T1 实例（各帽 §3 已填）：[`docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md`](../harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md)
