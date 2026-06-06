# Task · MANIFEST · docs-noise 治理线（Claude Code 编排）

> **状态**：`active`  
> **性质**：**母单 / 排期 MANIFEST** — 非单次交付；子批 P0/P1/P2/P3 各建 `task_gov_docs_noise_*`  
> **Epic**：docs-noise 治理 · [`docs/spec/governance/docs-noise-inventory/README.md`](../spec/governance/docs-noise-inventory/README.md)  
> **freeze_id**：`GOV-DOCS-NOISE-INVENTORY@2026-06-06`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `governance_docs_noise_line_manifest_v1` |
| **orchestration** | **Claude Code** · Lead 主会话 + **串行 spawn** `.claude/agents/harness-*` |
| **git_branch（当前子批）** | `task/gov-docs-noise-p1-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **test_strategy** | `not_applicable`（母单本身无实现） |

---

## 档期发现（Lead / subagent 开跑前 · 不必猜）

Agents **无**项目日历注入；按下列 **L0/L1 真值** 查当前安排：

| 序 | 来源 | 用途 |
| --- | --- | --- |
| 1 | [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) **§1.2** | 本仓 **排期真值** · docs-noise 条目 |
| 2 | **本 MANIFEST** `## Round 表` | 治理线 T0/T2b/T2c 下一棒 |
| 3 | [`docs/_tech_graph/02_version.md`](../../_tech_graph/02_version.md) | 版本时间线 · 架构迭代档期 |
| 4 | `python tools/tech_graph_graph_query.py neighbors <id>` | 改拓扑前按需 · **非**日常排期首选 |
| 5 | [`docs/coding_wiki/concepts/task-schedule-ink-backend.md`](../../coding_wiki/concepts/task-schedule-ink-backend.md) | L2 pointer → RECENT · **不**替代 RECENT |

**禁止**：默认 glob `docs/diary/` 或 `docs/harness/invokes/` 推断排期。

---

## 子批状态

| 批次 | Round | task | 执行器 | 状态 | PR |
| --- | --- | --- | --- | --- | --- |
| **P0** | T1 | [`done/task_gov_docs_noise_p0_readme_v1.md`](../done/task_gov_docs_noise_p0_readme_v1.md) | **Cursor Task 链** | **done** | [#121](https://github.com/Cyning12/ai-ink-brain-api-python/pull/121) |
| **P1** | T0→T2b | [`done/task_gov_docs_noise_p1_archived_v1.md`](../done/task_gov_docs_noise_p1_archived_v1.md) | **Claude Code** | **done** | [#123](https://github.com/Cyning12/ai-ink-brain-api-python/pull/123) |
| **P2** | T0→T2c | [`active/task_gov_docs_noise_p2_readorder_v1.md`](../active/task_gov_docs_noise_p2_readorder_v1.md) | **Claude Code** | `draft`（T0 改稿完成 · 待人签 gate） | — |
| **P3** | T3 | 未建 | Claude Code | 长期 | — |

**P0 留证**：[`docs/diary/2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md`](../../diary/2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md)

---

## Round 表（Claude Lead）

| Round | 帽链 | PROMPT 实例 | 说明 |
| --- | --- | --- | --- |
| **T0（P1）** | Lead 或 `harness-10-requirements` | [`PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md) | 写 **P1 task** + gate `pending` → **人签** |
| **T2b** | explore → 22 → 30 → 40 → CLOSE（**跳过 50**） | [`PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md) | P1 执行 · SPEC §8.2 |
| **T0（P2）** | Lead 或 `harness-10-requirements` | [`PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md) | P2 task 改稿确认 + 脚手架 |
| **T2c** | explore → 22 → 30 → 40 → CLOSE（**跳过 50**） | [`PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md) | P2 执行 · SPEC §8.3 |
| T3 | CLOSE + META | （未建） | P3 / 母单关账 |

**通用模板**：[`PROMPT_claude_chain_serial_v1.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1.md)

---

## Subagent  roster（`.claude/agents/`）

| 文件 | 帽 | T0 | T2b |
| --- | --- | --- | --- |
| `harness-10-requirements.md` | 10 | ✅ | — |
| `harness-explore-l0.md` | explore | — | ✅ |
| `harness-22-audit.md` | 22 | — | ✅ |
| `harness-30-docs.md` | 30 | — | ✅ |
| `harness-40-check.md` | 40 | — | ✅ |
| `harness-50-reinspect.md` | 50 | — | **跳过**（纯 docs · `not_applicable`） |

Lead = 主会话 · 读 `CLAUDE.md` → `AGENTS.md` + 本 MANIFEST + 当前 Round PROMPT §1。

**禁止**：Agent Teams · 内置 Explore/Plan 裸用（须自定义 agent 或 spawn 内嵌读序）。

---

## P1 范围指针（SPEC §8.2）

| ID | 交付 |
| --- | --- |
| P1-1 | `docs/delivery/v0.2.0-code-rag/README.md` archived 横幅 → `docs/harness/README` + `docs/spec/` |
| P1-2 | 新建 `docs/flows/README.md` · Legacy · superseded by `_tech_graph` |

---

## 人工闸（母单 · 仅说明）

子批 task 各自维护 `HG-TASK-DRAFT` / `HG-GOV-P*-EXEC`；**Lead 禁止代签**。

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | `fp-manifest-round-skip` | 子批未按 T0→T2b→T2c→T3 顺序执行 | 阻塞关账；回退至 Round 表核对 |
| F2 | `fp-manifest-scope-creep` | 母单直接改 `api/` / `tests/` / CI workflow | **禁止**；母单仅排期与索引，实现归子批 task |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | v1：P1 Claude 脚手架 · MANIFEST + agents + T0/T2b PROMPT |
