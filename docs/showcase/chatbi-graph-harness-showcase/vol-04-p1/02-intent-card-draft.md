---
title: "P1 Intent 卡草案"
slug: vol-04-02-intent
series: chatbi-graph-harness-showcase
vol: "04"
chapter: "02"
status: compiled
planning_only: true
---

# 02 · Intent 卡草案（轮 0 · 开 Task-B 前冻结）

> **模板**：[`SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../../../spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) 轮 0  
> **状态**：**draft** — 00/10 帽开工前须人确认 · **非** L1 task 真值

---

## 1. 完成态一句话

在 **Q-8 Graph 路由**上交付 **自研 StateGraph MVP**：`intent_decide` → clarify / tool / plan / direct 条件边环，**SSE 与 Legacy 核心帧 parity**（`agent.*` · `router.decision` · `done`）；**不修改** `unified_chat.py` 默认行为（D-2）。

---

## 2. 非范围

| 非范围 | 说明 |
| --- | --- |
| P2 **interrupt / checkpointer** | plan/clarify 真 HITL 图暂停 |
| P2 **subgraph** 全量 Text2SQL 内嵌图 |
| **生产** Ink 默认切 Graph | Task-E · D-4 后置 |
| Legacy `/api/py/chat` 整链重写 | 路线图明确排除 |
| Graph 接入 **V1 规则路由** | D-3 已冻结 |
| 引入 `langgraph` / `langchain` 库 | D-1 |
| Intent Hints Step3 Full | 独立 Epic · 不并入本 Loop |

---

## 3. 验收预览（Task-B 开工后勾选）

### 后端（本仓）

- [ ] `POST /api/py/unified/chat/graph/stream` 返回 **真实** intent→tool 事件流（非 `graph_stub`）
- [ ] 核心 SSE type 与 Legacy 路径 **parity**（快照或 contract 测）
- [ ] `error_code` 驱动边表 · 方案 A Intent 超时（`LLM_API_TIMEOUT` → `direct_answer` on Graph 侧）
- [ ] `tests/test_chatbi_graph_p1_*.py`（专测名 TBD）**required** 全绿
- [ ] `pytest` 全集 + `tech_graph_*_check` 仍绿
- [ ] `unified_chat.py` diff **空**（D-2）或 task 明文例外

### 契约 / 图谱

- [ ] 若新增 `graph.*` type → `_contract_manifest.json` + drift 索引
- [ ] `_manifest` 仍含 Q-8 两 path
- [ ] 增量 `10_flow_agent_graph.ai.md`（或等价）指针

### 跨仓（可选 · Task-B-FE）

- [ ] Ink BFF 可转发 Graph stream（local/dev）
- [ ] Timeline **未知 type 可忽略** · 核心帧可渲染

---

## 4. Harness 元信息（建议 · 00 帽填入 task）

| 字段 | 建议值 |
| --- | --- |
| **task_slug** | `chatbi_graph_p1_mvp_v1`（可微调） |
| **test_strategy** | `required` |
| **audit_profile** | `post_close` |
| **semi_auto** | `true`（人确认） |
| **blocks** | —（前置：P0 已 merge · 无基线闸） |
| **freeze_id** | Roadmap §5 + D-1～D-5 · merge `f53327a` 后 SPEC 版本行 |
| **human_gate** | `HG-TASK-DRAFT` · `HG-AUDIT-R1`（与 P0 同节奏） |

---

## 5. 失败路径（预览 · 须 10 帽扩写）

| Scenario ID（草案） | 触发 | 系统行为 |
| --- | --- | --- |
| `fp-p1-graph-sse-parity-drift` | Graph 漏发 `router.decision` | contract_check 或 快照测 fail |
| `fp-p1-legacy-regression` | 误改 `unified_chat` | 全集 v3/Unified 测 fail |
| `fp-p1-intent-timeout-a` | Graph Intent 超时 | 边表 → `direct_answer` · SSE 可观测 |

---

## 6. Delta 预览（MODIFIED / ADDED）

| 类型 | 对象 |
| --- | --- |
| **MODIFIED** | `api/graph/runner.py` stub → MVP 编排 |
| **ADDED** | Graph 节点模块（路径 TBD · 如 `api/graph/nodes/`） |
| **ADDED** | P1 专测 · 可选 SSE 快照 fixture |
| **UNCHANGED** | Legacy Unified 对外行为（D-2） |

---

## 指针

- 可见变化预览：[`03-human-visible-delta.md`](03-human-visible-delta.md)
- Harness 帽链：[`04-harness-path-preview.md`](04-harness-path-preview.md)
