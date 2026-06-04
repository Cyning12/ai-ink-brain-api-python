---
title: "30 秒电梯稿"
slug: vol-90-01-elevator
series: chatbi-graph-harness-showcase
vol: "90"
chapter: "01"
status: compiled
draft_version: v0.10
aligned_spec: docs/spec/governance/投递冲刺_20260609_v1_zh.md
---

# 01 · 30 秒电梯稿

> **用途**：开场自我介绍项目亮点 · **≤120 字** 正文 + 口播扩展  
> **边界**：P0 是 **地基 + 治理闭环**，不是「Graph 产品已上线」

---

## 正文（≤120 字 · 可直接粘贴）

main 上 v3 测与契约 CI 已红，阻 Graph P0 合入。Harness 独立基线 task，先 #106 清债再 #107：287 测绿，共享层与 Graph stub 落地，Legacy 零变更；真实 Agent 留 P1。

---

## 口播扩展（约 45 秒 · 面试官追问前）

1. **问题**：P0 50 复检发现「增量 OK、Strict merge 被 main 基线债挡住」— 10 个 plan/clarify 测 + contract `label` 在 main 已红，与 Graph diff 无关。
2. **动作**：维护者选 **方案 B** — 不夹带修复，单独 Harness Loop（10→22→30→40→50）合 #106；P0 rebase 后合 #107；#107 还修了 drift_check（manifest 绿 ≠ 叙述层绿）。
3. **结果**：`287 passed` · 契约/manifest/drift 全绿 · `api/graph/` stub 可 curl · **`unified_chat.py` 0 行 diff**。
4. **下一步（诚实）**：P1 才做 Graph 真实编排与 SSE parity；Ink 页面仍走 Legacy。

---

## 禁讲清单（对齐投递冲刺 §8）

| 禁讲 | 改说 |
| --- | --- |
| ChatBI 多 Agent 平台已成熟 | P0 是 **stub + 模块边界** |
| 维护成本归零 / 全行业数字 | 有 Harness 落盘与 CI，**无** 团队 KPI 数字 |
| Ink 已有 Graph Timeline | **P1 后**；演示用 curl + pytest |

---

## 指针

- 长叙事：[`vol-01`](../vol-01-baseline-merge-gate/) · [`vol-02`](../vol-02-p0-foundation/)
- 证据：[`_meta/EVIDENCE_LINKS.md`](../_meta/EVIDENCE_LINKS.md)
