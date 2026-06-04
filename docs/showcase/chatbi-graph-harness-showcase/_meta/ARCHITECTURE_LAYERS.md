# 架构三层 · 全系列对照

> 各卷叙述须标注属于哪一层；避免把「治理落盘」误写成「产品新功能」。

---

## 1. 运行面（用户 / 集成方）

| 路径 | P0 后状态 | 人类可感知 |
| --- | --- | --- |
| `POST /api/py/unified/chat` | 行为不变 | 现有 Ink Unified Chat |
| `POST /api/py/unified/chat/stream` | 行为不变 | 现有 SSE Timeline |
| `POST /api/py/unified/chat/graph` | **stub 200** | 仅 curl/联调可见 |
| `POST /api/py/unified/chat/graph/stream` | **stub SSE** | 同上 |

真值：[`docs/_tech_graph/_manifest.json`](../../_tech_graph/_manifest.json)

---

## 2. 代码面（模块布局）

```text
# P0 后（简化）
api/chatbi_events.py          # 从 agent 抽出
api/chatbi_agent_models.py
api/chatbi_failure.py
api/agent.py                  # run() 仍大 · 行为不变
api/graph/state.py            # ChatBIState + 边表草案
api/graph/runner.py           # stub 节点
api/unified_chat_graph.py     # Graph HTTP 薄 handler
api/unified_chat.py           # 未改行为（D-2）
```

路线图：[`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) §4.4

---

## 3. 治理面（Harness + CI）

| 环节 | 落盘 |
| --- | --- |
| 10 需求 | `docs/tasks/active/task_*.md` |
| 22 审查 | `docs/harness/reviews/task_*_audit_*.md` |
| 30/40 | task `### 自检结论` · invokes |
| 50 | `docs/tasks/reinspect_results/reinspect_*.md` |
| CI | `pytest` · `manifest_check` · `contract_check` · `drift_check` |

帽链真值：[`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md)

---

## 4. 与 P1/P2 的关系（预告）

| 阶段 | 运行面变化 | 见卷 |
| --- | --- | --- |
| **P1** | Graph 路由真实 Agent 环 + SSE parity | vol-04 |
| **P2** | HITL / checkpointer / subgraph | vol-05 |
