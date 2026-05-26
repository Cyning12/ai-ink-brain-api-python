# Wiki Loop · B-Q3 Recheck（第二次 Loop 试点）

> **目的**：验证 [`SKILL-harness-loop-batch`](../../../tasks/skills/SKILL-harness-loop-batch.md) 第二 Loop；闭环 Multi slug B **B-Q3**（A1 已补 ingest，原 W 载荷仍 stale）。  
> **分支**：`task/wiki-loop-bq3-recheck-v1` · **单 PR**

## 流程（三选一）

| 步骤 | 文件 |
|------|------|
| **A · Batch-10（一次）** | [`PROMPT_BATCH_10_bq3_recheck_v1.md`](./PROMPT_BATCH_10_bq3_recheck_v1.md) |
| **B · 全链（推荐）** | [`PROMPT_START_loop_bq3_full_chain_v1.md`](./PROMPT_START_loop_bq3_full_chain_v1.md) · 人批 `HG-LOOP-BATCH` 后粘贴 §3 |
| **C · 断点** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) + [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) |

## 与 Loop A1–A4 关系

| 项 | A1–A4（done） | 本 Loop |
|----|---------------|---------|
| 主题 | ingest 纪律 + SPEC/排期 | **实验复检** B-Q3 + 治理收口 |
| 子 round 数 | 4（A1–A4） | 3（R1–R3） |
| 改 scorecard 主表 | 否 | 否 · 仅 **§Recheck** addendum |

## invoke C2（第三批）

换帽前自检见 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) 步骤 1–5 · [`SKILL-harness-loop-batch`](../../../tasks/skills/SKILL-harness-loop-batch.md) §invoke 质量门禁。

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1：Batch-10 起草 · 扫描 SPEC/对比表/RECENT 合并为 R1–R3 |
| 2026-05-26 | 第三批：PROMPT_LOOP / PROMPT_START invoke C2 联动 |
