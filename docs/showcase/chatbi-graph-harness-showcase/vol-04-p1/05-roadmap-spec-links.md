---
title: "P1 路线图索引"
slug: vol-04-05-roadmap
series: chatbi-graph-harness-showcase
vol: "04"
chapter: "05"
status: compiled
planning_only: true
---

# 05 · 路线图 §5 索引

> L0 真值：[`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../../../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md)  
> 本页为 **L2 摘编 + 开工指针** · 冲突以 SPEC 为准。

---

## 1. §5.1 Structured Output / Parser

| 项 | 内容 |
| --- | --- |
| **吸收** | Intent、SQL JSON → Pydantic/dataclass |
| **失败映射** | `INTENT_PARSE_FAIL` · `SQL_GEN_SYNTAX` 等 `error_code` |
| **范围** | Graph **先上** · parity 后可回灌 `intent_agent.py` |
| **前端** | 否 |
| **P1 验收锚点** | 解析失败走边表 · 专测可 mock LLM 坏 JSON |

---

## 2. §5.2 RunnableConfig 式上下文

| 项 | 内容 |
| --- | --- |
| **吸收** | State 显式 `run_id` · `session_id` · `principal` |
| **目的** | 减 `chatbi_request_ctx` 隐式依赖 · 利于单测 |
| **范围** | Graph 全链 + persist 节点 |
| **前端** | 请求体字段与 Legacy **一致** |

---

## 3. §5.3 Router 单一决策点

| 项 | 内容 |
| --- | --- |
| **吸收** | Graph 内单节点 `intent_decide` + **条件边** |
| **拓扑** | `clarify_gate` · `tool_*` · `plan_preview` · `tool_direct`（D-3 方案 A） |
| **范围** | **仅 Graph** · handler 不堆 if-else |
| **前端** | **契约** — `router.decision` parity |

---

## 4. §5.4 Tool schema

| 项 | 内容 |
| --- | --- |
| **吸收** | `ToolRegistry` → Intent system 工具说明自动生成 |
| **范围** | Graph + Legacy **共用** registry |
| **前端** | 否 |
| **与 Intent Hints** | hints 改 **消费侧** · schema 仍 registry 真值 |

---

## 5. §5.5 交付物清单（Task-B）

| 交付物 | 说明 | 前端 | P0 对照 |
| --- | --- | :---: | --- |
| 新路由 | Q-8 两 POST（已定名） | 联调 | P0 stub ✅ |
| StateGraph MVP | intent→tool 环 + Failure 边表 | 否 | P0 边表结构 only |
| SSE | parity + 可选 `graph.*` | 契约·可选 | P0 最小 stub 事件 |
| Intent 超时 A | 单测 + contract | 契约 | P0 defer Q-7 |
| 共享模块 | 复用 P0 抽取层 | 否 | 已存在 |
| BFF 转发 | Ink 代理 graph* | 联调 | P0 无 |

---

## 6. Task 拆分（§10.2）

| Task ID | 主题 | 依赖 | 本仓/跨仓 |
| --- | --- | --- | --- |
| **Task-B** | Graph MVP 后端 | **Task-P0 done** | 本仓 |
| **Task-B-FE** | BFF + dev 入口 | Task-B 可测 | `ai-ink-brain` |
| **Task-C** | HITL + checkpointer | Task-B | P2 · vol-05 |
| **Task-E** | 生产默认 Graph | Task-B/C | P3 · 前端 |

开 Task-B 时复制：§10.1 P0 元信息表 + 本卷 [`02-intent-card-draft.md`](02-intent-card-draft.md)。

---

## 7. 范围矩阵速查（§9）

```text
P1 主战场 = Graph 新路由 + 共享层 intent/tools
P1 不改   = 旧 Unified 行为 · Legacy /chat
P1 可选   = graph.* SSE · BFF 联调
P1 不做   = interrupt · checkpointer · 生产默认 Graph
```

---

## 8. 相关 SPEC 链接

| 文档 | 用途 |
| --- | --- |
| [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](../../../spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §4.3 | D-1～D-5 |
| [`SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../../../spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) | 轮 0 意图卡 |
| [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) | 环境 · 路由 |
| [`vol-03-05-lessons-experience-capture.md`](../vol-03-cross-cutting/05-lessons-experience-capture.md) | P1 开工 checklist |

---

## 指针

- 全表 P0～P3：Roadmap §3 优先级总表
- P2/P3 远景：[`vol-05-roadmap-horizon/`](../vol-05-roadmap-horizon/)
