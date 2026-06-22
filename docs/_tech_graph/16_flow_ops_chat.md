---
graph_id: 16_flow_ops_chat
version: 2026-06-22
generated_at: 2026-06-22T07:48:09Z
source: docs/_tech_graph/16_flow_ops_chat.graph.yaml
---

# Ops Desk Chat / Orchestrator 子流程

Ops Orchestrator（00帽）· fast/deep 路由 · issue_analyst · review · ops_runs/events · 不复用 Unified Chat chain

## Mermaid

```mermaid
flowchart TD
    OPS_REQ[POST /ops/chat/messages]
    CLASSIFY[OpsOrchestrator.classify_intent]
    FAST[route=fast]
    DEEP[route=deep]
    DEMO[ops_demo_answers]
    METRICS[metrics template · GET /ops/metrics/*]
    RUN[ops_runs · run_id]
    ANALYST[issue_analyst · 子 Agent]
    REVIEW[review_gate · 20帽]
    SYNTH[synthesize]
    PARTIAL[synthesize_partial]
    EVT[ops_run_events · seq++]
    CKPT[ops_run_checkpoints]
    LG[LangGraph checkpointer]
    OPS_SB[Supabase ops_*]
    OPS_LLM[OPS_LLM provider]
    ANS[final.answer · END]
    GET_RUN[GET /ops/runs/{id}]
    GET_EVT[GET /ops/runs/{id}/events?after_seq=]
    OPS_SSE[GET /ops/runs/{id}/stream · progress only]
    RETRY[POST /ops/runs/{id}/retry]
    NOT_UC[≠ Unified Chat /api/py/unified/chat]

    OPS_REQ --> CLASSIFY
    // → api/ops/::chat_messages (P1 · 规划)
    CLASSIFY --"fast"--> FAST
    CLASSIFY --"deep"--> DEEP
    FAST --"demo hit"--> DEMO
    FAST --"metrics/list"--> METRICS
    FAST --"optional light events"--> EVT
    DEMO --> ANS
    METRICS --> OPS_SB
    METRICS --> ANS
    DEEP --> RUN
    RUN --> OPS_SB
    RUN --"delegate"--> ANALYST
    ANALYST --"只读 ops_issues/pr"--> OPS_SB
    ANALYST --"~>"--> OPS_LLM
    ANALYST --> REVIEW
    REVIEW --"[ok] pass"--> SYNTH
    REVIEW --"[retry] ≤2"--> ANALYST
    REVIEW --"[partial]"--> PARTIAL
    SYNTH --> EVT
    PARTIAL --> EVT
    EVT --> OPS_SB
    EVT --> ANS
    RUN --"P1-b"--> LG
    LG --> CKPT
    GET_RUN --> OPS_SB
    GET_EVT --> OPS_SB
    GET_EVT --"断联续看"--> EVT
    OPS_SSE --"progress only"--> EVT
    RETRY --"retry_token 幂等"--> RUN
    CLASSIFY --"禁止复用 chain"--> NOT_UC

    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

## Structured Data

### Nodes

| ID | Label | Kind |
|----|-------|------|
| OPS_REQ | POST /ops/chat/messages |  |
| CLASSIFY | OpsOrchestrator.classify_intent |  |
| FAST | route=fast |  |
| DEEP | route=deep |  |
| DEMO | ops_demo_answers |  |
| METRICS | metrics template · GET /ops/metrics/* |  |
| RUN | ops_runs · run_id |  |
| ANALYST | issue_analyst · 子 Agent |  |
| REVIEW | review_gate · 20帽 |  |
| SYNTH | synthesize |  |
| PARTIAL | synthesize_partial |  |
| EVT | ops_run_events · seq++ |  |
| CKPT | ops_run_checkpoints |  |
| LG | LangGraph checkpointer |  |
| OPS_SB | Supabase ops_* |  |
| OPS_LLM | OPS_LLM provider |  |
| ANS | final.answer · END |  |
| GET_RUN | GET /ops/runs/{id} |  |
| GET_EVT | GET /ops/runs/{id}/events?after_seq= |  |
| OPS_SSE | GET /ops/runs/{id}/stream · progress only |  |
| RETRY | POST /ops/runs/{id}/retry |  |
| NOT_UC | ≠ Unified Chat /api/py/unified/chat |  |

### Edges

| From | To | Mark | Type | Label | Anchors |
|------|----|------|------|-------|---------|
| OPS_REQ | CLASSIFY | -> | depends_on |  | 1 anchor(s) |
| CLASSIFY | FAST | ?> | condition | fast |  |
| CLASSIFY | DEEP | ?> | condition | deep |  |
| FAST | DEMO | ?> | condition | demo hit |  |
| FAST | METRICS | ?> | condition | metrics/list |  |
| FAST | EVT | ~> | async_calls | optional light events |  |
| DEMO | ANS | -> | depends_on |  |  |
| METRICS | OPS_SB | -> | depends_on |  |  |
| METRICS | ANS | -> | depends_on |  |  |
| DEEP | RUN | -> | depends_on |  |  |
| RUN | OPS_SB | -> | depends_on |  |  |
| RUN | ANALYST | -> | depends_on | delegate |  |
| ANALYST | OPS_SB | -> | depends_on | 只读 ops_issues/pr |  |
| ANALYST | OPS_LLM | ~> | async_calls |  |  |
| ANALYST | REVIEW | -> | depends_on |  |  |
| REVIEW | SYNTH | ?> | condition | [ok] pass |  |
| REVIEW | ANALYST | ?> | condition | [retry] ≤2 |  |
| REVIEW | PARTIAL | ?> | condition | [partial] |  |
| SYNTH | EVT | -> | depends_on |  |  |
| PARTIAL | EVT | -> | depends_on |  |  |
| EVT | OPS_SB | -> | depends_on |  |  |
| EVT | ANS | -> | depends_on |  |  |
| RUN | LG | ::triggers | triggers | P1-b |  |
| LG | CKPT | -> | depends_on |  |  |
| GET_RUN | OPS_SB | -> | depends_on |  |  |
| GET_EVT | OPS_SB | -> | depends_on |  |  |
| GET_EVT | EVT | ::yields | yields | 断联续看 |  |
| OPS_SSE | EVT | ::yields | yields | progress only |  |
| RETRY | RUN | -> | depends_on | retry_token 幂等 |  |
| CLASSIFY | NOT_UC | ::gates | gates | 禁止复用 chain |  |

## Notes

### 分期

| 阶段 | 交付 |
| --- | --- |
| **P1-a** | 手写 FSM · Orchestrator + issue_analyst + review · events 落库 |
| **P1-b** | LangGraph + `ops_run_checkpoints` · 与 P1-a 行为等价 |

### 与 Unified Chat 边界（SPEC §4.6.2）

- **禁止**复用 `ChatBIAgent` / `/api/py/unified/chat` chain
- **仅借鉴** intent→step→emit 结构与 event type 命名
- 数据源：`ops_*` 同步表 · 非 `rag_conversation_logs`

### 锚点（P1 实现时回填）

- `api/ops/orchestrator/` · `api/ops/chat/`（规划）
- 前端 BFF：`../ai-ink-brain/app/api/ops/chat/`（规划）
- 规格：`../ai-ink-brain/docs/tasks/specs/SPEC_ops_desk_kimi_code_mvp_v1_zh.md` §4.6
- 思考轮：`../../docs/harness/invokes/by-task/ops-desk-kimi-code-spec-refine/rounds/ROUND_09_R8_orchestrator_langgraph.md`

### Review 最小规则（SPEC §4.6.4）

- `#NNN` 须在 `ops_issues` / `ops_pull_requests` 存在
- 禁止写 Git / 开 PR 指令
- `confidence < 0.5` 且无 evidence → partial


