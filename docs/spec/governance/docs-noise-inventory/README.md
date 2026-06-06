# docs/ 噪音 / 重复 / 冲突 · 治理导图

> **性质**：治理线 **需求总纲** 的默认入口（**导图**）；日常 **只读本 README**，正文 SPEC 仅在开 task / 22 审核 / 关账验收时打开。  
> **状态**：`draft` · **freeze_id**：`GOV-DOCS-NOISE-INVENTORY@2026-06-06`  
> **盘点基线**：2026-06-06 · 本仓约 **1095** 个 `docs/**/*.md`

---

## 0. 一句话

本仓 docs **不是乱**，而是 Harness 过程库 + L0/L1/L2 分层叠加；冲突寄存器 **C1–C6 已 close**，治理线 **P0–P3 已执行**，**禁止** 删 invoke/review 审计链。

---

## 1. 文档地图（勿合并为单文件）

| 序号 | 文件 | 何时读 |
| --- | --- | --- |
| **0** | **本 README** | 立项、排期、Agent 默认 |
| **1** | [`SPEC-Governance-Docs-Noise-Inventory-v1_zh.md`](./SPEC-Governance-Docs-Noise-Inventory-v1_zh.md) | 开 task、22/50、冲突寄存器维护、VERIFY 全文 |

**Agent 纪律**：未 `@` 正文 SPEC 且非执行治理 task 时，**禁止** 默认打开 §1 全文（327 行）。

---

## 2. 体量快照（基线）

| 目录 | 文件数 | 认知 |
| --- | ---: | --- |
| `docs/harness/` | 512 | 过程工件 · 非必读全量 |
| `docs/diary/` | 257 | 非必读 · task/`@` 才开 |
| `docs/tasks/` | 206 | L1 执行 |
| `docs/_tech_graph/` | 23 | **L0 真值** |
| 其余 | — | 见正文 SPEC §2 |

约 **70%** 为 Harness + diary 留证；**设计如此**，不是实现 bug。

---

## 3. 冲突寄存器（摘要 · 详情见正文 §4）

| ID | 严重度 | 摘要 | 状态 |
| --- | --- | --- | --- |
| **C1** | 高 | `invokes/README` 误写 reviews「已移除」 | `done` |
| **C2** | 中高 | `docs/README` 推 flows，AGENTS 推 `_tech_graph` | `done` |
| **C3** | 中 | `docs/tech_graph/` vs `docs/_tech_graph/` 易混 | `done` |
| **C4** | 中 | PROJECT_CONFIG 仍提 `.cursorrules`（已不存在） | `done` |
| **C5** | 低中 | 根 README 端点/ env 不完整 | `done` |
| **C6** | 低 | HARNESS_V2_PLAN vs AGENTS 权威链略歧义 | `done` |

---

## 4. 分批治理（执行顺序）

| 批次 | 主题 | 首个 task 建议 |
| --- | --- | --- |
| **P0** | 修 C1/C2/C3 三处 README 指针 | `task_governance_docs_noise_cleanup_v1` |
| **P1** | `delivery/`、`flows/` 标 archived / superseded | 同上母单或 P1 子批 |
| **P2** | AGENTS / docs/README / PROJECT_CONFIG 读序对齐 | P2 子批 |
| **P3** | `spec/governance/` Wiki 批次收敛 · showcase 索引 | 长期 |

**test_strategy**：纯 docs 指针 → `not_applicable`。

---

## 5. Agent 最小读序（canonical）

```text
1. docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md
2. docs/_tech_graph/（graph_query 按需）
3. docs/tasks/RECENT_TASK_SCHEDULE.md → active/task_*.md
4. 涉 ChatBI → docs/spec/v3-agent/
5. 关账回顾 → docs/coding_wiki/syntheses/<slug>.md
```

**刻意不读**：`docs/diary/` 全树 · `docs/harness/invokes/` glob · `docs/showcase/` · `docs/delivery/` · `docs/flows/`（除非 task 指向）。

**档期（Agent 无注入时）**：[`RECENT_TASK_SCHEDULE.md`](../../../tasks/RECENT_TASK_SCHEDULE.md) **§1.2** → [`task_governance_docs_noise_line_manifest_v1.md`](../../../tasks/active/task_governance_docs_noise_line_manifest_v1.md) → 可选 `docs/_tech_graph/02_version.md`。

---

## 6. 执行编排（Claude Code · Task 链）

| 项 | 路径 |
| --- | --- |
| **MANIFEST（Lead 必读）** | [`docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md`](../../../tasks/active/task_governance_docs_noise_line_manifest_v1.md) |
| **Claude 通用 PROMPT** | [`docs/harness/prompts/PROMPT_claude_chain_serial_v1.md`](../../../harness/prompts/PROMPT_claude_chain_serial_v1.md) |
| **P1 T0/T2b** | [`PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md`](../../../harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md) · [`PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md`](../../../harness/prompts/PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md) |
| **P2 T0/T2c** | [`PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md`](../../../harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md) · [`PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`](../../../harness/prompts/PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md) |
| **P2 R1 改稿 handoff** | [`PROMPT_claude_P2_pre_exec_amendments_zh.md`](../../../harness/prompts/PROMPT_claude_P2_pre_exec_amendments_zh.md) |
| **Subagents** | [`.claude/agents/`](../../../../.claude/agents/README.md) · `harness-10` … `harness-50` |
| **P0 试点（Cursor）** | [`docs/diary/2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md`](../../../diary/2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md) |

**当前下一棒**：docs-noise 治理线 **已 CLOSE**（P0–P3 全量 done · PR #121/#123/#126/#129）。

---

## 7. 关联

| 文档 | 关系 |
| --- | --- |
| [`../README.md`](../README.md) | governance 总索引 |
| [`../../README.md`](../../README.md) | `docs/spec/` 根 · SPEC 分目录约定 |
| [`../../../tasks/RECENT_TASK_SCHEDULE.md`](../../../tasks/RECENT_TASK_SCHEDULE.md) | 不压过 ChatBI 业务队列 |
| [`../SPEC-Governance-Wiki-Agent-Readorder-v1.md`](../SPEC-Governance-Wiki-Agent-Readorder-v1.md) | §5 读序兼容 Wiki L2 |
| [`../../../diary/2026-06-05-plan-agent-analysis/00_README.md`](../../../diary/2026-06-05-plan-agent-analysis/00_README.md) | Plan Agent 对比实验 · 印证导航/读序问题 · **非 L0** |

---

## 8. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | T3 母单关账 · 治理线 P0–P3 全量 CLOSE |
| 2026-06-06 | P1 Claude 脚手架 · §6 执行编排 · §5 档期指针 |
| 2026-06-06 | 从 governance 根目录迁入独立文件夹；新增本导图 README |
| 2026-06-06 | 链入 diary Plan Agent 对比实验留证 |
