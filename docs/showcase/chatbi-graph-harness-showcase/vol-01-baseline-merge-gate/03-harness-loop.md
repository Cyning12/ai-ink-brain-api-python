---
title: "Harness 帽链"
slug: vol-01-03-harness
series: chatbi-graph-harness-showcase
vol: "01"
chapter: "03"
status: compiled
---

# 03 · Harness 闭环（基线闸）

> **task_slug**：`chatbi_baseline_merge_gate_v1` · **分支**：`task/chatbi-baseline-merge-gate-v1`  
> **test_strategy**：`required` · **audit_profile**：`post_close`

---

## 1. 帽链总览

```text
10 需求/task 草案
  → 22 R1 审查（文档零阻塞 · 人签闸）
  → 30 执行（conftest · agent · contract）
  → 40 自检（独立复跑 · 回填 task）
  → 50 复检（Fresh Context · reinspect 落盘）
  → PR #106 → merge main
```

**semi_auto: true** — 无 `human_gate` pending 时可链式戴帽；**22 开帽前**须 `HG-TASK-DRAFT` approved。

---

## 2. 各帽落盘与要点

| 帽 | 日期 | 关键产出 | 路径 |
| --- | --- | --- | --- |
| **10** | 06-04 | task 草案 · 50 选 B 背景 | `docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md` |
| **22 R1** | 06-04 | 文档零阻塞；流程闸 pending | `docs/harness/reviews/task_chatbi_baseline_merge_gate_v1_audit_R1_20260604.md` |
| **人签** | 06-04 | HG-TASK-DRAFT + HG-AUDIT-R1 → approved | commit `bbd6ded` · author `cyning` |
| **30** | 06-04 | 业务 fix `eed212e` | `tests/conftest.py` · `api/agent.py` · manifest |
| **40** | 06-04 | 自检表全 pass | task `### 自检结论（执行者）` · `d289fe9` |
| **50** | 06-04 | pass-with-notes | `reinspect_chatbi_baseline_merge_gate_v1_20260604_v1.md` |

Invoke 快照目录：[`docs/harness/invokes/by-task/chatbi_baseline_merge_gate_v1/`](../../../harness/invokes/by-task/chatbi_baseline_merge_gate_v1/)

---

## 3. human_gate 追溯（50 强制项）

| gate_id | blocks | 变更 commit | 结论 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | 22-R1, 30 | `bbd6ded` | 人签 · 非 Agent 代填 |
| HG-AUDIT-R1 | 30 | `bbd6ded` | 22 R1 落盘后人签 |

开 30 前须：`python tools/harness_human_gate_check.py --task docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md` → **exit 0**。

---

## 4. 22 R1 与 50 结论对照

| 维度 | 22 R1 | 50 |
| --- | --- | --- |
| task 文档 | 零阻塞 | 验收表逐项 pass |
| 30 开工 | 待闸口 | （已执行） |
| PR CI | — | pass-with-notes：本地绿 · **须** Actions 绿再 merge |
| P0 夹带 | — | F3 pass：无 `api/graph/*` |

22 阻塞项（开帽时）：`HG-TASK-DRAFT` pending → 人签后 30 可开工。详见 R1 审查 md。

---

## 5. AI Coding 可复用点

1. **required + 涉 api/**：关账前 **50 落盘** 非可选（task `test_strategy_note`）。
2. **两 PR 策略**：task `blocks` 字段 + vol-01-01 决策表，避免 Agent 在 P0 PR 里「顺手修基线」。
3. **Fresh Context**：50 只读 task、reviews、40 自检、diff — **不**读 30 invoke 长文（P1 规约）。

横切展开：[`vol-03-cross-cutting/04-agent-playbook.md`](../vol-03-cross-cutting/04-agent-playbook.md)（待填正文时可回链本页）。

---

## 6. Commit 链（本 task · 节选）

```text
a0830bb  10 帽 task + invoke
c51369e  22 R1 审查
bbd6ded  human_gate 人签
eed212e  fix(chatbi) 基线闸实现
d289fe9  40 自检
c04e481  50 复检
→ merge main 26e1c45 (#106)
```

完整索引：[`06-evidence-index.md`](06-evidence-index.md)
