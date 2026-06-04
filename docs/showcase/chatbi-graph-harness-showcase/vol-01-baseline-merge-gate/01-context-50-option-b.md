---
title: "50 复检选 B 与两 PR 策略"
slug: vol-01-01-context
series: chatbi-graph-harness-showcase
vol: "01"
chapter: "01"
status: compiled
---

# 01 · 背景：50 复检选 B

## 1. 前情：P0 增量本身已通过 50

`chatbi_graph_p0_foundation_v1` 在 **2026-06-03** 完成 30 实现并经 **50 独立复检** 时，结论是 **pass-with-notes**：

- P0 五步（共享层 / State / runner stub / Q-8 路由 / 专测 10/10）与 R2 审查 **一致**
- `api/unified_chat.py` **零 diff**（D-2 成立）
- **但** Strict 合入 main 仍被 **分支与 main 共有的基线红项** 挡住

详见 L1：[`reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md`](../../../tasks/reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md)。

## 2. 两类「基线债」（非 P0 引入）

| 红项 | 表现 | 与 P0 关系 |
| --- | --- | --- |
| **10× v3 pytest** | `test_unified_chat_backend_v2_agent.py` plan/clarify 相关 | main 上已 fail；P0 diff **未改** `unified_chat.py` |
| **contract `label`** | `tech_graph_contract_check` 报前端读 `label` 未声明 | main 上已 fail；与 P0 增扫描源无关 |

50 复检原文：**「若 Required check 须字面全绿 → 不建议合并 P0 PR 直至基线修复」**。

## 3. 维护者决策：选 B

| 选项 | 做法 | 优劣 |
| --- | --- | --- |
| **A** | P0 PR **夹带**修 10 测 + contract | 单 PR 快，但 **违反** P0 非范围（基线债与 Graph 五步混 diff） |
| **B（选定）** | **独立 task** `chatbi_baseline_merge_gate_v1` → **PR #106 先合 main** → P0 **rebase** 再 **PR #107** | 边界清晰；Harness 各走一条 Loop；合并顺序可审计 |

task 元信息 **`blocks: chatbi_graph_p0_foundation_v1`** 即此决策的落盘。

## 4. 两 PR 硬顺序

```text
① PR #106  task/chatbi-baseline-merge-gate-v1  → merge main  (26e1c45)
② rebase   task/chatbi-graph-p0-foundation-v1  on origin/main
③ PR #107  P0 Graph 地基                        → merge main  (f53327a)
```

**禁止** 在 P0 未 rebase 前假设 main 已含基线修复；否则 CI 叙事与 50 结论会对不上。

## 5. 本卷在系列中的位置

| 卷 | PR | 回答的问题 |
| --- | --- | --- |
| **vol-01（本卷）** | #106 | main 为什么必须先绿？修了啥？ |
| vol-02 | #107 | Graph 地基是什么？为何在基线之后？ |

## 指针

- P0 50 选 B 依据：[`reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md`](../../../tasks/reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md) 结论段
- 基线 task：[`task_chatbi_baseline_merge_gate_v1.md`](../../../tasks/active/task_chatbi_baseline_merge_gate_v1.md)
