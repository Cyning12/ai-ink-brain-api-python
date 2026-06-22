# Task · Ops Desk P1-3 · Orchestrator Core（P1-a FSM）

> **状态**：`active` · **blocked until P1-2 同分支提交**  
> **SPEC**：§4.6  
> **图谱**：[`16_flow_ops_chat.md`](../../_tech_graph/16_flow_ops_chat.md)  
> **invoke**：R8 · [`DIAGRAM_00_orchestrator_agents_human_v1_zh.md`](../../../../docs/harness/guides/DIAGRAM_00_orchestrator_agents_human_v1_zh.md)  
> **依赖**：P1-1 metrics · P1-2 runs/events schema  
> **后继**：P1-5 chat-ui（前端）· P1-4 langgraph（可选后置）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p1-orchestrator-core` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P1-ORCHESTRATOR-CORE` |
| **git_branch** | `task/ops-desk-p1-backend-chain` |
| **链序** | P1-3 / 3 · **本串行链终点** |

---

## 背景与目标

实现 **Ops Orchestrator（00 帽）** 手写 FSM：fast/deep 路由 · `issue_analyst` · `review_gate` · `ops_run_events` 落库。

### 完成态

- [ ] `api/ops/orchestrator/`（classify · fast · deep · review · synthesize）
- [ ] `api/ops/agents/issue_analyst.py`（只读 ops_issues/pr · LLM 可 mock）
- [ ] HTTP：
  - `POST /ops/chat/messages` → `{ run_id, route, status }`
  - `GET /ops/runs/{id}`
  - `GET /ops/runs/{id}/events?after_seq=`
  - `POST /ops/runs/{id}/retry`（`retry_token`）
- [ ] **禁止**复用 `/api/py/unified/chat` · `ChatBIAgent`
- [ ] `tests/ops_desk/test_orchestrator_p1.py`（mock LLM + store · required）
- [ ] 深析 Demo issue：**#545**（或 ISSUE_SCAN 较新 open issue）

---

## Fast path

| 意图 | 行为 |
| --- | --- |
| `metrics_trend` | 调 P1-1 metrics |
| `issue_list` / `pr_list` | 调 P1-1 list API |
| demo 命中 | 直返模板（无 LLM）· 可接 P1-6 表后补 |

## Deep path

`classify` → `ops_runs` → `issue_analyst` → `review`（V1–V4 · R8 §3.4）→ `synthesize` → `final.answer` event

Review 失败：`retry` ≤2 或 `partial`

---

## 非范围

- LangGraph / checkpointer 运行时（P1-4）
- SSE stream（可 stub 404 · P1-5 前不强制）
- 前端 Chat 页（P1-5）
- `ops_demo_answers` 全量（P1-6）

---

## 验收标准

- [x] fast：metrics 类问题无 LLM 调用（assert mock）
- [x] deep：#545 类问题产出 events 时间线 · `review.pass` 或 `partial`
- [x] `after_seq` 增量可读
- [x] retry_token 幂等
- [x] 全量 pytest + `bash scripts/verify-tech-graph.sh` 绿

---

## 40 自检表

| 项 | 状态 | 证据 |
| --- | --- | --- |
| pytest tests/ops_desk/ -v | ✅ pass | 22 passed (P1-1 7 + P1-3 8 + P1-2 6 skipped) |
| pytest tests -m "not intent_eval and not intent_benchmark" -q | ✅ pass | 457 passed, 14 skipped |
| bash scripts/verify-tech-graph.sh | ✅ pass | all slices OK |
| commit | ✅ | `feat(ops-desk): P1-3 orchestrator FSM and chat endpoints` |

## 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | LLM 超时/断联 | run `partial` · events 已写可续看 |
| F2 | issue# 不存在 | review fail → partial |
| F3 | retry_token 不匹配 | HTTP 409 |

---

## 图谱回填

- [x] 更新 `16_flow_ops_chat.graph.yaml` 锚点至真实 `api/ops/` 路径
- [x] compile · export · equivalence 绿

---

## 给 Cursor

`ops-desk-p1-orchestrator-core` · P1-a FSM only · LangGraph-ready schema。
