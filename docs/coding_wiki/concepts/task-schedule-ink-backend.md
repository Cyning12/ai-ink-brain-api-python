---
title: 任务排期导航（L1 RECENT + L2 Wiki + L0 图谱）
slug: task-schedule-ink-backend
layer: L2
status: compiled
graph_nodes: []
---

# 任务排期导航

纯叙事 · **排期 hub**；**不**复制 `RECENT_TASK_SCHEDULE.md` 全文。排期真值仍以 L1 为准。

## 三层分工（防孤岛）

| 层 | 载体 | 管什么 | 不管什么 |
|----|------|--------|----------|
| **L1** | [`RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md) · `active/` / `done/` task | **当前棒**、状态、Harness 关账 | 技术拓扑 |
| **L2** | 本页 · `index.md` · `syntheses/`（**done** Epic） | 跨 Epic 导航、关账摘要、读序 | 进行中 task 全文 |
| **L0** | `graph_query` · `_manifest` | 改 `api/` 时的影响面 | 任务先后依赖 DAG |

**任务先后** → RECENT + task 头 `schedule_ref` / `blocked_by` / `blocks`。  
**技术依赖** → L0 `graph_query`（synthesis 的 `graph_nodes` 仅作种子）。

## Agent 读序（规划 / 开工前）

1. 本页或 [`RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md) §0 · §1.1  
2. 打开 1～3 个 `docs/tasks/active/task_*.md`  
3. 若改接口/表/RPC → `python tools/tech_graph_graph_query.py` + `_manifest.json`  
4. 若关账回顾 → [`index.md`](../index.md) → `syntheses/<slug>.md` → pointer L1 done task  

**禁止**：仅读本 Wiki 页推断排期或改 `api/`；与 RECENT 矛盾时 **L1 为准**。

---

## Epic 分区（2026-05-29 快照）

### ChatBI V3 · P2 韧性 — **当前 Loop（单 PR）**

| RECENT | task | 状态 | 说明 |
|--------|------|------|------|
| §1.1 **#L1** | [`task_chatbi_v3_p2_resilience_loop_v1.md`](../../tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md) | `in_progress` | **母单** · `task/chatbi-v3-p2-loop-v1` |
| §1.1 L1-R1 | [`task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md`](../../tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md) | `todo` | 归档 #0b/#W1（#86/#87 已合） |
| §1.1 #0c | [`task_chatbi_v3_p2_resilience_circuit_breaker_v1.md`](../../tasks/active/task_chatbi_v3_p2_resilience_circuit_breaker_v1.md) | `todo` | **Loop R2** 熔断 |
| invoke | [`chatbi-v3-p2-loop/`](../../harness/invokes/by-task/chatbi-v3-p2-loop/) | — | PROMPT_START · MANIFEST |

**已合 main、待 R1 归档**：P2-1b（#86）· W1（#87）

**母单 / 已关账**：→ [[../syntheses/chatbi-v3-p2-health-ready]]（P2-1a）· [[../syntheses/chatbi-v3-text2sql-tool-latency-obs]]

**图谱种子（改 ChatBI 路径时）**：`T2S` · `SSE` · `U2`

### ChatBI V3 · 队列（非本 Loop）

| task | 状态 |
|------|------|
| [`task_chatbi_v3_planning_after_resume_v1.md`](../../tasks/active/task_chatbi_v3_planning_after_resume_v1.md) | `planning` |
| 低置信 / 多轮欠债 / Intent | `backlog` · P2–P4 |

### RAG / 探索

| task | 状态 |
|------|------|
| [`task_rag_graphrag_pilot_explore_v1.md`](../../tasks/active/task_rag_graphrag_pilot_explore_v1.md) | 按需 |

### 治理 · Wiki / Harness（**已收口**）

| 里程碑 | pointer |
|--------|---------|
| T4 ops + lint | [[../syntheses/governance-wiki-t4-expand]] |
| Wiki 验收留证 | [`docs/diary/2026-05-29-wiki-milestone-acceptance.md`](../../diary/2026-05-29-wiki-milestone-acceptance.md) |

**可选后续**：Batch-4 ingest · P3 lint CI

### 其它 active

| task | 排期 |
|------|------|
| [`task_ui_chain_events_backend.md`](../../tasks/active/task_ui_chain_events_backend.md) | P3 |

---

## active task 头字段（反孤岛常模）

新建或修订 `active/task_*.md` 时，Harness 元信息表 **建议** 增：

| 字段 | 示例 | 说明 |
|------|------|------|
| **schedule_ref** | `RECENT §1.1 #L1-R2` | 本仓排期表锚点 |
| **epic** | `ChatBI V3 · P2 韧性` | Epic 归属 |
| **blocked_by** | `Loop R1 done` | 前置条件 |
| **blocks** | `P2-2` | 阻塞下游（可选） |

与 Harness 元信息 `task_slug` · `git_branch` · `freeze_id` · 链图谱路径（改 api 时）保持不变。

---

## RECENT 维护触发

| 事件 | 动作 |
|------|------|
| 新开 active task | RECENT §1.1 增行 + §8 修订 |
| task 关账 | `git mv` done/ · `_views/done.md` · RECENT 改 done |
| Epic 里程碑 | §6.6 或 diary 留证 |
| 本页 active 表 | **随 RECENT §1.1 同步** |

---

## 链接

- 排期真值：[`RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md)  
- Task 落盘规则：[`docs/tasks/README.md`](../../tasks/README.md)  
- P2 Loop SKILL：[`SKILL-harness-loop-batch.md`](../../tasks/skills/SKILL-harness-loop-batch.md)  
- 三方读序 smoke：[`conclusion_smoke_zh.md`](../../harness/experiments/task_schedule_read_smoke_v1/conclusion_smoke_zh.md)  
- 三层总览：[[llm-wiki-layers]]  
- 需求对比：[[../WIKI_REQUIREMENTS_COMPARISON_v1_zh.md]]
