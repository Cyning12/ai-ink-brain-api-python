---
title: "P1 人类可见变化预览"
slug: vol-04-03-visible
series: chatbi-graph-harness-showcase
vol: "04"
chapter: "03"
status: compiled
planning_only: true
---

# 03 · P1 完成后人类可见变化（预览）

> **性质**：**预期**行为 · Task-B **未交付** · 与 vol-02-05（P0 stub）对照。

---

## 1. 对比表（P0 已交付 vs P1 预期）

| 项 | P0（main 今） | P1（Task-B 后预期） |
| --- | --- | --- |
| Graph JSON | `ok` + `graph_stub` | 含 intent/tool 结构化载荷 |
| Graph SSE | chain/done 心跳 | **真实** `agent.think` · `router.decision` · `tool.*` 等 |
| Ink 默认聊天 | Legacy `/unified/chat/stream` | **仍 Legacy**（除非 dev 切 URL） |
| 回答内容 | stub 无 RAG 真回答 | Graph 路径可走 **真实** RAG/Text2SQL |
| Timeline 新 tab | 无 | dev 联调可见 Graph 事件流 |
| `graph.*` 事件 | 无 | **可选** 新增 · 旧客户端可忽略 |

---

## 2. 预计将感受到（dev / 联调口径）

| # | 谁 | 感受 |
| ---: | --- | --- |
| 1 | **后端开发者** | curl/stream Graph 路由像「真 Chat」而非 stub |
| 2 | **前端联调** | BFF 转发 Graph 后 Timeline 出现与旧路径 **同形** 事件 |
| 3 | **维护者** | P1 专测 + contract 快照锁住 SSE 不回退 |
| 4 | **面试叙事** | 「P0 铺轨，P1 在 Graph 路径跑通 MVP 环，Legacy 零破坏」 |

**不会**自动发生：访客打开 Ink 生产站默认变 Graph — 属 **Task-E / P3**。

---

## 3. 仍可能感受不到

| 项 | 原因 |
| --- | --- |
| 生产 Ink 页面默认回答路径 | D-4 · 无 Task-B-FE 或未切 env |
| clarify/plan **图内 interrupt** | P2 · 仍可能用 token/现有 clarify 语义过渡 |
| 断点续跑 / 刷新恢复图状态 | P2 checkpointer |
| Graph 比 Legacy「更聪明」 | 能力取决于 tool/RAG · 非编排框架本身 |

---

## 4. 与 Intent Hints（#109/#111）的边界

| 能力 | 路径 | 用户可见？ |
| --- | --- | --- |
| Intent hints / 仲裁 / Timeline path 观测 | **Legacy** Unified | 是（Portfolio 相关） |
| Graph StateGraph MVP | **Q-8** `/graph/stream` | 仅联调切 URL 时 |

两者 **共用** intent/registry 概念，但 **不** 把 hints Epic 误说成 Graph P1 已交付。

---

## 5. 演示脚本差异（相对 vol-90-03）

| 步骤 | P0 演示 | P1 演示（预期） |
| --- | --- | --- |
| curl Graph | 看 `graph_stub: true` | 看 event stream 含 `router.decision` |
| pytest | `test_chatbi_graph_p0_foundation` 10/10 | + P1 专测 |
| Ink UI | 强调「仍走 Legacy」 | dev 可选展示 Graph Timeline |

---

## 6. 验收口语（禁 overclaim）

**可说**：「Graph 路由上我们跑通了 intent 到 tool 的 MVP 编排，SSE 与旧路径对齐，生产默认仍走 Legacy。」

**禁说**：「ChatBI 已全面切 Graph」「多 Agent 平台已上线」「用户都已用上 Graph 模式」。

---

## 指针

- P0 人类验收：[`vol-02-p0-foundation/05-human-acceptance.md`](../vol-02-p0-foundation/05-human-acceptance.md)
- 投递短稿：[`vol-90-portfolio/`](../vol-90-portfolio/)（P1 后须增 v0.11+）
