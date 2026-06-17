# Task · 图谱幽灵节点 `external_ref` schema（Backlog · 可选）

> **状态**：`backlog`（**不阻塞 G0 链** · 按需立项）  
> **schedule_ref**：RECENT **§1.7 链外**  
> **来源**：QNA §已知遗留 · 幽灵节点 · Inform 复查

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | backlog 占位 · 未立项 · 无实现 |

---

## 背景

YAML/graph.json 允许边引用未在 `nodes` 声明的节点（如 AUTH、FTS）。当前无 schema 字段显式标记，易被误判为数据 bug。

**若立项**：在 `graph_v2_schema.md` + YAML 约定 `external_ref` · 逐图标注 · compile/export 校验策略 · **非本阶段必须**。

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| — | — | backlog · 未定义 | 立项后补 |

---

## 建议触发条件

- G0 inventory 将「幽灵节点」列为 **gap** 且维护者签收要做
- 或某 flow 图维护反复踩坑

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-17 | backlog 占位 · 不建 HG-TASK-DRAFT 直至维护者拉 active |
