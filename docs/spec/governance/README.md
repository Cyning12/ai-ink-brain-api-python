# governance — 治理 / Harness / Coding Wiki 规格

> **非 ChatBI 功能 SPEC**；描述 Agent 协作、上下文消费、推广顺序与实验闸口。

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| [`SPEC-Governance-Harness-Theory-Align-P0-v1.md`](./SPEC-Governance-Harness-Theory-Align-P0-v1.md) | **`done` · P0 最高** | 培训理论 vs 落地 · 任务单/AGENTS/22/50（**压过业务队列**） |
| [`SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md`](./SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md) | **`done` · #94** | OpenSpec 写法 × TDD 纪律 · validate/22/40/status · RECENT **§0.6** |
| [`SPEC-Governance-Harness-Chain-Orchestration-v1.md`](./SPEC-Governance-Harness-Chain-Orchestration-v1.md) | `draft` | **链式编排常模** · `orchestration` 字段 · semi_auto 退场 · Epic A 轨 |
| [`SPEC-Governance-Harness-Theory-Align-P1-v1.md`](./SPEC-Governance-Harness-Theory-Align-P1-v1.md) | `active`（依赖 P0） | Fresh Context、半自动推广、首条领域 Linter |
| [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) | `active` | **整体安排表**（T0～T4、Wiki-CTX-AB P1/P2） |
| [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) | `active` | **T4** Wiki `graph_nodes` ↔ L0 / `graph_query` 桥接 · `GOV-T4-SPEC-ACTIVE@2026-05-27` |
| [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) | `draft` | **L2 工具链** 锚点 + `_test_manifest`（≠ `coding_wiki/` L2 层） |
| [`SPEC-Governance-TechGraph-Anchor-SQLGate-Backlog-v1_zh.md`](./SPEC-Governance-TechGraph-Anchor-SQLGate-Backlog-v1_zh.md) | `draft` | **图谱 backlog** SQL 闸对齐 + 锚点校验 v1 · P0～P2 选择性抽空实施 |
| [`SPEC-Governance-PR-Post-CI-v1.md`](./SPEC-Governance-PR-Post-CI-v1.md) | `active` | PR 后 CI 更新 body + Mergify 条件 automerge（方案 C） |
| [`SPEC-Governance-Wiki-Frontend-Parity-v1.md`](./SPEC-Governance-Wiki-Frontend-Parity-v1.md) | `active` | **P1-4** 前端 Harness parity · **当前推广主棒** |
| [`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](./SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md) | `active` | **P2 后续** 三 round Loop 编排 |
| [`SPEC-Governance-Wiki-Agent-Readorder-v1.md`](./SPEC-Governance-Wiki-Agent-Readorder-v1.md) | `active` | 后端 Agent Coding Wiki 读序 |
| [`SPEC-Governance-Wiki-Ingest-Batch-v1.md`](./SPEC-Governance-Wiki-Ingest-Batch-v1.md) | `active` | Batch-1 ingest（10 slug） |
| [`SPEC-Governance-Wiki-CTX-AB-Representative-v1.md`](./SPEC-Governance-Wiki-CTX-AB-Representative-v1.md) | `active` | AB 代表性扩面 |
| [`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](./SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) | `active` | Portfolio 演示站 RAG 同源 ingest + 五问验收 RUNBOOK · `PORTFOLIO-RAG-DEMO@2026-06-01` |
| [`PROMPT_00_SPEC-refine_Portfolio-RAG-Demo-v1_zh.md`](./PROMPT_00_SPEC-refine_Portfolio-RAG-Demo-v1_zh.md) | `active` | 上述 SPEC · ≤5 轮读问解 · §4 可复制 Prompt |
| [`docs-noise-inventory/`](./docs-noise-inventory/README.md) | `draft` | **docs/ 噪音治理** · **只读导图** · 正文 SPEC 按需 · `GOV-DOCS-NOISE-INVENTORY@2026-06-06` |

---

## 按主题分组速查（P3 新增）

| 主题 | 文件 | 状态 | 说明 |
| --- | --- | --- | --- |
| **Harness 核心** | [`SPEC-Governance-Harness-Theory-Align-P0-v1.md`](./SPEC-Governance-Harness-Theory-Align-P0-v1.md) | **`done`** | 培训理论 vs 落地 · 压过业务队列 |
| | [`SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md`](./SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md) | **`done`** | OpenSpec 写法 × TDD 纪律 |
| | [`SPEC-Governance-Harness-Chain-Orchestration-v1.md`](./SPEC-Governance-Harness-Chain-Orchestration-v1.md) | `draft` | 链式编排 · semi_auto 退场 |
| | [`SPEC-Governance-Harness-Theory-Align-P1-v1.md`](./SPEC-Governance-Harness-Theory-Align-P1-v1.md) | `active` | Fresh Context、半自动推广 |
| | [`SPEC-Governance-PR-Post-CI-v1.md`](./SPEC-Governance-PR-Post-CI-v1.md) | `active` | PR 后 CI + Mergify automerge |
| **Wiki 批次** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) | `active` | 整体安排表（T0～T4） |
| | [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) | `active` | T4 Wiki ↔ L0 桥接 |
| | [`SPEC-Governance-Wiki-Frontend-Parity-v1.md`](./SPEC-Governance-Wiki-Frontend-Parity-v1.md) | `active` | P1-4 前端 Harness parity |
| | [`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](./SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md) | `active` | P2 后续三 round Loop |
| | [`SPEC-Governance-Wiki-Agent-Readorder-v1.md`](./SPEC-Governance-Wiki-Agent-Readorder-v1.md) | `active` | 后端 Agent Coding Wiki 读序 |
| | [`SPEC-Governance-Wiki-Ingest-Batch-v1.md`](./SPEC-Governance-Wiki-Ingest-Batch-v1.md) | `active` | Batch-1 ingest（10 slug） |
| | [`SPEC-Governance-Wiki-CTX-AB-Representative-v1.md`](./SPEC-Governance-Wiki-CTX-AB-Representative-v1.md) | `active` | AB 代表性扩面 |
| | [`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](./SPEC-Governance-Wiki-Unit-AB-Plan-v1.md) | `active` | Unit AB 计划 |
| **L2 工具链 / Backlog** | [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) | `draft` | L2 工具链锚点 + `_test_manifest` |
| | [`SPEC-Governance-TechGraph-Anchor-SQLGate-Backlog-v1_zh.md`](./SPEC-Governance-TechGraph-Anchor-SQLGate-Backlog-v1_zh.md) | `draft` | 图谱 backlog SQL 闸对齐 |
| **Portfolio / 其他** | [`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](./SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) | `active` | 演示站 RAG 同源 ingest + RUNBOOK |
| | [`PROMPT_00_SPEC-refine_Portfolio-RAG-Demo-v1_zh.md`](./PROMPT_00_SPEC-refine_Portfolio-RAG-Demo-v1_zh.md) | `active` | 上述 SPEC · ≤5 轮读问解 Prompt |
| | [`投递冲刺_20260609_v1_zh.md`](./%E6%8A%95%E9%80%92%E5%86%B2%E5%88%BA_20260609_v1_zh.md) | `active` | 投递冲刺规划 |
| **docs-noise 治理线** | [`docs-noise-inventory/README.md`](./docs-noise-inventory/README.md) | `draft` | docs/ 噪音治理 · 只读导图 · `GOV-DOCS-NOISE-INVENTORY@2026-06-06` |

**分目录约定（2026-06-06 起）**：新增或多文件治理线优先 **`governance/<topic>/README.md`（导图）+ 正文 SPEC**；`governance/` 根 **仅** 保留单页短 SPEC 或历史 flat 文件，逐步迁入子目录。

**SDD 起草**（全仓 SPEC 通用）：[`../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md)

**实验落盘**（非 SPEC 正文）：[`../../harness/experiments/wiki_ctx_ab_v1/`](../../harness/experiments/wiki_ctx_ab_v1/README.md)

**工作区对照稿**：`Projects/docs/harness/guides/COMPARISON_tech_graph_coding_wiki_graph_memory_v1_zh.md`
