---
title: "Vol-04 · P1 Graph MVP"
slug: vol-04-p1
series: chatbi-graph-harness-showcase
vol: "04"
status: compiled
planning_only: true
layer: L2-showcase
---

# Vol-04 · P1 Graph MVP（规划 narrative）

> **重要**：本卷为 **Task-B 开工前** 的 L2 规划稿 · **`planning_only: true`** · **实现未开工**。  
> 不得将下文写成已 merge 行为；开工后以 `docs/tasks/active/task_chatbi_graph_p1_*.md` + reinspect 为 L1 真值。

## 依赖（已满足）

| 依赖 | 状态 |
| --- | --- |
| P0 地基 #107 | main ✅ |
| vol-03 横切 #112 | main ✅ |
| 基线闸 #106 | main ✅ |
| Roadmap §5 | SPEC ✅ |

## 本卷章节

| # | 文件 | 用途 | 状态 |
| ---: | --- | --- | --- |
| 01 | [01-why-after-p0.md](01-why-after-p0.md) | 为何 P1 · P0 已/未交付 | 已完成 |
| 02 | [02-intent-card-draft.md](02-intent-card-draft.md) | 轮 0 意图卡草案 | 已完成 |
| 03 | [03-human-visible-delta.md](03-human-visible-delta.md) | 人类可见变化预览 | 已完成 |
| 04 | [04-harness-path-preview.md](04-harness-path-preview.md) | 预计帽链 · 跨仓 | 已完成 |
| 05 | [05-roadmap-spec-links.md](05-roadmap-spec-links.md) | §5.1～5.5 索引 | 待编写 |
| 06 | `06-evidence-index.md` | PR · 证据 | **Task-B 关账后** |

## 建议读序

1. **01** 为何 P1 → **02** 意图卡  
2. **05** 路线图索引 → **04** Harness 预览  
3. **03** 人类可见边界 → 开工写 task

## 下一步（真实开工）

- [ ] `docs/tasks/active/task_chatbi_graph_p1_mvp_v1.md`（slug 可微调）
- [ ] 00 帽冻结本卷 02 → 人签 gate → 30
- [ ] 本卷 `planning_only` 移除 · `status` → `in_progress` → `done` + **06**

## 与 vol-90

P1 合入后再增投递短稿 **v0.11+**；当前 vol-90 仍描述 P0+#106/#107 口径。
