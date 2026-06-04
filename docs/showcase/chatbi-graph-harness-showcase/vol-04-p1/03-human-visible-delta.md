---
title: "P1 人类可见变化预览"
slug: vol-04-03-visible
series: chatbi-graph-harness-showcase
vol: "04"
chapter: "03"
status: planned
---

# 03 · P1 完成后人类可见变化（预览）

## 大纲（待编写）

### 预计将感受到

- [ ] Graph 路由返回 **真实** Agent 事件（非 stub）
- [ ] SSE 与现有 `agent.*` / `router.decision` **parity**
- [ ] （可选）Ink BFF 转发 `/graph*`

### 仍可能感受不到

- [ ] 旧 Unified 页面默认仍走 legacy 路径
- [ ] P2 级 HITL 完整环

## 对比 vol-02-05

| 项 | P0 | P1（预期） |
| --- | --- | --- |
| Graph JSON | stub | MVP 载荷 |
| Timeline | 无新 type | parity / 可选 graph.* |
