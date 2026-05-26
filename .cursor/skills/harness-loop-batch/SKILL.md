---
name: harness-loop-batch
description: >-
  Harness Loop Batch: Batch-10 once, then 22→30→40→50→close per round (R1…Rn+META)
  via LOOP_MANIFEST and single PR. Cross-round semi_auto authorized once in
  PROMPT_START_<loop-slug>_full_chain, not in PROMPT_LOOP template. Use when planning
  or executing multi-subtask Harness loops, wiki-loop, wiki-loop-a1-a4, HG-LOOP-BATCH,
  LOOP_MANIFEST, or PROMPT_BATCH_10. Body uses <loop-slug>; wiki-loop-a1-a4 is pilot only.
disable-model-invocation: true
---

# Harness Loop Batch（母单 + 多子 task · 单 PR）

> **便携真值**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../../../docs/tasks/skills/SKILL-harness-loop-batch.md)  
> **试点实例**：[`docs/harness/invokes/by-task/wiki-loop-a1-a4/`](../../../docs/harness/invokes/by-task/wiki-loop-a1-a4/)（A1–A4 = R1–R4 示例）

## 何时使用

- 10 帽 **Batch 一次** → **N** 个子 task；执行 **禁止再开 10**
- round：**R1…Rn + META**（非固定 4 轮）
- 全链：人贴 **一次** `PROMPT_START_<loop-slug>_full_chain`（含 cross-round【授权】）

## 硬约束

1. **【授权】** 只放在 `PROMPT_START_<loop-slug>_full_chain_v1.md`，**不**写入 `PROMPT_LOOP` §3
2. 每帽：**invoke §3 全文 + commit** 后再换帽
3. 新 Loop：复制 `invokes/by-task/<loop-slug>/`，模式名见 SKILL 工件表
4. 排期/RECENT：**母 task 明示**哪 round 改；非全局定律

## 流程（三选一）

- **A** Batch 一次（必做）
- **B** 全链一次 + cross-round（推荐；可单会话 R1→META）
- **C** 断点续跑（PROMPT_LOOP + MANIFEST）

## 可选

- [`harness-meta-reinspect`](../../harness-meta-reinspect/SKILL.md) — META/PR 后流程元复检

## 状态

SKILL **`draft`** — 未第二次 Loop 验证前不宜标 accepted
