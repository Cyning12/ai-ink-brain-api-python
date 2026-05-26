---
title: Ink 后端跨 Epic 测试策略（指针）
slug: test-strategy-ink-backend
layer: L2
status: compiled
freeze_id: CODING-WIKI-T1C@2026-05-26
---

# Ink 后端跨 Epic 测试策略（指针）

> **非第二真值**：pytest 文件树、`graph.json`、CI Required 仍以 **代码 + L0/L1** 为准；本页仅汇总 **读序与分工**。

## 分层

| 层 | 测什么 | Agent 何时读 |
|----|--------|--------------|
| **L0** | 流程拓扑、`ERR_*` 节点、契约 manifest | 改接口/SSE/表 → `graph_query` + `_tech_graph/*.ai.md` |
| **L1** | 单 task `failure_paths`、验收命令、`test_strategy` | 执行/关账该 Epic |
| **L2** | 测试 **变更过程**（`syntheses` §测试变更、`decisions/`） | 跨 Epic 理解「为何增删改测」 |

## 本仓惯例（摘要）

- **合并前必绿**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见根 `AGENTS.md` §8）。
- **`test_strategy: required`**：须先有可失败自动化测试再改 `api/`；关账链 **30→40→50**。
- **`test_strategy: not_applicable`**：纯文档 Epic（如 T1c）；**不**因 Wiki 而新增 pytest。
- **ChatBI / Text2SQL**：分阶段验收（中间 vs 最终）见 L1 task 拍板；子阶段可观测性以 **pytest + SSE/JSON 日志 pointer** 验收，**P0 不要求**现网 P95 metrics 管道（→ `task_chatbi_v3_text2sql_tool_latency_obs_v1` §拍板 #4）。
- **RAG 可观测**：metadata 字段契约优先 **单测**；DB/Embedding 失败见 L1 `failure_paths`（→ `task_05_query_rewrite_observability`）。

## Wiki 测试档案读序

1. [[../index]]  
2. 本页 → 相关 [[../syntheses/query-rewrite-observability]] / [[../syntheses/chatbi-v3-text2sql-tool-latency-obs]]  
3. 按需打开 L1 `source_task` 片段  
4. 改代码/拓扑 **必回 L0**

## 相关

- [[llm-wiki-layers]]  
- 决策：[[../decisions/2026-05-26-unit-first-test-archive]]  
- 治理：→ `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` §5.1 P1 T1c
