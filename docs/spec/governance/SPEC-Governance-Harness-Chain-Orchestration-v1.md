# SPEC — 治理：Harness 链式编排常模 · semi_auto 退场（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft`（**A 轨 task 30 帽定稿**） |
| **freeze_id** | `GOV-HARNESS-CHAIN-ORCHESTRATION@2026-06-08` |
| **Epic** | [`task_harness_semi_auto_retirement_manifest_v1.md`](../../tasks/active/task_harness_semi_auto_retirement_manifest_v1.md) |
| **执行 task** | [`task_harness_chain_orchestration_spec_v1.md`](../../tasks/active/task_harness_chain_orchestration_spec_v1.md) |
| **规划** | [`docs/diary/2026-06-08-harness-chain-next-task-planning_zh.md`](../../diary/2026-06-08-harness-chain-next-task-planning_zh.md) |

---

## 0. 完成态（一句话）

本仓 **新 task / 改码关账** 默认用 **`orchestration` + `PROMPT_*_chain_serial_*` + invoke 落盘** 串行帽链；**`semi_auto: true` 进入过渡/废弃**，不再作为推荐常模。全面废弃须 **A（本文）+ B（api 链式试点）** 齐 CLOSE。

---

## 1. 背景

| 已验证 | 来源 |
| --- | --- |
| Cursor Task 链 · docs | docs-noise P0 · #121 |
| Claude Code spawn 链 · docs | docs-noise P1–P3 · #123–#129 |
| Kimi Agent 链 · docs | recentsync · #134 |
| P0 取向 | 「Task 链 = **改代码主力** · semi_auto 计划废弃」 |

**缺口**：`HARNESS_V2_PLAN` §5.6 仍列 `semi_auto`；`TASK_TEMPLATE` 无 `orchestration`；**无 api + required + 50 链式关账**（→ **B 轨**）。

---

## 2. `orchestration` 字段（task 元信息 · 必填于链式 task）

| 取值示例 | 含义 |
| --- | --- |
| `Cursor Task 链` | 父 Agent `Task(subagent_type=…)` 串行 |
| `Claude Code` | Lead spawn `.claude/agents/harness-*` |
| `Kimi Code` | Lead `Agent()` 串行 · prompt 内联读序 |
| `MANIFEST 仅` | 母单不执行 |

**与 `semi_auto` 关系**：

| | `semi_auto: true`（过渡/废弃） | 链式（推荐） |
| --- | --- | --- |
| 换帽 | 同会话自动下一帽 | Lead 按 PROMPT 显式 spawn / Task |
| 真值 | invoke + HANDOFF_SEMI_AUTO | invoke + **`PROMPT_*_chain_serial_*`** |
| 子 Agent 上下文 | 会话历史叠加 | 隔离（KC 须内联读序） |
| Git | 混用 | **Lead 独占 commit**（CC/KC 约定） |

**新建 task 默认**：`semi_auto: false` + 填 `orchestration` + 链 PROMPT 实例路径。

---

## 3. 帽链常模

### 3.1 docs-only（`test_strategy: not_applicable`）

```text
explore → 22 → 30 → 40 → CLOSE → PR → CI → merge
（跳过 50 · 须在 task/PROMPT 明示）
```

### 3.2 改码（`test_strategy: required`）

```text
explore → 22 → 30（先失败测试 → 实现）→ 40 → 50 → CLOSE → PR → CI → merge
（50 必须 · reinspect_results/）
```

---

## 4. Prompt 真值（本仓）

| 执行器 | 通用 | 实例示例 |
| --- | --- | --- |
| Cursor | [`PROMPT_cursor_task_chain_serial_v1.md`](../../harness/prompts/PROMPT_cursor_task_chain_serial_v1.md) | T1 gov-docs-noise P0 |
| Claude Code | [`PROMPT_claude_chain_serial_v1.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1.md) | T1 orchestration-spec · T1 intent-retry |
| Kimi Code | [`PROMPT_kimi_task_chain_serial_v1.md`](../../harness/prompts/PROMPT_kimi_task_chain_serial_v1.md) | T1 recentsync |

对照：[`COMPARISON_kimi_claude_chain_prompt_v1_zh.md`](../../harness/prompts/COMPARISON_kimi_claude_chain_prompt_v1_zh.md)

---

## 5. 验收（VERIFY · A 轨）

```bash
test -f docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md
rg -n 'orchestration' docs/tasks/templates/TASK_TEMPLATE.md
rg -n '链式|semi_auto' docs/harness/HARNESS_V2_PLAN.md
python tools/harness_task_validate.py docs/tasks/active/task_harness_chain_orchestration_spec_v1.md
```

---

## 6. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | v1 草案 · A 轨 task 脚手架 |
