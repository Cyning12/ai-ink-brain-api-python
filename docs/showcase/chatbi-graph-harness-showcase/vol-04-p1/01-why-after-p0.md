---
title: "P1 为何在 P0 之后"
slug: vol-04-01-why
series: chatbi-graph-harness-showcase
vol: "04"
chapter: "01"
status: compiled
planning_only: true
---

# 01 · 为何 P1 在 P0 之后

> **性质**：规划 narrative · **Task-B 未开工** · 不得写成已交付。  
> **前置**：main 已含 P0（#107）· vol-03 横切（#112）· Intent Hints Step1/2（#109/#111）为 **并行轨**，非 Graph P1 阻塞项。

---

## 1. P0 Done 已有什么

| 能力 | 证据 |
| --- | --- |
| 共享层 | `chatbi_events` · `chatbi_agent_models` · `chatbi_failure` |
| State + 边表 | `api/graph/state.py` · D-3 分表单测 |
| Q-8 路由 | stub JSON/SSE · `_manifest` + drift 索引 |
| Legacy 不动 | `unified_chat.py` **0 行行为 diff**（D-2） |
| 治理 | Harness 两 PR · 287 pytest · 三门 CI 绿 |

详见 [`vol-02-p0-foundation/`](../vol-02-p0-foundation/)。

---

## 2. P0 刻意没有什么（§4A.4）

| 未做 | 原因 |
| --- | --- |
| **intent→tool 真实环** | 避免在单体 `agent.run` 上硬改；P0 只铺边界 |
| **Graph SSE parity** | 无真实节点 → 无 `agent.*` / `router.decision` 真发射 |
| **`graph.*` 新 type** | D-5：P0 不新增；契约登记留 P1 |
| **Ink BFF 选 Graph** | D-4：后端常开 · 前端联调 **后置** |
| **Q-7 Intent 超时 SSE `ok`** | defer **Task-B**（P1）冻结 |

P0 的 `run_graph_stub` **不是**产品能力 — 是 **可测占位 + HTTP 注册**。

---

## 3. P1（Task-B）要补什么

对齐 Roadmap **§5 P1 — Graph MVP**：

| 交付 | 说明 |
| --- | --- |
| **StateGraph MVP** | `intent_decide` → clarify / tool_* / plan / direct（D-3 方案 A） |
| **Runnable 节点** | `(state) → partial_state` + `error_code` 驱动边表 |
| **SSE parity** | Graph 路径发射与 Legacy **同形** `agent.*` · `router.decision` · `done` |
| **可选 `graph.*`** | D-5 superset · contract 登记 · 前端可忽略未知 type |
| **Structured Output / Tool schema** | Intent · SQL 解析 → `error_code`（Graph 先上） |
| **BFF 联调** | `ai-ink-brain` 代理 `/graph*`（**Task-B-FE** · 跨仓） |

**仍不在 P1**：P2 HITL interrupt · checkpointer · subgraph 全量 · 生产默认走 Graph（Task-E）。

---

## 4. 与 D-2 的关系（下一阶段）

```text
P0：Legacy Unified ──不变──► 用户页面仍走 /unified/chat/stream
         │
         └── Graph 路由 ──stub──► 仅 curl/专测

P1：Legacy Unified ──仍不变──► 默认路径照旧（D-2 延续）
         │
         └── Graph 路由 ──MVP──► dev/BFF 可选切 URL · 真实 Timeline 事件
```

**旧 Unified 不调 Graph** 直到产品决策（P3 Task-E）；P1 是 **后端能力就绪 + 联调可选**。

---

## 5. 为何不在 P0 一次性做完

| 理由 | 本系列证据 |
| --- | --- |
| **合并闸** | main 基线债须独立 #106 · Delta 可审计 |
| **Harness 粒度** | `required` + 50 适合 **单 Loop 单 task**（P0 已验证） |
| **契约风险** | SSE parity 牵 `_contract_manifest` · 前端 Timeline — 独立 Loop 便于 50 对照 |
| **agent.py 策略** | 路线图：**先抽模块（P0）→ Graph 接棒（P1）→ parity 后 run 变壳（P2）** |

---

## 6. 与 Intent Hints 的关系（并行 · 非阻塞）

main 上 **Intent Hints Step1/2**（#109/#111）增强 **Legacy 路径** 的 hints / router / Timeline 可观测性。

| 项 | Graph P1 |
| --- | --- |
| 共用 registry / `intent_agent` | P1 Tool schema 与 **同一** `ToolRegistry` |
| 阻塞 Graph P1？ | **否** — Task-B 依赖 **Task-P0 done**，不依赖 hints Epic 关账 |
| 展示系列 | hints 无独立 vol；见 `docs/spec/intent-hints/` |

---

## 指针

- Roadmap §4A.4 · §5：[`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../../../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md)
- P0 案例：[`vol-02`](../vol-02-p0-foundation/)
- 开工前横切：[`vol-03`](../vol-03-cross-cutting/)
