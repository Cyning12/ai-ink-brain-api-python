---
name: harness-loop-batch
description: >-
  Harness Loop Batch: Batch-10 once, then 22→30→40→50→close per round (R1…Rn+META)
  via LOOP_MANIFEST and single PR. FIRST step: scan human_gate on task (+ mother task
  if inherited); pending blocks all hats—semi_auto and pasted PROMPT do not override.
  Cross-round semi_auto only in PROMPT_START_<loop-slug>_full_chain. Invoke C2 ≥15 lines.
disable-model-invocation: true
---

# Harness Loop Batch（母单 + 多子 task · 单 PR）

> **便携真值**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../../../docs/tasks/skills/SKILL-harness-loop-batch.md)（**v1.9** · 含 **§执行铁律**）  
> **实例 1–4**：[`wiki-loop-a1-a4/`](../../../docs/harness/invokes/by-task/wiki-loop-a1-a4/) · [`wiki-loop-bq3-recheck/`](../../../docs/harness/invokes/by-task/wiki-loop-bq3-recheck/) · [`wiki-loop-c2-verify/`](../../../docs/harness/invokes/by-task/wiki-loop-c2-verify/) · [`wiki-loop-t4-l2/`](../../../docs/harness/invokes/by-task/wiki-loop-t4-l2/) · [`wiki-loop-unit-a/`](../../../docs/harness/invokes/by-task/wiki-loop-unit-a/)

## 何时使用

- 10 帽 **Batch 一次** → **N** 个子 task；执行 **禁止再开 10**
- round：**R1…Rn + META**（非固定 4 轮）
- 全链：人贴 **一次** `PROMPT_START_<loop-slug>_full_chain`（含 cross-round【授权】）

## 硬约束

0. **执行铁律（首步 · 不可跳过）**：开当前 round task → 扫 `human_gate`；子 task「继承母闸」时 **同时** 开 **母 task**，**以母单 status 为准**。任一相关 gate `pending` 且阻塞当前帽 → **硬停**（阻塞版状态栏），**禁止** 22/30/invoke。`semi_auto`、粘贴 Prompt、用户说「执行」**均不免除**。详见便携真值 **§执行铁律**。
1. **【授权】** 只放在 `PROMPT_START_<loop-slug>_full_chain_v1.md`，**不**写入 `PROMPT_LOOP` §3
2. 每帽：**invoke §3 全文（≥15 行 · 含元信息表）+ commit** 后再换帽；R2+ 与 R1 **同标准**，禁止 stub
3. 新 Loop：复制 `invokes/by-task/<loop-slug>/`，模式名见 SKILL 工件表
4. 排期/RECENT：**母 task 明示**哪 round 改；非全局定律
5. **META 关账后**：落盘 `REPORT_completion_*`（§1～§5）；PR 前跑 [`docs-governance`](../docs-governance/SKILL.md) hygiene H1–H6

## 流程（三选一）

- **A** Batch 一次（必做）→ 人批母单 `HG-LOOP-BATCH`（建议单独 commit）
- **B** 全链一次 + cross-round（推荐）→ **Gate 验证通过** 后 R1→META
- **C** 断点续跑（PROMPT_LOOP + MANIFEST）

## 相邻 SKILL

| SKILL | 关系 |
|-------|------|
| [`docs-governance`](../docs-governance/SKILL.md) | 关账后 hygiene H1–H6 |
| [`harness-task`](../harness-task/SKILL.md) | **单 task** 帽链（非 Loop） |
| [`harness-meta-reinspect`](../harness-meta-reinspect/SKILL.md) | META/PR 后流程元复检 |

## 状态

SKILL **`accepted`** · **v1.9**（2026-05-28 执行铁律 + cc 入口修补）· 完整条文见便携真值修订记录
