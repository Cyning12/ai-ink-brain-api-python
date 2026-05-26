# Wiki Loop · C2 Verify（第三次 Loop 试点）

> **目的**：验证 [`SKILL-harness-loop-batch`](../../../tasks/skills/SKILL-harness-loop-batch.md) **invoke C2 质量门禁**全绿；**非**重跑 B-Q3 业务。  
> **分支**：`task/wiki-loop-c2-verify-v1` · **单 PR** · **docs-only**

## 流程（三选一）

| 步骤 | 文件 |
|------|------|
| **A · Batch-10（一次）** | [`PROMPT_BATCH_10_c2_verify_v1.md`](./PROMPT_BATCH_10_c2_verify_v1.md) |
| **B · 全链（推荐）** | [`PROMPT_START_loop_c2_verify_full_chain_v1.md`](./PROMPT_START_loop_c2_verify_full_chain_v1.md) · 人批 `HG-LOOP-BATCH` 后粘贴 §3 |
| **C · 断点** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) + [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) |

## 与前置 Loop 关系

| 项 | B-Q3 Recheck（done） | 本 Loop |
|----|----------------------|---------|
| 主题 | 实验复检 B-Q3 + 治理收口 | **invoke C2 质量验证**（docs 烟雾） |
| 子 round 数 | 3（R1–R3） | 2（R1–R2） |
| meta-reinspect | **C2 FAIL**（R2/R3 stub） | 目标 **C2 全绿** |

## invoke C2（第三批 · 本 Loop 主验收）

换帽前自检见 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) 步骤 1–5 · [`SKILL-harness-loop-batch`](../../../tasks/skills/SKILL-harness-loop-batch.md) §invoke 质量门禁。

**验收说明（关账后回填）**：第三 Loop 完成后，meta-reinspect 或 SKILL 晋升须抽检 R1/R2 全部 30/40/50 invoke **§3 ≥15 行** · 非 stub。

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1：Batch-10 起草 · 2 round docs 烟雾 + C2 Verify |
| 2026-05-26 | 第三批：PROMPT_LOOP / PROMPT_START invoke C2 联动 |
