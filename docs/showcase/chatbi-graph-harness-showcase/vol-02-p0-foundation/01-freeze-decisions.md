---
title: "冻结决策 D-1～D-5"
slug: vol-02-01-freeze
series: chatbi-graph-harness-showcase
vol: "02"
chapter: "01"
status: compiled
---

# 01 · 冻结决策

> **真值**：[`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](../../../spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §4.3  
> **task §10**：2026-06-03 人确认 · Q-8 等已写入 task

---

## 1. 为什么先冻结再写代码

P0 不是「把 LangGraph 搬进来」，而是 **在不动 Legacy Unified 的前提下**，为 Graph 版 Agent 预留 **模块边界 + HTTP 骨架 + 可测边表**。若路由 path、State 路径、SSE 策略在 30 帽边写边猜，会导致：

- `_manifest` / drift_check 与实现双轨漂移
- 50 无法对照 Delta Scenario
- 前端/BFF 联调契约反复改

因此 **10 帽按 22 R1 回填 §10**，人签 `HG-TASK-DRAFT` 后再开 30。

---

## 2. D-1～D-5 摘要（P0 口径）

| ID | 决策 | P0 落地 | 非 P0（路线图） |
| --- | --- | --- | --- |
| **D-1** | **自研** StateGraph，不引 `langgraph` | `api/graph/state.py` + `runner.py` stub | P1 真实节点环 |
| **D-2** | **并行** Graph 新路由；**不改** Legacy Unified | `unified_chat.py` **0 行 diff** | P1 Graph 真实编排 |
| **D-3** | Graph 不接入 V1 规则路由；Intent 超时 **方案 A** | 边表：`graph→direct_answer` · `legacy→intent_v1_fallback` | Q-7 SSE `ok` 语义 defer P1 |
| **D-4** | 前端控展示；后端 Graph 路由 **常开** | 仅注册 Q-8 端点；**无** Ink 改动 | P1 BFF 选路 |
| **D-5** | Graph SSE 可为 **superset** | **P0 不新增** `graph.*` type；stub 复用现有 chain/done | P1 parity 事件 |

D-5 长期与 P0 的区分：调研 SPEC 允许 Graph 路径扩展 SSE；**本 Loop task 明确 P0 不新增 `graph.*`**（task 非范围 · §10 项 3 选 A）。

---

## 3. Q-8 · Graph 路由（已冻结）

| 端点 | 方法 | P0 行为 |
| --- | --- | --- |
| `/api/py/unified/chat/graph` | POST | HTTP 200 · JSON stub（`ok` · `graph_stub` · `run_id`） |
| `/api/py/unified/chat/graph/stream` | POST | HTTP 200 · SSE 心跳（chain + done · 含 `graph_stub`） |

与 [`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../../../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) §5.5 一致；须同步 `_manifest.json` + drift 叙述层（见 vol-02-06）。

---

## 4. task §10 冻结清单（节选）

| # | 决策点 | 选定 |
| --- | --- | --- |
| **Q-8** | Graph path | **A** · 上表两 POST |
| **Q-7** | Intent 超时 SSE `ok` | **defer P1 Task-B** |
| 3 | P0 新增 `graph.*` SSE | **A** · 不新增 |
| 4 | `ChatBIState` 路径 | **A** · `api/graph/state.py` |
| 5 | stub 最小契约 | **A** · 200 + 最小 JSON/SSE |

**均已人确认 · 2026-06-03**（`ab4ca03` 人签 human_gate）。

---

## 5. 与 vol-01 的决策链

P0 **50 复检**发现 main 同 **10× v3 plan 红 + contract `label` 红** → 维护者选 **方案 B**：**不**在 P0 PR 修基线 → 单独 vol-01 task → **#106 先合** → rebase P0 → **#107 合**。

若无此冻结顺序，Agent 易在 P0 diff 中「顺手改 conftest」，破坏 **Delta 可审计性**。

---

## 指针

- task 全文：`docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` §10
- 22 R2（零阻塞开 30）：`docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md`
