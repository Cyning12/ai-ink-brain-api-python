# Wiki Loop · T4 + L2 工具链（第四轮 · 真实业务）

> **目的**：落地治理 Roadmap **P2** — Wiki `graph_nodes` 桥接（T4）+ `_test_manifest`（L2）；**非** Harness 烟雾 Loop。  
> **分支**：`task/gov-spec-t4-l2-v1` · **单 PR** · **docs-only**（R3 仅增 `_test_manifest.json`）

## 流程（三选一）

| 步骤 | 文件 |
|------|------|
| **A · Batch-10（一次）** | [`PROMPT_BATCH_10_t4_l2_v1.md`](./PROMPT_BATCH_10_t4_l2_v1.md)（**已执行** · 见 [`invoke_20260527_10_batch_t4_l2_v1.md`](./invoke_20260527_10_batch_t4_l2_v1.md)） |
| **B · 全链（推荐）** | [`PROMPT_START_loop_t4_l2_full_chain_v1.md`](./PROMPT_START_loop_t4_l2_full_chain_v1.md) · 人批 `HG-LOOP-BATCH` 后粘贴 §3 |
| **C · 断点** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) + [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) |

## Round 主题

| round | 主题 | 关键交付 |
|-------|------|----------|
| **R1** | T4 Pilot | `query-rewrite-observability` · `graph_nodes` · `CODING_WIKI` · RECENT in_progress |
| **R2** | T4 L0 | `99_spec` Wiki 桥接小节 · VERIFY |
| **R3** | L2 manifest | `_test_manifest.json` · RECENT **done** · `reinspect_gov-l2-r3-test-manifest_20260527_v1.md` |
| **META** | 母关账 | CLOSE_TRACE · `REPORT_completion_*` |

## 完成汇报

[`REPORT_completion_20260527_v1.md`](./REPORT_completion_20260527_v1.md)（META 关账后 · §1～§5 落盘）

**验收说明（META 回填 · 2026-05-27）**：本 Loop **主验收** = T4 Pilot（`graph_nodes`）+ T4 L0 VERIFY 对齐 + L2 `_test_manifest` 草案 + invoke C2 全绿（22/30/40/50/CLOSE · §3 ≥15 行 · 元信息含 `task_slug`）。第四轮真实业务 Loop · 单 PR `task/gov-spec-t4-l2-v1` · 3 round：R1 T4 Pilot → R2 T4 L0 → R3 L2 manifest。

## SPEC 真值

- [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../../../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md)  
- [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../../../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md)

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：Batch-10 落盘 · 3 round T4→L2 + MANIFEST / PROMPT_START / PROMPT_LOOP |
| 2026-05-27 | hygiene：reinspect 文件名修正 + README 验收说明 + RECENT §6.6/§8 同步 |
