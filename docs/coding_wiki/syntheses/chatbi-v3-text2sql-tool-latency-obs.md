---
title: ChatBI V3 Text2SQL 工具链延迟与可观测性
slug: chatbi-v3-text2sql-tool-latency-obs
layer: L2
source_task: docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md
freeze_id: CHATBI-V3-TEXT2SQL-OBS@2026-05-11
closed_date: 2026-05-11
status: compiled
graph_nodes:
  - id: T2S
    relation: documents
    note: Text2SQL 子流程 · SSE 子阶段延迟与可观测性（T4 扩面）
  - id: SSE
    relation: triggers
    note: SSE 流式输出 · text2sql.phase.* 子阶段触发
  - id: U2
    relation: documents
    note: Unified SSE 契约 · X-ChatBI-Sse-Contract
---

# ChatBI V3 Text2SQL 工具链延迟与可观测性

## 摘要

多轮 Agent 路径下 `text2sql_execute` 原整段 `tool.call` 墙时过长。交付 **SSE 子阶段**（`text2sql.phase.*`）、**`text2sql_phases_ms`** 结构化分段、分阶段 LLM **timeout**、**JSON 日志**（`request_id`/`run_id`）与可判定聚合的 **确定性总结**（减第二次 `llm_summarize`）。

## 决策要点（拍板摘录）

- **P0-1+3** 可先中间验收，**P0-2** 日志 Trace 后再宣称总规 P0 最终完成。  
- **P95 可归因**：P0 **不要求**现网 metrics；pytest + 单次 JSON 日志人工对齐 `run_id`。  
- 契约：`X-ChatBI-Sse-Contract`、`_contract_manifest.json` 与代码同批。

## 测试变更

| 动作 | 路径 / 说明 |
|------|-------------|
| **新增/强化** | `tests/test_chatbi_json_log.py` — `CHATBI_JSON_LOG`、`text2sql_phases_ms`、`subphase_id` 等（P0-2 日志贯通；细节见 L1 实现备忘） |
| **阶段 A 验收** | pytest + SSE/`ToolResult` 上 `text2sql_phases_ms`（L1 §验收 A 项） |
| **阶段 B 验收** | 同上 + JSON 日志与 `run_id` 对齐（L1 §验收 B 项） |
| **未在 Wiki 记录** | 全仓 ChatBI 用例枚举；coverage 数字 |

**失败/超时语义**：`LLM_API_TIMEOUT` + 可选 `detail.phase` = `llm_sql` / `llm_summary`（→ L1 §拍板 #5）。

**图谱**：→ `docs/_tech_graph/11_flow_text2sql.md` / `.ai.md`（L1 要求与实现一致）。
**T4**：frontmatter `graph_nodes`（T2S/SSE/U2）· 读序见 [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) §4.1。

**RUNBOOK**：→ `docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md`（流程细则，禁止复制全文）。

## 相关

- [[../concepts/test-strategy-ink-backend]]  
- [[../decisions/2026-05-26-unit-first-test-archive]]
