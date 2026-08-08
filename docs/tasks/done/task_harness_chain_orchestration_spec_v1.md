# Task：治理 SPEC · Harness 链式编排常模（semi_auto 退场 · A 轨）

> **状态**：`done`（PR #135 · 2026-06-08）  
> **Epic**：[`task_harness_semi_auto_retirement_manifest_v1.md`](task_harness_semi_auto_retirement_manifest_v1.md) · **A 轨 / G1**  
> **关联 SPEC（本 task 产出）**：[`docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md`](../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md)  
> **freeze_id**：`GOV-HARNESS-CHAIN-ORCHESTRATION@2026-06-08`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `harness_chain_orchestration_spec_v1` |
| **orchestration** | **Claude Code** · Lead + 串行 spawn `.claude/agents/harness-*` |
| **semi_auto** | `false` |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 governance docs / 模板 / 索引；无 `api/` 行为变更 |
| **audit_profile** | `post_close` |
| **git_branch** | `task/harness-chain-orchestration-spec-v1` |
| **merge_policy** | `docs_only_ci_green_merge` |
| **close_action** | `merge` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **experience_capture** | `required` |
| **experience_capture_note** | 关账后更新 planning diary §5 checklist |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | approved | 22-R1, 30 | task + SPEC 草案 + PROMPT 人扫 · **2026-06-08 用户授权代填** |
| HG-CHAIN-A-EXEC | approved | explore, 22, 30, 40, CLOSE | A 轨 T1 执行链 · **2026-06-08 用户授权代填** |

---

## 背景与目标

P0 Task 链试点已写「**Task 链定为改代码主力；semi_auto 计划废弃**」，但 `HARNESS_V2_PLAN` §5.6 仍将 `semi_auto` 列为可选常模；`TASK_TEMPLATE` 缺 **`orchestration`** 字段说明。

本 task（**A 轨**）将链式编排升格为 **governance 真值**，并同步模板与索引。** alone 不宣称 semi_auto 全面废弃** — 须与 **B 轨**（api 链式 U1.5）齐 CLOSE。

---

## 范围

| ID | 交付 | 文件 |
| --- | --- | --- |
| **A-1** | 新建/定稿 **SPEC** 正文 | `docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md` |
| **A-2** | `TASK_TEMPLATE` 增 **`orchestration`** 行 + 与 `semi_auto` 关系说明 | `docs/tasks/templates/TASK_TEMPLATE.md` |
| **A-3** | `HARNESS_V2_PLAN` §5.6 增补 **链式常模** + `semi_auto` **过渡/废弃** 表述（不删历史） | `docs/harness/HARNESS_V2_PLAN.md` |
| **A-4** | `docs/spec/governance/README.md` 索引新 SPEC | 同上目录 |
| **A-5** | `docs/harness/prompts/README.md` 链式三执行器 + MANIFEST 指针 | prompts README |
| **A-6（E 合并）** | `docs-noise-inventory/README.md` §6 补 KC/#134/COMPARISON · MANIFEST→`done/` | 导图 §6 |
| **A-7** | `docs/tasks/RECENT_TASK_SCHEDULE.md` 新增 **§1.3 semi_auto 退场双轨** 一行表 | RECENT |

## 非范围

- 改 `api/`、`tests/`、`.github/workflows/`
- B 轨 Intent U1.5 实现（另 task · 本 task 仅链 SPEC）
- 删 `docs/harness/invokes/` / `reviews/` 历史

---

## 验收标准

- [ ] A-1～A-7 交付物存在且互相链接一致
- [ ] SPEC 含：`orchestration` 枚举 · 帽链 · Git 仅 Lead · 与 `semi_auto` 对照表 · 三执行器 PROMPT 指针
- [ ] `python tools/harness_task_validate.py` 本 task **OK**
- [ ] Harness T1：invoke + 22 R1 落盘 · slug `harness-chain-orchestration-spec`
- [ ] 单 PR docs-only · CI Required 全绿

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | fp-chain-a-scope-drift | 30 帽改 `api/` 或 workflow | **禁止** |
| F2 | fp-chain-a-delete-semi-auto-doc | 未写过渡说明即删 `semi_auto` 全文 | **禁止**；须「废弃/过渡 + 链式替代」 |
| F3 | fp-chain-a-no-orchestration-field | TASK_TEMPLATE 未增 `orchestration` | 40 **fail** |

---

## 链式执行（Round T1）

**Prompt**：[`PROMPT_claude_chain_serial_v1_T1_harness-chain-orchestration-spec_zh.md`](../harness/prompts/PROMPT_claude_chain_serial_v1_T1_harness-chain-orchestration-spec_zh.md)

**帽链**：explore → 22 → 30 → 40 → CLOSE（**跳过 50** · not_applicable）

**invoke**：`docs/harness/invokes/by-task/harness-chain-orchestration-spec/`

---

## 关账（CLOSE · 2026-06-08）

| 项 | 内容 |
| --- | --- |
| **PR** | #135 · `task/harness-chain-orchestration-next-v1` → `main` · squash merge `ceadc4d` |
| **帽链** | explore → 22 R1 → 30 → 40（跳过 50 · `not_applicable`） |
| **invoke** | `docs/harness/invokes/by-task/harness-chain-orchestration-spec/` 4 文件 |
| **review** | `docs/harness/reviews/by-task/harness-chain-orchestration-spec/task_harness_chain_orchestration_spec_v1_audit_R1_20260608.md` |
| **CI** | pytest ✓ · tech-graph ✓ · tech-graph-contract ✓ · pr-post-ci ✓ · verify-fast ✓ |
| **KPI** | 按 `KPI_RUBRIC_v1_2` · `CLOSE` 聚合 |
| **经验** | MANIFEST 须补 `failure_paths`（task_validate 硬性检查）· branch 名 `next-v1` ≠ task 头 `spec-v1`（以实际分支为准） |

---

## 给 Cursor / CC

`orchestration=Claude Code` · `semi_auto=false` · 开跑前读 T1 PROMPT §1 · `human_gate` 须预批。
